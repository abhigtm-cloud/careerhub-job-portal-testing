# CareerHub — Job Portal + Python Test Automation

Academic mini-project: **Automation Testing of CareerHub – Job Portal Using Python, Selenium and Pytest**
Student: **Ritika** · UID: **23BCA10289** · Chandigarh University

## 1. What's in this repository

| Folder | Contents |
|---|---|
| `backend/` | Express + MongoDB REST API (JWT auth, jobs, applications, saved jobs, profile, recruiter stats) |
| `frontend/` | React + Vite + Bootstrap 5 job portal UI |
| `python-automation/` | Pytest + Selenium (Page Object Model) + Requests + PyMongo test suite |
| `postman/` | Postman collection + environment for Newman API testing |
| `docs/` | Academic report (DOCX/PDF) |

## 2. Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- MongoDB running locally (`mongodb://127.0.0.1:27017`)
- Google Chrome and/or Microsoft Edge installed (Selenium runs with a **visible** browser window — never headless, never Firefox)

## 3. Run the application

**Backend**
```bash
cd backend
npm install
npm run dev
```
Backend runs on `http://localhost:5000`.

**Seed the database** (demo accounts + 8 realistic job listings; safe to re-run, skips if already seeded)
```bash
cd backend
npm run seed
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`.

### Demo credentials (development only)

| Role | Email | Password |
|---|---|---|
| Candidate | `candidate@careerhub.com` | `CareerHub@123` |
| Recruiter | `recruiter@careerhub.com` | `CareerHub@123` |

Both roles also have one-click **Demo candidate / Demo recruiter** buttons on the login page.

## 4. Run the Python automation suite

```bash
cd python-automation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Make sure the backend (`:5000`), frontend (`:5173`) and MongoDB are all running first.

**Run everything:**
```bash
pytest -v --html=reports/report.html --self-contained-html
```

**Run individual categories:**
```bash
pytest tests/test_database_integration.py -v
pytest tests/test_api_endpoints.py -v
pytest tests/test_ui_authentication.py -v
pytest tests/test_ui_job_management.py -v
pytest tests/test_ui_job_applications.py -v
pytest tests/test_ui_saved_jobs_profile.py -v
pytest tests/test_responsive_layout.py -v
pytest tests/test_security.py -v
pytest tests/test_regression.py -v
pytest tests/test_smoke.py -v
pytest tests/test_cross_browser.py -v
```

**Notes on execution behaviour (mandatory, non-negotiable per project spec):**
- Selenium always launches a **visible, maximized** Chrome or Edge window — never `--headless`.
- Firefox is explicitly rejected (`build_driver('firefox')` raises `ValueError`).
- Every important screen is held on-screen for **6 seconds** via `utils.test_helpers.hold_important_page()` so it can be visually verified / screen-recorded.
- Screenshots are saved to `python-automation/screenshots/` with timestamped filenames.
- HTML report and console log are saved to `python-automation/reports/`.

## 5. Run the Postman/Newman API suite

```bash
npx newman run postman/CareerHub_API_Tests.postman_collection.json -e postman/CareerHub_Environment_Template.postman_environment.json
```

## 6. Project modules implemented

- JWT authentication with bcrypt password hashing, role-based access control (candidate / recruiter), protected routes, demo login
- Job board: search (title/company/skills), filters (type, experience), pagination, job detail modal, empty states, reset filters
- Applications: apply with optional cover letter, duplicate-application prevention (HTTP 409), application history with status
- Saved jobs: save / remove / list, persisted per candidate
- Candidate profile: edit name, headline, phone, skills
- Recruiter dashboard: post / edit / delete jobs, view applicants per job, dashboard statistics

## 7. Known limitations / honesty notes

- The academic report in `docs/` leaves the faculty name, subject code and exact academic-year fields as placeholders, since these were not supplied — fill them in before submission.
- Cross-browser testing covers Chrome and Microsoft Edge only (Firefox is intentionally excluded per the project brief).
- Test execution results in the generated HTML report reflect an actual run against this codebase on this machine; re-running after code changes will regenerate fresh numbers.
