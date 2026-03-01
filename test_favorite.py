import allure
import httpx
import pytest

BASE_URL = "https://airportgap.com/api"


@pytest.mark.order(1)
@allure.id("TC001")
@allure.label("positive case")
@allure.tag("favorite")
@allure.title("remove all favorite")
def test_remove_all_favorite():
    with allure.step("Get token"):
        token_resp = httpx.post(
            url=f"{BASE_URL}/tokens",
            params={
                "email": "ping@gmail.com",
                "password": "123456",
            },
        )
        token = token_resp.json()["token"]

    with allure.step(""):
        fav_resp = httpx.delete(
            url=f"{BASE_URL}/favorites/clear_all",
            headers={
                "Authorization": f"Token {token}",
            },
        )

    with allure.step("Check status code"):
        assert fav_resp.status_code == 204


@pytest.mark.order(2)
@allure.id("TC002")
@allure.label("negative case")
@allure.tag("favorite")
@allure.title("add favorite with airport_id and note")
def test_add_favorite_with_airport_id_and_note():
    with allure.step("Get token"):
        token_resp = httpx.post(
            url=f"{BASE_URL}/tokens",
            params={
                "email": "ping@gmail.com",
                "password": "123456",
            },
        )
        token = token_resp.json()["token"]

    with allure.step("Add new favorite"):
        fav_resp = httpx.post(
            url=f"{BASE_URL}/favorites",
            headers={
                "Authorization": f"Token {token}",
            },
            params={"airport_id": "KIX", "note": "fav airport"},
        )

    with allure.step("Check status code"):
        assert fav_resp.status_code == 201

    with allure.step("Check body response"):
        body = fav_resp.json()
        del body["data"]["id"]

        assert body == {
            "data": {
                "type": "favorite",
                "attributes": {
                    "airport": {
                        "id": 3158,
                        "name": "Kansai International Airport",
                        "city": "Osaka",
                        "country": "Japan",
                        "iata": "KIX",
                        "icao": "RJBB",
                        "latitude": "34.427299",
                        "longitude": "135.244003",
                        "altitude": 26,
                        "timezone": "Asia/Tokyo",
                    },
                    "note": "fav airport",
                },
            }
        }


@pytest.mark.order(3)
@allure.id("TC003")
@allure.label("positive case")
@allure.tag("favorite")
@allure.title("get favorite with token")
def test_get_favorite_with_token():
    with allure.step("Get token"):
        token_resp = httpx.post(
            url=f"{BASE_URL}/tokens",
            params={
                "email": "ping@gmail.com",
                "password": "123456",
            },
        )
        token = token_resp.json()["token"]

    with allure.step(""):
        fav_resp = httpx.get(
            url=f"{BASE_URL}/favorites",
            headers={
                "Authorization": f"Token {token}",
            },
        )

    with allure.step("Check status code"):
        assert fav_resp.status_code == 200

    with allure.step("Check body response"):
        body = fav_resp.json()
        del body["data"][0]["id"]

        assert body == {
            "data": [
                {
                    "type": "favorite",
                    "attributes": {
                        "airport": {
                            "id": 3158,
                            "name": "Kansai International Airport",
                            "city": "Osaka",
                            "country": "Japan",
                            "iata": "KIX",
                            "icao": "RJBB",
                            "latitude": "34.427299",
                            "longitude": "135.244003",
                            "altitude": 26,
                            "timezone": "Asia/Tokyo",
                        },
                        "note": "fav airport",
                    },
                }
            ],
            "links": {
                "first": "https://airportgap.com/api/airports",
                "self": "https://airportgap.com/api/airports",
                "last": "https://airportgap.com/api/airports?page=1",
                "prev": "https://airportgap.com/api/airports",
                "next": "https://airportgap.com/api/airports",
            },
        }


@allure.id("TC004")
@allure.label("negative case")
@allure.tag("favorite")
@allure.title("get favorite without token")
def test_get_favorite_without_token():
    with allure.step(""):
        fav_resp = httpx.get(
            url=f"{BASE_URL}/favorites",
        )

    with allure.step("Check status code"):
        assert fav_resp.status_code == 401

    with allure.step("Check body response"):
        assert fav_resp.json() == {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "You are not authorized to perform the requested action.",
                }
            ]
        }


@allure.id("TC005")
@allure.label("negative case")
@allure.tag("favorite")
@allure.title("get favorite with invalid token")
def test_get_favorite_invalid_token():
    with allure.step(""):
        fav_resp = httpx.get(
            url=f"{BASE_URL}/favorites",
            headers={
                "Authorization": "Token PxLWDKEqwSMgLXvvnp3frHqf",
            },
        )

    with allure.step("Check status code"):
        assert fav_resp.status_code == 401

    with allure.step("Check body response"):
        assert fav_resp.json() == {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "You are not authorized to perform the requested action.",
                }
            ]
        }


@allure.id("TC006")
@allure.label("positive case")
@allure.tag("favorite")
@allure.title("get favorite with id")
def test_edit_favorite_with_id():
    with allure.step("Get token"):
        token_resp = httpx.post(
            url=f"{BASE_URL}/tokens",
            params={
                "email": "ping@gmail.com",
                "password": "123456",
            },
        )
        token = token_resp.json()["token"]

    with allure.step("Get favorite airport by id"):
        fav_resp = httpx.patch(
            url=f"{BASE_URL}/favorites/3158",
            headers={
                "Authorization": f"Token {token}",
            },
            params={"note": "Edit"},
        )

    with allure.step("Check status code"):
        assert fav_resp.status_code == 404

    with allure.step("Check body response"):
        assert fav_resp.json() == {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "The page you requested could not be found",
                }
            ]
        }


@allure.id("TC001")
@allure.label("positive case")
@allure.tag("favorite")
@allure.title("remove by id")
def test_remove_by_id():
    with allure.step("Get token"):
        token_resp = httpx.post(
            url=f"{BASE_URL}/tokens",
            params={
                "email": "ping@gmail.com",
                "password": "123456",
            },
        )
        token = token_resp.json()["token"]

    with allure.step(""):
        fav_resp = httpx.delete(
            url=f"{BASE_URL}/favorites/1234",
            headers={
                "Authorization": f"Token {token}",
            },
        )

    with allure.step("Check status code"):
        assert fav_resp.status_code == 404

    with allure.step("Check body response"):
        assert fav_resp.json() == {
            "errors": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "The page you requested could not be found",
                }
            ]
        }
