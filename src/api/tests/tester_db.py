from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_TEST_DB = "sqlite:///:memory:"

engine = create_engine(
        SQLALCHEMY_TEST_DB,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        )

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()