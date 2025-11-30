"""
Purpose:
    Detects if an email is from a disposable (temporary) email provider.
    Prevents users from registering or submitting disposable emails if needed.

Key points:
    Input: email string
    Output: True / False
    Uses get_domain() from utils.py for domain extraction.
    Compares domain with a predefined list of disposable providers.
"""
from .utils import get_domain

DISPOSABLE_DOMAINS = {
    "10minutemail.com",
    "guerrillamail.com",
    "mailinator.com",
    "tempmail.com",
    "trashmail.com",
    "getnada.com",
}

def is_disposable(email: str) -> bool:
    """
    Checks whether the email comes from a disposable provider.
    """
    domain = get_domain(email)
    if not domain:
        return False

    return domain in DISPOSABLE_DOMAINS
