import time

import pytest
import requests

from config import API_BASE_URL, CANDIDATE_EMAIL, CANDIDATE_PASSWORD, RECRUITER_EMAIL, RECRUITER_PASSWORD
from utils.test_data import unique_email

pytestmark = pytest.mark.api


def _token(email, password):
    resp = requests.post(f'{API_BASE_URL}/auth/login', json={'email': email, 'password': password}, timeout=10)
    resp.raise_for_status()
    return resp.json()['token']


@pytest.fixture(scope='module')
def candidate_token():
    return _token(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)


@pytest.fixture(scope='module')
def recruiter_token():
    return _token(RECRUITER_EMAIL, RECRUITER_PASSWORD)


@pytest.fixture(scope='module')
def sample_job_id():
    resp = requests.get(f'{API_BASE_URL}/jobs?limit=1', timeout=10)
    jobs = resp.json()['jobs']
    assert len(jobs) >= 1
    return jobs[0]['_id']


class TestAuthEndpoints:
    def test_register_returns_201_and_token(self):
        payload = {'name': 'API Test User', 'email': unique_email('api'), 'password': 'StrongPass123', 'role': 'candidate'}
        resp = requests.post(f'{API_BASE_URL}/auth/register', json=payload, timeout=10)
        assert resp.status_code == 201
        body = resp.json()
        assert 'token' in body
        assert body['user']['email'] == payload['email']

    def test_register_duplicate_email_returns_409(self):
        payload = {'name': 'Dup User', 'email': unique_email('dup'), 'password': 'StrongPass123', 'role': 'candidate'}
        first = requests.post(f'{API_BASE_URL}/auth/register', json=payload, timeout=10)
        assert first.status_code == 201
        second = requests.post(f'{API_BASE_URL}/auth/register', json=payload, timeout=10)
        assert second.status_code == 409

    def test_register_missing_fields_returns_400(self):
        resp = requests.post(f'{API_BASE_URL}/auth/register', json={'email': 'x@x.com'}, timeout=10)
        assert resp.status_code == 400

    def test_login_valid_credentials_returns_200(self, candidate_token):
        assert candidate_token is not None

    def test_login_invalid_credentials_returns_401(self):
        resp = requests.post(
            f'{API_BASE_URL}/auth/login',
            json={'email': CANDIDATE_EMAIL, 'password': 'WrongPassword'},
            timeout=10
        )
        assert resp.status_code == 401

    def test_me_endpoint_returns_current_user(self, candidate_token):
        resp = requests.get(f'{API_BASE_URL}/auth/me', headers={'Authorization': f'Bearer {candidate_token}'}, timeout=10)
        assert resp.status_code == 200
        assert resp.json()['user']['email'] == CANDIDATE_EMAIL


class TestJobEndpoints:
    def test_list_jobs_returns_200(self):
        resp = requests.get(f'{API_BASE_URL}/jobs', timeout=10)
        assert resp.status_code == 200
        assert 'pagination' in resp.json()

    def test_get_single_job_returns_200(self, sample_job_id):
        resp = requests.get(f'{API_BASE_URL}/jobs/{sample_job_id}', timeout=10)
        assert resp.status_code == 200
        assert resp.json()['job']['_id'] == sample_job_id

    def test_get_job_with_invalid_id_returns_400(self):
        resp = requests.get(f'{API_BASE_URL}/jobs/not-a-valid-id', timeout=10)
        assert resp.status_code == 400

    def test_get_job_with_nonexistent_id_returns_404(self):
        resp = requests.get(f'{API_BASE_URL}/jobs/000000000000000000000000', timeout=10)
        assert resp.status_code == 404

    def test_create_job_without_auth_returns_401(self):
        resp = requests.post(f'{API_BASE_URL}/jobs', json={'title': 'X', 'company': 'Y', 'description': 'Z' * 20}, timeout=10)
        assert resp.status_code == 401

    def test_create_job_as_candidate_returns_403(self, candidate_token):
        resp = requests.post(
            f'{API_BASE_URL}/jobs',
            headers={'Authorization': f'Bearer {candidate_token}'},
            json={'title': 'X', 'company': 'Y', 'description': 'Z' * 20},
            timeout=10
        )
        assert resp.status_code == 403

    def test_create_job_as_recruiter_returns_201(self, recruiter_token):
        resp = requests.post(
            f'{API_BASE_URL}/jobs',
            headers={'Authorization': f'Bearer {recruiter_token}'},
            json={
                'title': 'API Created Role', 'company': 'API Co',
                'description': 'A job created directly through the API test suite.',
                'skills': ['Python'], 'salaryMin': 400000, 'salaryMax': 600000
            },
            timeout=10
        )
        assert resp.status_code == 201
        job = resp.json()['job']
        assert job['title'] == 'API Created Role'

        update_resp = requests.put(
            f'{API_BASE_URL}/jobs/{job["_id"]}',
            headers={'Authorization': f'Bearer {recruiter_token}'},
            json={'title': 'API Updated Role'},
            timeout=10
        )
        assert update_resp.status_code == 200
        assert update_resp.json()['job']['title'] == 'API Updated Role'

        delete_resp = requests.delete(
            f'{API_BASE_URL}/jobs/{job["_id"]}',
            headers={'Authorization': f'Bearer {recruiter_token}'},
            timeout=10
        )
        assert delete_resp.status_code == 200

    def test_search_jobs_by_query_param(self):
        resp = requests.get(f'{API_BASE_URL}/jobs', params={'search': 'Developer'}, timeout=10)
        assert resp.status_code == 200
        assert isinstance(resp.json()['jobs'], list)

    def test_pagination_boundary_large_page_returns_empty_list(self):
        resp = requests.get(f'{API_BASE_URL}/jobs', params={'page': 9999, 'limit': 10}, timeout=10)
        assert resp.status_code == 200
        assert resp.json()['jobs'] == []


