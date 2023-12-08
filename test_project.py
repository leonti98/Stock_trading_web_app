import pytest
from project import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client


def test_home_page_redirect(client):
    response = client.get("/home")
    assert response.status_code == 302  # Expecting a redirect if not logged in


def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_successful_registration(client):
    response = client.post(
        "/register", data={"username": "new_user", "password": "new_password"}
    )
    assert (
        response.status_code == 302
    )  # Expecting a redirect after successful registration


def test_registration_duplicate_username(client):
    response = client.post(
        "/register", data={"username": "user1", "password": "password1"}
    )
    assert b"Username already exists" in response.data


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_successful_login(client):
    response = client.post(
        "/login", data={"username": "user1", "password": "password1"}
    )
    assert response.status_code == 302  # Expecting a redirect after successful login


def test_login_invalid_username(client):
    response = client.post(
        "/login", data={"username": "nonexistent_user", "password": "password1"}
    )
    assert b"Invalid username" in response.data


def test_login_invalid_password(client):
    response = client.post(
        "/login", data={"username": "user1", "password": "incorrect_password"}
    )
    assert b"Invalid password" in response.data


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302  # Expecting a redirect


def test_buy_route(client):
    response = client.post("/buy", json={"symbol": "AAPL", "quantity": 5})
    assert (
        response.status_code == 200
    )  # Assuming a successful purchase returns status 200


def test_buy_insufficient_funds(client):
    response = client.post("/buy", json={"symbol": "AAPL", "quantity": 999999})
    assert (
        response.status_code == 200
    )  # Assuming a successful response, as the user is not logged in
    assert b"Please log in to buy stocks." in response.data


def test_sell_not_enough_shares(client):
    response = client.post("/sell", json={"symbol": "AAPL", "quantity": 999999})
    assert (
        response.status_code == 200
    )  # Assuming a successful response, as the user is not logged in
    assert b"Please log in to sell stocks." in response.data


def test_get_user_data(client):
    response = client.get("/get_user_data")
    assert (
        response.status_code == 200
    )  # Assuming a successful response, as the user is not logged in
    assert (
        b'"error"' in response.data
    )  # Ensure there is an error in the response for non-authenticated users


def test_logout_redirect(client):
    # Logout and check for redirect to login page
    response_logout = client.get("/logout", follow_redirects=True)
    assert (
        response_logout.status_code == 200
    )  # Assuming a successful logout returns status 200
    assert b"Login" in response_logout.data
