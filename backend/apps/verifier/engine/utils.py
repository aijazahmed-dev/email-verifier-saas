"""
Purpose:
    Contains shared helper functions used across multiple modules to avoid duplicating logic.

Common functions:
    normalize_email(email) → strips spaces and converts to lowercase.
    get_domain(email) → extracts domain from email.

Optional: 
    get_local_part(email) → extracts local part for role checkers.

Why needed:
    Keeps code DRY (Don't Repeat Yourself)
    Ensures consistent email parsing across all modules
"""
def normalize_email(email: str) -> str:
    """
    Normalize email by stripping spaces and converting to lowercase.
    """
    return email.strip().lower()


def get_domain(email: str) -> str | None:
    """
    Returns the domain part of the email.
    """
    if "@" not in email:
        return None
    return email.split("@")[-1].lower()
