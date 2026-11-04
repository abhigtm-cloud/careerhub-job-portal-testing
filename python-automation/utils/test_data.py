import random
import string
import time


def unique_email(prefix: str = 'user') -> str:
    suffix = f'{int(time.time())}{random.randint(100, 999)}'
    return f'{prefix}_{suffix}@careerhub-test.com'


def random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))


INVALID_EMAILS = ['plainaddress', '@missingusername.com', 'user@.com', 'user@com', 'user name@site.com']
INVALID_PHONES = ['abcdefg', '123', '!!!not-a-phone!!!']
WEAK_PASSWORDS = ['', '123', 'a', 'ab']
XSS_PAYLOADS = ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>', "'; alert(1); //"]
NOSQL_INJECTION_PAYLOADS = [
    {'$gt': ''},
    {'$ne': None},
    "' || '1'=='1",
]
BOUNDARY_STRINGS = {
    'empty': '',
    'single_char': 'a',
    'max_name_length': 'a' * 80,
    'over_max_name_length': 'a' * 500,
    'special_chars': "O'Brien-Smith_Jr. (QA) #1 & Co.",
}
