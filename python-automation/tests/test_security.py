import pytest
import requests

from config import API_BASE_URL, CANDIDATE_EMAIL, CANDIDATE_PASSWORD, RECRUITER_EMAIL, RECRUITER_PASSWORD, FRONTEND_URL
from pages.auth_page import LoginPage
from utils.test_data import XSS_PAYLOADS, NOSQL_INJECTION_PAYLOADS
from utils.test_helpers import hold_important_page

pytestmark = pytest.mark.security


def _login(email, password):
    resp = requests.post(f'{API_BASE_URL}/auth/login', json={'email': email, 'password': password}, timeout=10)
    resp.raise_for_status()
    return resp.json()['token']


class TestAuthenticationSecurity:
    def test_protected_endpoint_rejects_missing_token(self):
        resp = requests.get(f'{API_BASE_URL}/profile', timeout=10)
        assert resp.status_code == 401

    def test_protected_endpoint_rejects_malformed_token(self):
        headers = {'Authorization': 'Bearer not-a-real-jwt-token'}
        resp = requests.get(f'{API_BASE_URL}/profile', headers=headers, timeout=10)
        assert resp.status_code == 401

    def test_protected_endpoint_rejects_tampered_token(self):
        token = _login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
        tampered = token[:-4] + 'abcd'
        headers = {'Authorization': f'Bearer {tampered}'}
        resp = requests.get(f'{API_BASE_URL}/profile', headers=headers, timeout=10)
        assert resp.status_code == 401

    def test_login_response_never_exposes_password_hash(self):
        resp = requests.post(
            f'{API_BASE_URL}/auth/login',
            json={'email': CANDIDATE_EMAIL, 'password': CANDIDATE_PASSWORD},
            timeout=10
        )
        body = resp.json()
        assert 'passwordHash' not in body['user']
        assert 'password' not in body['user']


class TestRoleBasedAccessControl:
    def test_candidate_cannot_create_job(self):
        token = _login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.post(
            f'{API_BASE_URL}/jobs',
            headers=headers,
            json={'title': 'Hacked Job', 'company': 'N/A', 'description': 'should not be allowed to create'},
            timeout=10
        )
        assert resp.status_code == 403

    def test_recruiter_cannot_apply_to_job(self):
        jobs = requests.get(f'{API_BASE_URL}/jobs?limit=1', timeout=10).json()['jobs']
        assert len(jobs) >= 1
        token = _login(RECRUITER_EMAIL, RECRUITER_PASSWORD)
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.post(
            f'{API_BASE_URL}/applications',
            headers=headers,
            json={'jobId': jobs[0]['_id'], 'coverLetter': 'should not be allowed'},
            timeout=10
        )
        assert resp.status_code == 403

    def test_recruiter_cannot_access_another_recruiters_job_applications(self):
        jobs = requests.get(f'{API_BASE_URL}/jobs?limit=1', timeout=10).json()['jobs']
        job_id = jobs[0]['_id']

        token = _login(RECRUITER_EMAIL, RECRUITER_PASSWORD)
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.get(f'{API_BASE_URL}/applications/job/{job_id}', headers=headers, timeout=10)
        assert resp.status_code in (200, 403)

    def test_candidate_cannot_view_recruiter_stats(self):
        token = _login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.get(f'{API_BASE_URL}/recruiter/stats', headers=headers, timeout=10)
        assert resp.status_code == 403


class TestInputSanitization:
    @pytest.mark.parametrize('payload', XSS_PAYLOADS)
    def test_registration_handles_xss_payload_in_name_safely(self, payload):
        resp = requests.post(
            f'{API_BASE_URL}/auth/register',
            json={'name': payload, 'email': f'xss_{abs(hash(payload))}@careerhub-test.com',
                  'password': 'StrongPass123', 'role': 'candidate'},
            timeout=10
        )
        assert resp.status_code in (201, 400)
        if resp.status_code == 201:
            assert resp.json()['user']['name'] == payload

    @pytest.mark.parametrize('payload', NOSQL_INJECTION_PAYLOADS)
    def test_login_handles_nosql_injection_payload_safely(self, payload):
        resp = requests.post(
            f'{API_BASE_URL}/auth/login',
            json={'email': payload, 'password': payload},
            timeout=10
        )
        assert resp.status_code in (400, 401)


class TestUiAccessRestrictions:
    def test_candidate_redirected_away_from_recruiter_dashboard(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
        hold_important_page()
        driver.get(f'{FRONTEND_URL}/recruiter')
        hold_important_page()
        login_page.screenshot('rbac_candidate_blocked_from_recruiter_dashboard')
        assert not login_page.is_present('recruiter-tabs')

    def test_unauthenticated_user_redirected_to_login_from_profile(self, driver):
        driver.get(f'{FRONTEND_URL}/profile')
        hold_important_page()
        assert 'login' in driver.current_url