class TestApplicationEndpoints:
    def test_apply_without_auth_returns_401(self, sample_job_id):
        resp = requests.post(f'{API_BASE_URL}/applications', json={'jobId': sample_job_id}, timeout=10)
        assert resp.status_code == 401

    def test_apply_with_invalid_job_id_returns_400(self, candidate_token):
        resp = requests.post(
            f'{API_BASE_URL}/applications',
            headers={'Authorization': f'Bearer {candidate_token}'},
            json={'jobId': 'invalid'},
            timeout=10
        )
        assert resp.status_code == 400

    def test_apply_and_duplicate_application_returns_409(self, sample_job_id):
        fresh_email = unique_email('apiapplicant')
        register = requests.post(
            f'{API_BASE_URL}/auth/register',
            json={'name': 'API Applicant', 'email': fresh_email, 'password': 'StrongPass123', 'role': 'candidate'},
            timeout=10
        )
        token = register.json()['token']
        headers = {'Authorization': f'Bearer {token}'}

        first = requests.post(f'{API_BASE_URL}/applications', headers=headers, json={'jobId': sample_job_id}, timeout=10)
        assert first.status_code == 201

        second = requests.post(f'{API_BASE_URL}/applications', headers=headers, json={'jobId': sample_job_id}, timeout=10)
        assert second.status_code == 409

    def test_get_my_applications_returns_200(self, candidate_token):
        resp = requests.get(f'{API_BASE_URL}/applications/mine', headers={'Authorization': f'Bearer {candidate_token}'}, timeout=10)
        assert resp.status_code == 200
        assert isinstance(resp.json()['applications'], list)


class TestSavedJobEndpoints:
    def test_save_and_list_and_remove_job(self, sample_job_id):
        fresh_email = unique_email('apisaver')
        register = requests.post(
            f'{API_BASE_URL}/auth/register',
            json={'name': 'API Saver', 'email': fresh_email, 'password': 'StrongPass123', 'role': 'candidate'},
            timeout=10
        )
        headers = {'Authorization': f'Bearer {register.json()["token"]}'}

        save_resp = requests.post(f'{API_BASE_URL}/saved-jobs', headers=headers, json={'jobId': sample_job_id}, timeout=10)
        assert save_resp.status_code == 201

        duplicate_save = requests.post(f'{API_BASE_URL}/saved-jobs', headers=headers, json={'jobId': sample_job_id}, timeout=10)
        assert duplicate_save.status_code == 409

        list_resp = requests.get(f'{API_BASE_URL}/saved-jobs', headers=headers, timeout=10)
        assert list_resp.status_code == 200
        assert len(list_resp.json()['savedJobs']) >= 1

        remove_resp = requests.delete(f'{API_BASE_URL}/saved-jobs/{sample_job_id}', headers=headers, timeout=10)
        assert remove_resp.status_code == 200


class TestProfileEndpoints:
    def test_get_profile_returns_200(self, candidate_token):
        resp = requests.get(f'{API_BASE_URL}/profile', headers={'Authorization': f'Bearer {candidate_token}'}, timeout=10)
        assert resp.status_code == 200

    def test_update_profile_returns_200(self, candidate_token):
        resp = requests.put(
            f'{API_BASE_URL}/profile',
            headers={'Authorization': f'Bearer {candidate_token}'},
            json={'headline': 'Updated via API test', 'skills': ['Python', 'Pytest']},
            timeout=10
        )
        assert resp.status_code == 200
        assert resp.json()['user']['headline'] == 'Updated via API test'

    def test_update_profile_invalid_phone_returns_400(self, candidate_token):
        resp = requests.put(
            f'{API_BASE_URL}/profile',
            headers={'Authorization': f'Bearer {candidate_token}'},
            json={'phone': '!!!invalid!!!'},
            timeout=10
        )
        assert resp.status_code == 400


class TestRecruiterStatsEndpoint:
    def test_recruiter_stats_returns_200(self, recruiter_token):
        resp = requests.get(f'{API_BASE_URL}/recruiter/stats', headers={'Authorization': f'Bearer {recruiter_token}'}, timeout=10)
        assert resp.status_code == 200
        body = resp.json()
        assert 'totalJobs' in body
        assert 'totalApplications' in body

    def test_recruiter_stats_forbidden_for_candidate(self, candidate_token):
        resp = requests.get(f'{API_BASE_URL}/recruiter/stats', headers={'Authorization': f'Bearer {candidate_token}'}, timeout=10)
        assert resp.status_code == 403


class TestResponseTime:
    def test_jobs_listing_responds_within_reasonable_time(self):
        start = time.time()
        resp = requests.get(f'{API_BASE_URL}/jobs', timeout=10)
        elapsed_ms = (time.time() - start) * 1000
        assert resp.status_code == 200
        assert elapsed_ms < 2000, f'Jobs listing took {elapsed_ms:.0f}ms, expected under 2000ms'

    def test_login_responds_within_reasonable_time(self):
        start = time.time()
        requests.post(f'{API_BASE_URL}/auth/login', json={'email': CANDIDATE_EMAIL, 'password': CANDIDATE_PASSWORD}, timeout=10)
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < 2000, f'Login took {elapsed_ms:.0f}ms, expected under 2000ms'


class TestUnknownRoute:
    def test_unknown_route_returns_404(self):
        resp = requests.get(f'{API_BASE_URL}/this-route-does-not-exist', timeout=10)
        assert resp.status_code == 404
