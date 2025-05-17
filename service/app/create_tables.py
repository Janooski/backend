from database import create_db_and_tables

# Import models so their metadata is registered with SQLModel
from models import plan, user  # noqa: F401


def main() -> None:
    create_db_and_tables()
    print("Database tables created!")


if __name__ == "__main__":
    main()
