import pytest
import requests
from etc import config_parser
from etc import helpers
from http import HTTPStatus


HEADERS = {"Content-Type": "application/json"}


def test_auth_success():
    """
        Positive case
    """
    payload = helpers.build_user_payload(config_parser.username, config_parser.password)
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json=payload)

    assert response.status_code == HTTPStatus.OK, f"Response was not 200. Reason: {response.reason}"

    body = response.json()
    assert "token" in body, body["reason"]
    assert isinstance(body["token"], str), f"Token has unexpected type: {type(body["token"])}"
    assert len(body["token"]) > 0, f"Token has unexpected length: {len(body["token"])}"

@pytest.mark.parametrize("username, password", [
    ("wrongUser", "password123"),
    ("admin", "wrongPassword"),
    ("wrongUser", "wrongPassword"),
])
def test_auth_invalid_credentials(username, password):
    """
        Case with invalid credentials
    """
    payload = helpers.build_user_payload(username, password)
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED, f"Unexpected status code: {response.status_code}"
    body = response.json()
    assert "token" not in body, f"Token was returned for invalid credentials"
    assert "reason" in body, f"Reason was not provided for invalid credentials"
    assert body['reason'] == "Bad credentials", f"Unexpected reason: {body['reason']}"

def test_auth_empty_body():
    """
        Case with empty body
    """
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json={})

    assert response.status_code == HTTPStatus.BAD_REQUEST, f"Unexpected status code: {response.status_code}"
    body = response.json()
    assert "token" not in body, f"Token was returned for invalid credentials"
    assert "reason" in body, f"Reason was not provided for invalid credentials"
    assert body['reason'] == "Bad credentials", f"Unexpected reason: {body['reason']}"

@pytest.mark.skip(reason="Should be clarified expected status code: 400 or 401")
def test_auth_missing_username():
    """
        Case without username
    """
    payload = {"password": config_parser.password}
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST, f"Unexpected status code: {response.status_code}"
    body = response.json()
    assert "token" not in body, f"Token was returned for invalid credentials"
    assert "reason" in body, f"Reason was not provided for invalid credentials"
    assert body['reason'] == "Bad credentials", f"Unexpected reason: {body['reason']}"

@pytest.mark.skip(reason="Should be clarified expected status code: 400 or 401")
def test_auth_missing_password():
    """
        Case without password
    """
    payload = {"username": config_parser.username}
    response = requests.post(config_parser.auth_endpoint, headers=HEADERS, json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST, f"Unexpected status code: {response.status_code}"
    body = response.json()
    assert "token" not in body, f"Token was returned for invalid credentials"
    assert "reason" in body, f"Reason was not provided for invalid credentials"
    assert body['reason'] == "Bad credentials", f"Unexpected reason: {body['reason']}"

@pytest.mark.skip(reason="Should be clarified expected status code: 400, or 415")
def test_auth_wrong_content_type():
    """
        Case with wrong Content-Type
    """
    headers = {"Content-Type": "text/plain"}
    response = requests.post(config_parser.auth_endpoint, data="username=admin&password=password123", headers=headers)
    assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNSUPPORTED_MEDIA_TYPE], f"Unexpected status code: {response.status_code}"

@pytest.mark.skip(reason="Should be clarified expected status code: 400, 401, 415")
def test_auth_empty_headers():
    """
        Case with empty headers
    """
    payload = helpers.build_user_payload(config_parser.username, config_parser.password)
    response = requests.post(config_parser.auth_endpoint, headers={}, json=payload)
    assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.UNSUPPORTED_MEDIA_TYPE], f"Unexpected status code: {response.status_code}"