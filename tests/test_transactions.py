from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas
from app.models import TransactionType

def test_delete_own_transaction(client: TestClient, db_session: Session):
    user = crud.create_user(db_session, schemas.UserCreate(email="test@test.com", name="test", password="password"))
    transaction_data = schemas.TransactionCreate(trans_type=TransactionType.INCOME, amount=100.0, description="Salary")
    transaction = crud.create_user_transaction(db_session, transaction_data, user.id)

    login_response = client.post("/users/token", data={"username": "test@test.com", "password": "password"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/transactions/{transaction.id}", headers=headers)

    assert response.status_code == 204

    deleted_transaction = crud.get_transaction_by_id(db_session, transaction.id)
    assert deleted_transaction is None

def test_delete_other_user_transaction_forbidden(client: TestClient, db_session: Session):
    user_owner = crud.create_user(db_session, schemas.UserCreate(email="owner@test.com", name="Owner", password="password"))
    user_attacker = crud.create_user(db_session, schemas.UserCreate(email="attacker@test.com", name="Attacker", password="password"))

    transaction_data = schemas.TransactionCreate(trans_type=TransactionType.EXPENSE, amount=50.0, description="Rent")
    transaction = crud.create_user_transaction(db_session, transaction_data, user_owner.id)

    login_response = client.post("/users/token", data={"username": "attacker@test.com", "password": "password"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/transactions/{transaction.id}", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to delete this transaction."