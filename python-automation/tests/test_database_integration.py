import re

import pytest
from bson import ObjectId

from config import CANDIDATE_EMAIL, RECRUITER_EMAIL

pytestmark = pytest.mark.db

BCRYPT_HASH_RE = re.compile(r'^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$')


class TestUserCollection:
    def test_candidate_document_exists_with_expected_fields(self, mongo_db):
        user = mongo_db.users.find_one({'email': CANDIDATE_EMAIL})
        assert user is not None
        assert user['role'] == 'candidate'
        assert 'name' in user
        assert 'skills' in user

    def test_recruiter_document_exists_with_expected_fields(self, mongo_db):
        user = mongo_db.users.find_one({'email': RECRUITER_EMAIL})
        assert user is not None
        assert user['role'] == 'recruiter'

    def test_passwords_are_bcrypt_hashed_not_plaintext(self, mongo_db):
        users = list(mongo_db.users.find({}, {'passwordHash': 1, 'email': 1}).limit(20))
        assert len(users) > 0
        for user in users:
            assert 'passwordHash' in user
            assert user['passwordHash'] != ''
            assert BCRYPT_HASH_RE.match(user['passwordHash']), (
                f"passwordHash for {user['email']} does not look like a bcrypt hash: {user['passwordHash'][:10]}..."
            )

    def test_no_plaintext_password_field_present(self, mongo_db):
        users = list(mongo_db.users.find({}).limit(20))
        for user in users:
            assert 'password' not in user

    def test_user_role_is_restricted_to_known_values(self, mongo_db):
        users = list(mongo_db.users.find({}, {'role': 1}).limit(50))
        for user in users:
            assert user['role'] in ('candidate', 'recruiter')


class TestJobCollection:
    def test_jobs_collection_has_documents(self, mongo_db):
        count = mongo_db.jobs.count_documents({})
        assert count > 0

    def test_job_documents_reference_valid_recruiter(self, mongo_db):
        jobs = list(mongo_db.jobs.find({}).limit(10))
        assert len(jobs) > 0
        for job in jobs:
            assert isinstance(job['postedBy'], ObjectId)
            poster = mongo_db.users.find_one({'_id': job['postedBy']})
            assert poster is not None
            assert poster['role'] == 'recruiter'

    def test_job_documents_have_required_fields(self, mongo_db):
        job = mongo_db.jobs.find_one({})
        assert job is not None
        for field in ('title', 'company', 'description', 'employmentType', 'experienceLevel'):
            assert field in job


class TestApplicationCollection:
    def test_application_documents_reference_valid_job_and_candidate(self, mongo_db):
        applications = list(mongo_db.applications.find({}).limit(10))
        for app in applications:
            job = mongo_db.jobs.find_one({'_id': app['job']})
            candidate = mongo_db.users.find_one({'_id': app['candidate']})
            assert job is not None
            assert candidate is not None
            assert candidate['role'] == 'candidate'

    def test_duplicate_application_unique_index_exists(self, mongo_db):
        indexes = mongo_db.applications.index_information()
        composite_indexes = [
            spec for spec in indexes.values()
            if spec.get('unique') and {'job', 'candidate'}.issubset({k for k, _ in spec['key']})
        ]
        assert len(composite_indexes) >= 1, 'Expected a unique compound index on (job, candidate)'


class TestSavedJobCollection:
    def test_saved_job_unique_index_exists(self, mongo_db):
        indexes = mongo_db.savedjobs.index_information()
        composite_indexes = [
            spec for spec in indexes.values()
            if spec.get('unique') and {'job', 'candidate'}.issubset({k for k, _ in spec['key']})
        ]
        assert len(composite_indexes) >= 1, 'Expected a unique compound index on (job, candidate)'


class TestDataPersistence:
    def test_write_and_read_back_marker_document(self, mongo_db):
        marker_id = mongo_db.test_markers.insert_one({'source': 'pytest-db-integration'}).inserted_id
        found = mongo_db.test_markers.find_one({'_id': marker_id})
        assert found is not None
        assert found['source'] == 'pytest-db-integration'
        mongo_db.test_markers.delete_one({'_id': marker_id})
