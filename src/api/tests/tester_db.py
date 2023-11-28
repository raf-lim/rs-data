from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from db.base_class import Base


SQLALCHEMY_TEST_DB = "sqlite:///:memory:"

engine = create_engine(
        SQLALCHEMY_TEST_DB,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        )

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


