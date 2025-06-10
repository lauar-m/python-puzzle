from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv
load_dotenv()


class DatabaseManager:
    @staticmethod
    def __get_db_url():
        db_url = os.environ.get("DB_PATH")
        if not db_url:
            raise ValueError("DB_PATH não está definido no .env ou não foi carregado corretamente.")
        return db_url

    __engine = create_engine(__get_db_url(), echo=False, future=True)
    __session_factory = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=__engine))

    @classmethod
    def get_session(cls):
        """Returns a database session"""
        return cls.__session_factory()

    @classmethod
    def get_engine(cls):
        return cls.__engine
