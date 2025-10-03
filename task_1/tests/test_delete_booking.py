
import pytest
import requests
from etc import config_parser
from http import HTTPStatus


def test_delete_booking_with_token(auth_token, booking_id):
    """
        Positive case - successful deletion of booking with token
    """
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.delete(f"{config_parser.booking_endpoint}/{booking_id}", headers=headers)

    assert response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED], f"Unexpected status code: {response.status_code}"

    get_resp = requests.get(f"{config_parser.booking_endpoint}/{booking_id}")
    assert get_resp.status_code == HTTPStatus.NOT_FOUND, f"Booking was not deleted: {get_resp.status_code}"

def test_delete_booking_with_basic_auth(booking_id):
    """
        Positive case - successful deletion of booking with basic auth
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM="
    }
    response = requests.delete(f"{config_parser.booking_endpoint}/{booking_id}", headers=headers)

    assert response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED], f"Unexpected status code: {response.status_code}"
    get_resp = requests.get(f"{config_parser.booking_endpoint}/{booking_id}")
    assert get_resp.status_code == HTTPStatus.NOT_FOUND, f"Booking was not deleted: {get_resp.status_code}"

def test_delete_booking_without_auth(booking_id):
    """
        Negative case - deletion without auth
    """
    response = requests.delete(f"{config_parser.booking_endpoint}/{booking_id}")
    assert response.status_code == HTTPStatus.FORBIDDEN, f"Unexpected status code: {response.status_code}"

def test_delete_non_existing_booking(auth_token):
    """
        Negative case - deletion of non-existent booking
    """
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    get_all_booking_ids = requests.get(config_parser.booking_endpoint)
    assert get_all_booking_ids.status_code == HTTPStatus.OK, f"Response was not 200: {response.status_code}"
    existing_ids_length = len(get_all_booking_ids.json())

    response = requests.delete(f"{config_parser.booking_endpoint}/{existing_ids_length + 99999999999}", headers=headers)

    assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.METHOD_NOT_ALLOWED], f"Unexpected status code: {response.status_code}"

@pytest.mark.parametrize("invalid_id", [0, -1])
def test_delete_booking_invalid_ids(auth_token, invalid_id):
    """
        Negative case - deletion with edge case IDs
    """
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.delete(f"{config_parser.booking_endpoint}/{invalid_id}", headers=headers)

    assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.METHOD_NOT_ALLOWED], f"Unexpected status code: {response.status_code}"