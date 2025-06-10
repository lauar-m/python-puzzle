from data.schemas import PuzzleHistory, User, Difficulty
from data.db_manager import DatabaseManager
from data.services import UserService, PuzzleHistoryService, AuthService

session = DatabaseManager.get_session()


user, error = UserService.create_user("bianca", "12345678")
if error:
    print(f"Error: {error}")
else:
    print(f"User create: {user.username}")

user, error = AuthService.authenticate_user("bianca", "123456")
if error:
    print(f"Login failed: {error}")
else:
    print(f"Welcome {user.username}!")

history, error = PuzzleHistoryService.add_puzzle_history(
    user_id=1,
    solving_time=120,
    difficulty=Difficulty.medium,
    image=""
)
if error:
    print(f"Error adding history: {error}")
else:
    print(user.puzzle_histories)