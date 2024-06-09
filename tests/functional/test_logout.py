import uuid
import random

import pytest
from werkzeug.security import generate_password_hash

LOGOUT_ENDPOINT = "api/v1/user/logout"
@pytest.mark.asyncio
async def test_user_logout_without_cookies(add_user_to_table, make_get_request, delete_row_from_table):
    id = uuid.uuid4()
    login = "User" + str(random.randint(1, 1000))
    email = "Email" + str(random.randint(1, 1000))
    password = generate_password_hash("Password")
    await add_user_to_table(id=id, login=login, email=email, password=password, )
    status, response = await make_get_request(LOGOUT_ENDPOINT, params={"login": login})
    assert status == 401
    await delete_row_from_table('users', id)


