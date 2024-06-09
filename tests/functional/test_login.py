import uuid
import random

import pytest
from werkzeug.security import generate_password_hash

LOGIN_ENDPOINT = "api/v1/login"
@pytest.mark.asyncio
async def test_user_successfull_login(add_user_to_table, make_post_request, delete_row_from_table):
    id = uuid.uuid4()
    login = "User" + str(random.randint(1, 100))
    email = "Email" + str(random.randint(1, 100))
    password = generate_password_hash("Password")
    await add_user_to_table(id=id, login=login, email=email, password=password)
    status, response = await make_post_request(LOGIN_ENDPOINT, data={"user_login": login, "password": "Password"})
    assert status == 200
    assert 'access_token' in response
    await delete_row_from_table('authentication_histories', id, "user_id")
    await delete_row_from_table('users', id)

@pytest.mark.asyncio
async def test_user_login_with_wrong_pass(add_user_to_table, make_post_request, delete_row_from_table):
    id = uuid.uuid4()
    login = "User"+str(random.randint(1, 100))
    email = "Email" + str(random.randint(1, 100))
    password = generate_password_hash("Password")
    await add_user_to_table(id=id, login=login, email=email, password=password)
    status, response = await make_post_request(LOGIN_ENDPOINT, data={"user_login": login, "password": "WrongPassword"})
    assert status == 401
    assert 'access_token' not in response
    await delete_row_from_table('authentication_histories', id, "user_id")
    await delete_row_from_table('users', id)

@pytest.mark.asyncio
async def test_user_login_with_wrong_user(add_user_to_table, make_post_request, delete_row_from_table):
    id = uuid.uuid4()
    login = "User"+str(random.randint(1, 100))
    email = "Email" + str(random.randint(1, 100))
    password = generate_password_hash("Password")
    await add_user_to_table(id=id, login=login, email=email, password=password)
    status, response = await make_post_request(LOGIN_ENDPOINT, data={"user_login": "WrongUser", "password": "Password"})
    assert status == 401
    assert 'access_token' not in response

