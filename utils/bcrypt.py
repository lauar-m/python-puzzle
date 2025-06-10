import bcrypt
from typing import Optional

HASH_ROUNDS = 12


def hash_password(password: str) -> Optional[str]:
    """Generates a secure hash from the password using bcrypt"""
    try:
        if not password or len(password) < 8:
            raise ValueError("password must be at least 8 characters long")
        
        salt = bcrypt.gensalt(rounds=HASH_ROUNDS)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    except Exception as e:
        print(f"Error hashing password: {e}")
        return None


def check_password(password: str, hashed_password: str) -> bool:
    """Checks if the password typed matches the correct password"""
    try:
        if not password or not hashed_password:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception as e:
        print(f"Error checking password: {e}")
        return False
