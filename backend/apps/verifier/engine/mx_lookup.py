"""
Purpose:
    Checks whether the email’s domain has valid MX (mail exchange) records, meaning the domain can receive emails.

Key points:
    Input: email string
    Output: True / False
    Uses get_domain() from utils.py to extract domain from email.
    Handles exceptions when domain has no MX record or DNS errors.
"""
import dns.resolver
from .utils import get_domain

def has_mx_record(email: str) -> bool:
    """
    Checks whether the email's domain has valid MX records.
    """
    domain = get_domain(email)
    if not domain:
        return False

    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False
