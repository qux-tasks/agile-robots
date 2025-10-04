import pytest
import requests
from etc import config_parser
from http import HTTPStatus


def test_get_booking_by_id():
    """
        Positive case to get booking by valid ID
    """
    get_all_booking_ids = requests.get(config_parser.booking_endpoint)
    assert get_all_booking_ids.status_code == HTTPStatus.OK, f"Response was not 200: {response.status_code}"
    assert len(get_all_booking_ids.json()) > 0, "No bookings returned from th service"

    testing_data = [
        get_all_booking_ids.json()[0],
        get_all_booking_ids.json()[-1],
        get_all_booking_ids.json()[len(get_all_booking_ids.json()) // 2]
    ]

    for i in testing_data:
        response = requests.get(f"{config_parser.booking_endpoint}/{i["bookingid"]}")
        assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"

        body = response.json()
        assert "firstname" in body, f"Response body does not contain 'firstname': {body}"
        assert "lastname" in body, f"Response body does not contain 'lastname': {body}"
        assert "totalprice" in body, f"Response body does not contain 'totalprice': {body}"
        assert "depositpaid" in body, f"Response body does not contain 'depositpaid': {body}"
        assert "bookingdates" in body, f"Response body does not contain 'bookingdates': {body}"
        assert "checkin" in body["bookingdates"], f"Response body does not contain 'checkin': {body["bookingdates"]}"
        assert "checkout" in body["bookingdates"], f"Response body does not contain 'checkout': {body["bookingdates"]}"
        assert "additionalneeds" in body, f"Response body does not contain 'additionalneeds': {body}"

def test_get_booking_invalid_id():
    """
        Negative case with non-existing booking ID
    """
    get_all_booking_ids = requests.get(config_parser.booking_endpoint)
    assert get_all_booking_ids.status_code == HTTPStatus.OK, f"Response was not 200: {response.status_code}"
    existing_ids_length = len(get_all_booking_ids.json())

    response = requests.get(f"{config_parser.booking_endpoint}/{existing_ids_length + 99999999999}")
    assert response.status_code == HTTPStatus.NOT_FOUND, f"Boking with non-existing ID returned"

def test_get_booking_non_numeric_id():
    """
        Negative case with non-numeric booking ID
    """
    response = requests.get(f"{config_parser.booking_endpoint}/abc")
    assert response.status_code == HTTPStatus.NOT_FOUND, f"Boking with non-existing ID returned"

@pytest.mark.parametrize("accept_type", ["application/json", "application/xml"])
def test_get_booking_with_accept_header(accept_type):
    """
        Positive case with different Accept headers
    """
    get_all_booking_ids = requests.get(config_parser.booking_endpoint)
    assert get_all_booking_ids.status_code == HTTPStatus.OK, f"Response was not 200: {response.status_code}"
    get_first_id = get_all_booking_ids.json()[0]["bookingid"]

    headers = {"Accept": accept_type}
    response = requests.get(f"{config_parser.booking_endpoint}/{get_first_id}", headers=headers)

    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    if accept_type == "application/json":
        assert response.headers["Content-Type"].startswith("application/json"), "Server does not support JSON"
        body = response.json()
        assert isinstance(body, dict), f"Response body is not a JSON object: {body}"
    elif accept_type == "application/xml":
        assert response.headers["Content-Type"].startswith("application/xml"), f"Unexpected Content-Type: {response.headers["Content-Type"]}"
        assert response.text.startswith("<?xml"), "Server does not support XML"

@pytest.mark.parametrize("invalid_id", [0, -1])
def test_get_booking_edge_case_ids(invalid_id):
    """
        Negative case with edge case IDs
    """
    response = requests.get(f"{config_parser.booking_endpoint}/{invalid_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND, f"Boking with non-existing ID returned"