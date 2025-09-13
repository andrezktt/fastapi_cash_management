import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_database
from app.settings import settings

SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_database():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_database] = override_get_database
    yield TestClient(app)
    app.dependency_overrides.clear()