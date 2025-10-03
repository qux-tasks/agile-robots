import pytest
import requests
from etc import config_parser


HEADERS = {"Content-Type": "application/json"}


def test_auth_success():
    """
        Positive case
    """
    payload = {"username": config_parser.username, "password": config_parser.password}
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json=payload)

    assert response.status_code == 200

    body = response.json()
    assert "token" in body, body["reason"]
    assert isinstance(body["token"], str)
    assert len(body["token"]) > 0

@pytest.mark.parametrize("username,password", [
    ("wrongUser", "password123"),
    ("admin", "wrongPassword"),
    ("wrongUser", "wrongPassword"),
])
def test_auth_invalid_credentials(username, password):
    """
        Case with invalid credentials
    """
    payload = {"username": username, "password": password}
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json=payload)

    assert response.status_code in [200, 401]
    body = response.json()
    assert "token" not in body
    assert "reason" in body
    assert body['reason'] == "Bad credentials"

def test_auth_empty_body():
    """
        Case with empty body
    """
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json={})

    assert response.status_code in [200, 400]
    body = response.json()
    assert "token" not in body
    assert "reason" in body
    assert body['reason'] == "Bad credentials"

def test_auth_missing_username():
    """
        Case without username
    """
    payload = {"password": config_parser.password}
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json=payload)

    assert response.status_code in [200, 400]
    body = response.json()
    assert "token" not in body
    assert "reason" in body
    assert body['reason'] == "Bad credentials"

def test_auth_missing_password():
    """
        Case without password
    """
    payload = {"username": config_parser.username}
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json=payload)

    assert response.status_code in [200, 400]
    body = response.json()
    assert "token" not in body
    assert "reason" in body
    assert body['reason'] == "Bad credentials"

def test_auth_wrong_content_type():
    """
        Case with wrong Content-Type
    """
    headers = {"Content-Type": "text/plain"}
    response = requests.post(config_parser.auth_endpoint, data="username=admin&password=password123", headers=headers)
    assert response.status_code in [400, 415]

def test_auth_empty_headers():
    """
        Case with empty headers
    """
    payload = {"username": config_parser.username, "password": config_parser.password}
    response = requests.post(config_parser.auth_endpoint, headers={}, json=payload)

    assert response.status_code in [400, 401, 415]