import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / '.env')
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent

FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/careerhub')

BROWSER = os.getenv('BROWSER', 'chrome').lower()
SUPPORTED_BROWSERS = ('chrome', 'edge')

HOLD_SECONDS = 6
EXPLICIT_WAIT_SECONDS = 15

SCREENSHOTS_DIR = BASE_DIR / 'screenshots'
REPORTS_DIR = BASE_DIR / 'reports'
SCREENSHOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

CANDIDATE_EMAIL = os.getenv('CANDIDATE_EMAIL', 'candidate@careerhub.com')
CANDIDATE_PASSWORD = os.getenv('CANDIDATE_PASSWORD', 'CareerHub@123')
RECRUITER_EMAIL = os.getenv('RECRUITER_EMAIL', 'recruiter@careerhub.com')
RECRUITER_PASSWORD = os.getenv('RECRUITER_PASSWORD', 'CareerHub@123')

VIEWPORTS = {
    'desktop': (1440, 900),
    'tablet': (768, 1024),
    'mobile': (390, 844),
}
