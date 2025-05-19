from database import create_db_and_tables
<<<<<<< HEAD

# Import models so their metadata is registered with SQLModel
from models import plan, user  # noqa: F401
=======
from models import plan, user
>>>>>>> 504c450 (run linter)


def main() -> None:
    create_db_and_tables()
    print("Database tables created!")


if __name__ == "__main__":
    main()
