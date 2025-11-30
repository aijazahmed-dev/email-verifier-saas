"""
Purpose:
    Detects role-based accounts (e.g., admin@domain.com, support@domain.com).
    Useful to block generic inboxes from being used as user accounts.

Key points:
    Input: email string
    Output: True / False

Optional: 
    can use get_local_part() from utils.py for consistent local-part extraction.
    Checks if the local part (before @) is in a predefined set of role accounts.
"""
ROLE_ACCOUNTS = {
    "admin",
    "support",
    "info",
    "contact",
    "help",
    "sales",
    "marketing",
    "billing",
    "team",
    "office",
    "postmaster",
    "webmaster",
}

def is_role_account(email: str) -> bool:
    """
    Checks whether the email is a role-based account.
    """
    if "@" not in email:
        return False

    local_part = email.split("@")[0].lower()

    return local_part in ROLE_ACCOUNTS
