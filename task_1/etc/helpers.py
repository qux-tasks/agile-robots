def build_booking_payload(
    firstname="Jim",
    lastname="Brown",
    totalprice=111,
    depositpaid=True,
    checkin="2018-01-01",
    checkout="2019-01-01",
    additionalneeds="Breakfast"
):
    return {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
        },
        "additionalneeds": additionalneeds
    }