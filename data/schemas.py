from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
import enum
import datetime

Base = declarative_base()


class Difficulty(enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    puzzle_histories = relationship(
        "PuzzleHistory", back_populates="user", cascade="all, delete-orphan"
    )


class PuzzleHistory(Base):
    __tablename__ = "puzzle_history"

    id = Column(Integer, primary_key=True)
    image = Column(LargeBinary, nullable=False)
    solving_time = Column(Integer, nullable=False)
    played_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="puzzle_histories")
