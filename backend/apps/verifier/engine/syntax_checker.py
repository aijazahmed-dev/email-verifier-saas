"""
Purpose:
    Validates the syntax of an email using a regex.
    Ensures the email is in a proper format before other checks (MX, disposable, role).

Key points:
    Input: full email string
    Output: True / False
    Optional: can call normalize_email() from utils.py for consistent lowercase/whitespace stripping.
"""
from .utils import normalize_email
import re

EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def is_syntax_valid(email: str) -> bool:
    """
    Validates the syntax of an email using a strict regex.
    """
    email = normalize_email(email)  # optional
    if not email or "@" not in email:
        return False

    return bool(EMAIL_REGEX.match(email))
