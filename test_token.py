import allure
import httpx
import pytest

BASE_URL = "https://airportgap.com/api"


@allure.id("TC001")
@allure.label("positive case")
@allure.tag("token")
@allure.title("email valid")
def test_token_email_valid():
    with allure.step("Hit endpoint"):
        resp = httpx.post(
            url=f"{BASE_URL}/tokens",
            params={
                "email": "ping@gmail.com",
                "password": "123456",
            },
        )

    with allure.step("Check status code"):
        assert resp.status_code == 200

    with allure.step("Check body response"):
        assert "token" in resp.json()
        assert len(resp.json()["token"]) != 0


@allure.id("TC002")
@allure.label("negative case")
@allure.tag("token")
@allure.title("email unregistered")
def test_token_email_unregistered():
    with allure.step("Hit endpoint"):
        resp = httpx.post(
            url=f"{BASE_URL}/tokens",
            params={
                "email": "wrong@gmail.com",
                "password": "wrong123456",
            },
        )

    with allure.step("Check status code"):
        assert resp.status_code == 401

    with allure.step("Check body response"):
        body_resp = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "You are not authorized to perform the requested action.",
                }
            ]
        }
        assert resp.json() == body_resp

@allure.id("TC003")
@allure.label("negative case")
@allure.tag("token")
@allure.title("email invalid format")
def test_token_email_invalid_format():
    with allure.step("Hit endpoint"):
        resp = httpx.post(
            url=f"{BASE_URL}/tokens",
            params={
                "email": "wronggmail.com",
                "password": "wrong123456",
            },
        )

    with allure.step("Check status code"):
        assert resp.status_code == 401

    with allure.step("Check body response"):
        body_resp = {
            "errors": [
                {
                    "status": "401",
                    "title": "Unauthorized",
                    "detail": "You are not authorized to perform the requested action.",
                }
            ]
        }
        assert resp.json() == body_resp


@pytest.mark.skip("flaky")
@allure.id("TC004")
@allure.label("positive case")
@allure.tag("token")
@allure.title("rate limit < 100/minute")
def test_token_rate_limit_not_reached():
    for i in range(1, 50):
        with allure.step(f"Hit endpoint {i}"):
            resp = httpx.post(
                url=f"{BASE_URL}/tokens",
                params={
                    "email": "ping@gmail.com",
                    "password": "123456",
                },
            )

        with allure.step("Check status code"):
            assert resp.status_code == 200

        with allure.step("Check body response"):
            assert "token" in resp.json()
            assert len(resp.json()["token"]) != 0


@pytest.mark.skip("flaky")
@allure.id("TC005")
@allure.label("positive case")
@allure.tag("token")
@allure.title("rate limit > 100/minute")
def test_token_rate_limit_reached():
    for i in range(1, 200):
        with allure.step(f"Hit endpoint {i}"):
            resp = httpx.post(
                url=f"{BASE_URL}/tokens",
                params={
                    "email": "ping@gmail.com",
                    "password": "123456",
                },
            )

        with allure.step("Check status code"):
            assert resp.status_code == 200

        with allure.step("Check body response"):
            assert "token" in resp.json()
            assert len(resp.json()["token"]) != 0
