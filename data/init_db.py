from data.db_manager import DatabaseManager
from data.schemas import Base


def init_db():
    engine = DatabaseManager.get_engine()
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas (caso não existissem)")


if __name__ == "__main__":
    init_db()
