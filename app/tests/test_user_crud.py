import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.database import Base
from app.crud.user import create_user, get_user_by_email
from utils.database import UserCreate


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
       yield db
    finally:
       db.close()
       Base.metadata.drop_all(bind=engine)


def test_create_and_get_user(db):
    user_in = UserCreate(name="Test", email="t@example.com", password="pass")
    user = create_user(db, user_in)
    fetched = get_user_by_email(db, "t@example.com")
    assert fetched is not None
    assert fetched.email == "t@example.com"