from http import HTTPStatus
from urllib.parse import urljoin

import pytest

from tests.settings import test_settings
from tests.test_data.user import registration_data

USER_ENDPOINT = "api/v1/user"
USER_URL = urljoin(test_settings.auth_api_url, USER_ENDPOINT)

pytestmark = pytest.mark.asyncio


async def test_refresh_token_401(make_post_request):
    status, response = await make_post_request(USER_URL + "/refresh")

    assert status == HTTPStatus.UNAUTHORIZED
    assert (
        response["detail"] == "Пользователь не авторизован, нет рефреш токена в cookies"
    )


async def test_refresh_token_200(refresh_token_unknown_role, client_session):
    client_session.cookie_jar.update_cookies(
        {"refresh_token": refresh_token_unknown_role}
    )

    async with client_session.post(USER_URL + "/refresh") as raw_response:
        response = await raw_response.json()

        assert raw_response.status == HTTPStatus.OK
        assert response["message"] == "Токен обновлен"


async def test_register_200(make_post_request, delete_row_from_table):
    status, response = await make_post_request(USER_URL + "/signup", registration_data)

    assert status == HTTPStatus.CREATED
    assert response["first_name"] == registration_data["first_name"]
    assert response["last_name"] == registration_data["last_name"]
    assert "password" not in response

    await delete_row_from_table("users", response["id"])


async def test_user_creating_w_already_existing_name(
    make_post_request, delete_row_from_table
):
    _, response = await make_post_request(USER_URL + "/signup", registration_data)
    status, response_error = await make_post_request(
        USER_URL + "/signup", registration_data
    )
    assert status == 400
    assert response_error["detail"] == "Значение поля: 'email' не уникально"

    await delete_row_from_table("users", response["id"])