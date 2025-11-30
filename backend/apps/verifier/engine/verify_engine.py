"""
Purpose:
    Central coordination file that calls all the other checkers and returns a structured result.
    Acts as the main “email verification engine” for your project.

Key points:
    Input: email string
    Output: dictionary with keys:

{
    "syntax_valid": True/False,
    "has_mx": True/False,
    "is_disposable": True/False,
    "is_role": True/False
}

Calls: 
    syntax_checker, mx_lookup, disposable_checker, role_checker.

Optional: 
    uses normalize_email() from utils.py to clean email before processing.
"""
from .syntax_checker import is_syntax_valid
from .mx_lookup import has_mx_record
from .disposable_checker import is_disposable
from .role_checker import is_role_account
from .utils import normalize_email

def verify(email: str):
    email = normalize_email(email)

    result = {
        "syntax_valid": is_syntax_valid(email),
        "has_mx": has_mx_record(email),
        "is_disposable": is_disposable(email),
        "is_role": is_role_account(email),
    }

    result["deliverable"] = (
        result["syntax_valid"]
        and result["has_mx"]
        and not result["is_disposable"]
    )

    return result

def map_to_yes_no(value: bool) -> str:
    """
    Converts a boolean to "Yes" or "No" string for user-friendly display.
    """
    return "Yes" if value else "No"

