import allure
import httpx

BASE_URL = "https://airportgap.com/api"


@allure.id("TC001")
@allure.label("positive case")
@allure.tag("airport")
@allure.title("get airport")
def test_get_airport():
    with allure.step("Hit endpoint"):
        resp = httpx.get(
            url=f"{BASE_URL}/airports",
        )

    with allure.step("Check status code"):
        assert resp.status_code == 200

    with allure.step("Check body response"):
        body = resp.json()
        assert len(body["data"]) == 30

        assert body["data"][0]["attributes"]
        assert body["data"][0]["attributes"]["altitude"]
        assert body["data"][0]["attributes"]["city"]
        assert body["data"][0]["attributes"]["country"]
        assert body["data"][0]["attributes"]["iata"]
        assert body["data"][0]["attributes"]["icao"]
        assert body["data"][0]["attributes"]["latitude"]
        assert body["data"][0]["attributes"]["longitude"]
        assert body["data"][0]["attributes"]["name"]
        assert body["data"][0]["attributes"]["timezone"]
        assert body["data"][0]["id"]
        assert body["data"][0]["type"]

        assert body["links"]["first"] == "https://airportgap.com/api/airports"
        assert body["links"]["last"] == "https://airportgap.com/api/airports?page=203"
        assert body["links"]["next"] == "https://airportgap.com/api/airports?page=2"
        assert body["links"]["prev"] == "https://airportgap.com/api/airports"
        assert body["links"]["self"] == "https://airportgap.com/api/airports"


@allure.id("TC002")
@allure.label("positive case")
@allure.tag("airport")
@allure.title("get airport by page")
def test_get_airport_by_page():
    with allure.step("Hit endpoint"):
        resp = httpx.get(
            url=f"{BASE_URL}/airports",
            params={"page": 3},
        )

    with allure.step("Check status code"):
        assert resp.status_code == 200

    with allure.step("Check body response"):
        body = resp.json()
        assert len(body["data"]) == 30

        assert body["data"][0]["attributes"]
        assert body["data"][0]["attributes"]["altitude"]
        assert body["data"][0]["attributes"]["city"]
        assert body["data"][0]["attributes"]["country"]
        assert body["data"][0]["attributes"]["iata"]
        assert body["data"][0]["attributes"]["icao"]
        assert body["data"][0]["attributes"]["latitude"]
        assert body["data"][0]["attributes"]["longitude"]
        assert body["data"][0]["attributes"]["name"]
        assert body["data"][0]["attributes"]["timezone"]
        assert body["data"][0]["id"]
        assert body["data"][0]["type"]

        assert body["links"]["first"] == "https://airportgap.com/api/airports"
        assert body["links"]["last"] == "https://airportgap.com/api/airports?page=203"
        assert body["links"]["next"] == "https://airportgap.com/api/airports?page=4"
        assert body["links"]["prev"] == "https://airportgap.com/api/airports?page=2"
        assert body["links"]["self"] == "https://airportgap.com/api/airports?page=3"


@allure.id("TC003")
@allure.label("positive case")
@allure.tag("airport")
@allure.title("get airport by last page")
def test_get_airport_by_last_page():
    with allure.step("Hit endpoint"):
        resp = httpx.get(
            url=f"{BASE_URL}/airports",
            params={"page": 203},
        )

    with allure.step("Check status code"):
        assert resp.status_code == 200

    with allure.step("Check body response"):
        body = resp.json()
        assert len(body["data"]) == 12

        assert body["data"][0]["attributes"]
        assert body["data"][0]["attributes"]["altitude"]
        assert body["data"][0]["attributes"]["city"]
        assert body["data"][0]["attributes"]["country"]
        assert body["data"][0]["attributes"]["iata"]
        assert body["data"][0]["attributes"]["icao"]
        assert body["data"][0]["attributes"]["latitude"]
        assert body["data"][0]["attributes"]["longitude"]
        assert body["data"][0]["attributes"]["name"]
        assert body["data"][0]["attributes"]["timezone"] is None
        assert body["data"][0]["id"]
        assert body["data"][0]["type"]

        assert body["links"]["first"] == "https://airportgap.com/api/airports"
        assert body["links"]["last"] == "https://airportgap.com/api/airports?page=203"
        assert body["links"]["next"] == "https://airportgap.com/api/airports"
        assert body["links"]["prev"] == "https://airportgap.com/api/airports?page=202"
        assert body["links"]["self"] == "https://airportgap.com/api/airports?page=203"


@allure.id("TC004")
@allure.label("negative case")
@allure.tag("airport")
@allure.title("get airport by out of range page")
def test_get_airport_by_out_range_page():
    with allure.step("Hit endpoint"):
        resp = httpx.get(
            url=f"{BASE_URL}/airports",
            params={"page": 1000},
        )

    with allure.step("Check status code"):
        assert resp.status_code == 200

    with allure.step("Check body response"):
        body = resp.json()
        assert len(body["data"]) == 0


