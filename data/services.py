from data.db_manager import DatabaseManager
from data.schemas import User, PuzzleHistory, Difficulty
from sqlalchemy.orm import joinedload
from utils.bcrypt import hash_password, check_password
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    @classmethod
    def create_user(
        cls, username: str, password: str
    ) -> tuple[Optional[User], Optional[str]]:
        """
        Creates a new user with hashed password
        Returns tuple: (User object, error message)
        """
        session = DatabaseManager.get_session()
        try:
            if not username or len(username) < 3:
                return None, "username must be at least 3 characters long"
            if not password or len(password) < 8:
                return None, "password must be at least 8 characters long"

            existing_user = cls.get_user_by_username(username)
            if existing_user:
                return None, "username already exists"

            hashed_password = hash_password(password)
            if not hashed_password:
                return None, "Failed to hash password"

            user = User(username=username, password=password)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user, None
        except SQLAlchemyError as e:
            session.rollback()
            print(f"database error creating user: {e}")
            return None, "database error"
        except Exception as e:
            print(f"unexpected error creating user: {e}")
            return None, "unexpected error"
        finally:
            session.close()

    @classmethod
    def get_user_by_username(cls, username: str) -> Optional[User]:
        """Retrieves a user by username with their puzzle histories"""
        session = DatabaseManager.get_session()
        try:
            return (
                session.query(User)
                .options(joinedload(User.puzzle_histories))
                .filter_by(username=username)
                .first()
            )
        except SQLAlchemyError as e:
            print(f"database error fetching user: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def delete_user(cls, user_id: int) -> tuple[bool, Optional[str]]:
        """Deletes a user and returns (success, error)"""
        session = DatabaseManager.get_session()
        try:
            user = session.query(User).get(user_id)
            if not user:
                return False, "user not found"

            session.delete(user)
            session.commit()
            return True, None
        except SQLAlchemyError as e:
            session.rollback()
            print(f"database error deleting user: {e}")
            return False, "database error"
        finally:
            session.close()

    @classmethod
    def update_password(
        cls, user_id: int, new_password: str
    ) -> tuple[bool, Optional[str]]:
        """Updates user password with new hash"""
        session = DatabaseManager.get_session()
        try:
            user = session.query(User).get(user_id)
            if not user:
                return False, "user not found"

            hashed_password = hash_password(new_password)
            if not hashed_password:
                return False, "failed to hash password"

            user.password = hashed_password
            session.commit()
            return True, None

        except SQLAlchemyError as e:
            session.rollback()
            print(f"database error updating password: {e}")
            return False, "database error"
        finally:
            session.close()


class PuzzleHistoryService:
    @classmethod
    def add_puzzle_history(
        cls, user_id: int, solving_time: int, image: str, difficulty: Difficulty
    ) -> tuple[Optional[PuzzleHistory], Optional[str]]:
        """Adds a new puzzle history record"""
        session = DatabaseManager.get_session()
        try:
            if solving_time < 0:
                return None, "solving time cannot be negative"

            history = PuzzleHistory(
                user_id=user_id,
                solving_time=solving_time,
                difficulty=difficulty,
                image=image,
            )
            session.add(history)
            session.commit()
            session.refresh(history)
            return history, None
        except SQLAlchemyError as e:
            session.rollback()
            print(f"database error adding history: {e}")
            return None, "database error"
        finally:
            session.close()

    @classmethod
    def get_puzzle_histories_for_user(
        cls, user_id: int
    ) -> tuple[Optional[list[PuzzleHistory]], Optional[str]]:
        """Retrieves all puzzle histories for a user"""
        session = DatabaseManager.get_session()
        try:
            histories = (
                session.query(PuzzleHistory)
                .filter_by(user_id=user_id)
                .order_by(PuzzleHistory.played_date.desc())
                .all()
            )
            return histories, None
        except SQLAlchemyError as e:
            print(f"database error fetching histories: {e}")
            return None, "database error"
        finally:
            session.close()

    @classmethod
    def delete_puzzle_history(cls, history_id: int) -> tuple[bool, Optional[str]]:
        """Deletes a puzzle history record"""
        session = DatabaseManager.get_session()
        try:
            history = session.query(PuzzleHistory).get(history_id)
            if not history:
                return False, "history not found"
            session.delete(history)
            session.commit()
            return True, None
        except SQLAlchemyError as e:
            session.rollback()
            print(f"database error deleting history: {e}")
            return False, "database error"
        finally:
            session.close()


class AuthService:
    @classmethod
    def authenticate_user(
        cls, username: str, password: str
    ) -> tuple[Optional[User], Optional[str]]:
        """
        Authenticates a user
        Returns tuple: (User object, error message)
        """
        try:
            if not username or not password:
                return None, "username and password are required"

            user = UserService.get_user_by_username(username)
            if not user:
                new_user, error = UserService.create_user(
                    username=username, password=hash_password(password)
                )
                if error:
                    return None, error
                return new_user, None

            if not check_password(password, user.password):
                return None, "invalid credentials"

            return user, None
        except Exception as e:
            print(f"authentication error: {e}")
            return None, "authentication error"
