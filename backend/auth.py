import hashlib
from typing import Optional, Tuple

from .db import get_conn


def _hash_password(password: str) -> str:
    """Return a SHA‑256 hex digest of the password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _normalize_id(id_string: str) -> str:
    """
    Accepts "7" or "00007" and returns "7".
    Raises ValueError if not numeric.
    """
    return str(int(id_string)) 


def register_user(
    full_name: str, password: str, level: str
) -> Tuple[bool, str, Optional[int]]:
    """
    Insert a new user and return (success, message, id or None).
    """
    if not (full_name and password and level):
        return False, "All fields are required.", None

    hashed = _hash_password(password)

    try:
        with get_conn() as conn:
            cursor = conn.execute(
                "INSERT INTO users (full_name, password, level) VALUES (?, ?, ?)",
                (full_name, hashed, level),
            )
            user_id = cursor.lastrowid  # auto‑generated integer
        return (
            True,
            f"Registration successful!  Your ID is {str(user_id).zfill(5)}",
            user_id,
        )
    except Exception as exc:
        return False, f"Registration failed: {exc}", None


def authenticate_user(user_id: str, password: str) -> Optional[dict]:
    """
    Return a dict with user data if credentials are correct, else None.
    Accepts IDs with or without leading zeros.
    """
    try:
        uid_normalized = _normalize_id(user_id)
    except ValueError:
        return None

    hashed = _hash_password(password)

    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT id, full_name, level, right_answers, wrong_answers
            FROM users
            WHERE id = ? AND password = ?
            """,
            (uid_normalized, hashed),
        ).fetchone()

    if row:
        return {
            "id": row[0],
            "full_name": row[1],
            "level": row[2],
            "right_answers": row[3],
            "wrong_answers": row[4],
        }
    return None
