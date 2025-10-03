import pytest
import requests
from etc import config_parser
from http import HTTPStatus


def test_get_all_booking_ids():
    """
        Positive case without filters to get all booking IDs
    """
    response = requests.get(config_parser.booking_endpoint)
    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"

    body = response.json()
    assert isinstance(body, list), f"Response body has wrong type: {type(body)}"
    if body:
        for i in body:
            assert "bookingid" in i, f"'bookingid' was not found in item {i}"
            assert isinstance(i["bookingid"], int), f"'bookingid' is not integer: {type(i["bookingid"])}"

def test_get_booking_ids_by_name():
    """
        Positive case with filter by firstname and lastname
    """
    params = {"firstname": "Josh", "lastname": "Allen"}
    response = requests.get(config_parser.booking_endpoint, params=params)
    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"

    body = response.json()
    assert isinstance(body, list), f"Response body has wrong type: {type(body)}"
    if body:
        for i in body:
            assert "bookingid" in i, f"'bookingid' was not found in item {i}"
            assert isinstance(i["bookingid"], int), f"'bookingid' is not integer: {type(i["bookingid"])}"

def test_get_booking_ids_by_checkin_checkout():
    """
        Positive case with filter by checkin and checkout dates
    """
    params = {"checkin": "2014-03-13", "checkout": "2014-05-21"}
    response = requests.get(config_parser.booking_endpoint, params=params)
    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"

    body = response.json()
    assert isinstance(body, list), f"Response body has wrong type: {type(body)}"
    if body:
        for i in body:
            assert "bookingid" in i, f"'bookingid' was not found in item {i}"
            assert isinstance(i["bookingid"], int), f"'bookingid' is not integer: {type(i["bookingid"])}"

def test_get_booking_ids_combined_filters():
    """
        Positive case with combined filters
    """
    params = {
        "firstname": "sally",
        "lastname": "brown",
        "checkin": "2014-03-13",
        "checkout": "2014-05-21"
    }
    response = requests.get(config_parser.booking_endpoint, params=params)
    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"

    body = response.json()
    assert isinstance(body, list), f"Response body has wrong type: {type(body)}"
    if body:
        for i in body:
            assert "bookingid" in i, f"'bookingid' was not found in item {i}"
            assert isinstance(i["bookingid"], int), f"'bookingid' is not integer: {type(i["bookingid"])}"

@pytest.mark.parametrize("invalid_date", ["2022-99-99", "abcd-ef-gh", "01-01-2023"])
def test_get_booking_ids_invalid_date(invalid_date):
    """
        Negative case with invalid date format
    """
    params = {"checkin": invalid_date}
    response = requests.get(config_parser.booking_endpoint, params=params)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, f"Response was not 500: {response.status_code}"
    assert response.text == "Internal Server Error", f"Unexpected response test: {response.text}"

def test_get_booking_ids_empty_filters():
    """
        Case with empty filters
    """
    params = {"firstname": ""}
    response = requests.get(config_parser.booking_endpoint, params=params)
    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    body = response.json()
    assert isinstance(body, list), f"Response body has wrong type: {type(body)}"