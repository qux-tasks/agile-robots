
import pytest
import requests
from etc import config_parser


def test_delete_booking_with_token(auth_token, booking_id):
    """
        Positive case - successful deletion of booking with token
    """
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.delete(f"{config_parser.booking_endpoint}/{booking_id}", headers=headers)

    assert response.status_code in [200, 201]

    get_resp = requests.get(f"{config_parser.booking_endpoint}/{booking_id}")
    assert get_resp.status_code == 404


def test_delete_booking_with_basic_auth(booking_id):
    """
        Positive case - successful deletion of booking with basic auth
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM="
    }
    response = requests.delete(f"{config_parser.booking_endpoint}/{booking_id}", headers=headers)

    assert response.status_code in [200, 201]
    get_resp = requests.get(f"{config_parser.booking_endpoint}/{booking_id}")
    assert get_resp.status_code == 404


def test_delete_booking_without_auth(booking_id):
    """
        Negative case - deletion without auth
    """
    response = requests.delete(f"{config_parser.booking_endpoint}/{booking_id}")
    assert response.status_code == 403


def test_delete_non_existing_booking(auth_token):
    """
        Negative case - deletion of non-existent booking
    """
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    get_all_booking_ids = requests.get(config_parser.booking_endpoint)
    assert get_all_booking_ids.status_code == 200
    existing_ids_length = len(get_all_booking_ids.json())

    response = requests.delete(f"{config_parser.booking_endpoint}/{existing_ids_length + 99999999999}", headers=headers)

    assert response.status_code in [404, 405]


@pytest.mark.parametrize("invalid_id", [0, -1])
def test_delete_booking_invalid_ids(auth_token, invalid_id):
    """
        Negative case - deletion with edge case IDs
    """
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.delete(f"{config_parser.booking_endpoint}/{invalid_id}", headers=headers)

    assert response.status_code in [404, 405]