@allure.id("TC005")
@allure.label("negative case")
@allure.tag("airport")
@allure.title("get airport by page alphabetic (not number)")
def test_get_airport_by_string_value():
    with allure.step("Hit endpoint"):
        resp = httpx.get(
            url=f"{BASE_URL}/airports",
            params={"page": "one"},
        )

    with allure.step("Check status code"):
        assert resp.status_code == 404

    with allure.step("Check body response"):
        assert (
            "<title>The page you were looking for doesn't exist (404 Not found)</title>"
            in resp.text
        )


@allure.id("TC006")
@allure.label("positive case")
@allure.tag("airport")
@allure.title("get airport by valid id")
def test_get_airport_by_valid_id():
    with allure.step("Hit endpoint"):
        resp = httpx.get(
            url=f"{BASE_URL}/airports/KIX",
        )

    with allure.step("Check status code"):
        assert resp.status_code == 200

    with allure.step("Check body response"):
        body = resp.json()

        assert body["data"]["id"] == "KIX"
        assert body["data"]["type"] == "airport"

        assert body["data"]["attributes"]
        assert body["data"]["attributes"]["altitude"] == 26
        assert body["data"]["attributes"]["city"] == "Osaka"
        assert body["data"]["attributes"]["country"] == "Japan"
        assert body["data"]["attributes"]["iata"] == "KIX"
        assert body["data"]["attributes"]["icao"] == "RJBB"
        assert body["data"]["attributes"]["latitude"] == "34.427299"
        assert body["data"]["attributes"]["longitude"] == "135.244003"
        assert body["data"]["attributes"]["name"] == "Kansai International Airport"
        assert body["data"]["attributes"]["timezone"] == "Asia/Tokyo"


@allure.id("TC007")
@allure.label("positive case")
@allure.tag("airport")
@allure.title("get airport by invalid id")
def test_get_airport_by_invalid_id():
    with allure.step("Hit endpoint"):
        resp = httpx.get(
            url=f"{BASE_URL}/airports/KISS",
        )

    with allure.step("Check status code"):
        assert resp.status_code == 404

    with allure.step("Check body response"):
        assert resp.json() == {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "The page you requested could not be found",
                }
            ]
        }


@allure.id("TC008")
@allure.label("positive case")
@allure.tag("airport")
@allure.title("get distance airport using valid id")
def test_airport_distance_valid_from_to():
    with allure.step("Hit endpoint"):
        resp = httpx.post(
            url=f"{BASE_URL}/airports/distance",
            params={
                "from": "KIX",
                "to": "NRT",
            },
        )

    with allure.step("Check status code"):
        assert resp.status_code == 200

    with allure.step("Check body response"):
        assert resp.json() == {
            "data": {
                "attributes": {
                    "from_airport": {
                        "altitude": 26,
                        "city": "Osaka",
                        "country": "Japan",
                        "iata": "KIX",
                        "icao": "RJBB",
                        "id": 3158,
                        "latitude": "34.427299",
                        "longitude": "135.244003",
                        "name": "Kansai International Airport",
                        "timezone": "Asia/Tokyo",
                    },
                    "kilometers": 490.8053652969214,
                    "miles": 304.76001022047103,
                    "nautical_miles": 264.82908133654655,
                    "to_airport": {
                        "altitude": 141,
                        "city": "Tokyo",
                        "country": "Japan",
                        "iata": "NRT",
                        "icao": "RJAA",
                        "id": 1721,
                        "latitude": "35.764702",
                        "longitude": "140.386002",
                        "name": "Narita International Airport",
                        "timezone": "Asia/Tokyo",
                    },
                },
                "id": "KIX-NRT",
                "type": "airport_distance",
            }
        }


@allure.id("TC009")
@allure.label("negative case")
@allure.tag("airport")
@allure.title("get distance airport using invalid value from-to")
def test_airport_distance_invalid_from_to():
    distances = [["XXX", "YYY"], ["KIX", "XXX"], ["XXX", "NRT"]]
    for distance in distances:
        with allure.step("Hit endpoint"):
            resp = httpx.post(
                url=f"{BASE_URL}/airports/distance",
                params={
                    "from": distance[0],
                    "to": distance[1],
                },
            )

        with allure.step("Check status code"):
            assert resp.status_code == 422

        with allure.step("Check body response"):
            assert resp.json() == {
                "errors": [
                    {
                        "status": "422",
                        "title": "Unable to process request",
                        "detail": "Please enter valid 'from' and 'to' airports.",
                    }
                ]
            }
