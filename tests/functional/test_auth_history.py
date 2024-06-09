from http import HTTPStatus
from urllib.parse import urljoin

import pytest

from tests.settings import test_settings
from tests.test_data.auth_history import auth_history

AUTH_HISTORY_ENDPOINT = "api/v1/auth-history"

AUTH_HISTORY_URL = urljoin(test_settings.auth_api_url, AUTH_HISTORY_ENDPOINT)

pytestmark = pytest.mark.asyncio


async def test_get_all_auth_histories_wo_access_401(make_get_request):
    user_id = "1ed4dd3b-6235-4920-ab23-d51bafb5cbb2"
    status, response = await make_get_request(AUTH_HISTORY_ENDPOINT + f"/{user_id}")

    assert status == HTTPStatus.UNAUTHORIZED
    assert response["detail"] == "В cookies отсутствует access token"


async def test_all_auth_histories_success_200(
    put_data, access_token_admin, client_session, delete_row_from_table
):
    await put_data("authentication_histories", auth_history)
    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    user_id = "9304cf4c-75b7-4c06-8e70-aad73ef4d0d2"
    async with client_session.get(f"{AUTH_HISTORY_URL}/{user_id}") as raw_response:
        response = await raw_response.json()
        assert raw_response.status == HTTPStatus.OK
        assert len(response) == 2

    await delete_row_from_table(
        "authentication_histories", "1ed4dd3b-6235-4920-ab23-d51bafb5cbb2"
    )
    await delete_row_from_table(
        "authentication_histories", "97ac142b-8148-477b-811b-985340bc669e"
    )
