from http import HTTPStatus
from urllib.parse import urljoin

import pytest

from tests.settings import test_settings

GENERAL_ROLE_ENDPOINT = "api/v1/role"
GENERAL_ROLE_URL = urljoin(test_settings.auth_api_url, GENERAL_ROLE_ENDPOINT)

pytestmark = pytest.mark.asyncio


async def test_get_all_roles_wo_access_401(make_get_request):
    status, response = await make_get_request(GENERAL_ROLE_ENDPOINT)

    assert status == HTTPStatus.UNAUTHORIZED
    assert response["detail"] == "В cookies отсутствует access token"


async def test_get_all_roles_w_wrong_role_403(access_token_unknown_role, client_session):
    client_session.cookie_jar.update_cookies({"access_token": access_token_unknown_role})

    async with client_session.get(GENERAL_ROLE_URL) as raw_response:
        response = await raw_response.json()

        assert raw_response.status == HTTPStatus.FORBIDDEN
        assert response["detail"] == "Нет прав для совершения действия"


async def test_get_all_roles_success_200(access_token_admin, client_session):
    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    async with client_session.get(GENERAL_ROLE_URL) as raw_response:
        response = await raw_response.json()

        assert raw_response.status == HTTPStatus.OK
        assert len(response) == 3
        assert response[0]["name"] == "admin"
        assert response[1]["name"] == "general"
        assert response[2]["name"] == "subscriber"


async def test_role_creating_w_already_existing_name(
        access_token_admin, client_session,
):
    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    params = {"role_name": "admin"}

    async with client_session.post(GENERAL_ROLE_URL, params=params) as raw_response:
        response = await raw_response.json()

        assert raw_response.status == 400
        assert response["detail"] == (f"Роль с названием '{params['role_name']}' "
                                      f"уже существует")


async def test_role_creating_success(access_token_admin, client_session):
    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    params = {"role_name": "new_role"}

    async with client_session.post(GENERAL_ROLE_URL, params=params) as raw_response:
        response = await raw_response.json()

        assert raw_response.status == 201
        assert "id" in response
        assert response["name"] == "new_role"
        assert isinstance(response["created_at"], str)
        assert response["updated_at"] is None

    await client_session.delete(GENERAL_ROLE_URL, params={"role_id": response["id"]})


async def test_role_updating_not_found(access_token_admin, client_session):
    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    non_existent_role_name = "old_role_name"
    params = {"new_role_name": "some_role_for_updating"}

    async with client_session.patch(
            GENERAL_ROLE_URL + f"/{non_existent_role_name}", params=params,
    ) as raw_response:
        response = await raw_response.json()

        assert raw_response.status == 404
        assert response["detail"] == f"Роли с name '{non_existent_role_name}' не существует"


async def test_role_updating_success(access_token_admin, client_session):
    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    old_role_name = "subscriber"
    params = {"new_role_name": "some_role_for_updating"}

    async with client_session.patch(
            GENERAL_ROLE_URL + f"/{old_role_name}", params=params,
    ) as raw_response:
        response = await raw_response.json()

        assert raw_response.status == 200
        assert "id" in response
        assert response["name"] == params["new_role_name"]
        assert isinstance(response["created_at"], str)
        assert isinstance(response["updated_at"], str)

    await client_session.patch(
        GENERAL_ROLE_URL + f"/{response['name']}",
        params={"new_role_name": old_role_name},
    )


async def test_role_deleting_not_found(access_token_admin, client_session):
    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    params = {"role_name": "role_name_to_delete"}

    async with client_session.delete(GENERAL_ROLE_URL, params=params) as raw_response:
        response = await raw_response.json()

        assert raw_response.status == 404
        assert response["detail"] == f"Роли с name '{params['role_name']}' не существует"


async def test_role_deleting_success(access_token_admin, client_session):
    client_session.cookie_jar.update_cookies({"access_token": access_token_admin})

    params = {"role_name": "subscriber"}

    async with client_session.delete(GENERAL_ROLE_URL, params=params) as raw_response:
        response = await raw_response.json()

        assert raw_response.status == 204
        assert response is None

    await client_session.post(GENERAL_ROLE_URL, params={"role_name": "subscriber"})
