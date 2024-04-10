import pytest

from src.test.fixtures.auth_fixtures import (
    login_user_dict_fixture,
    mock_get_user_email,
    mock_get_user_email_empty,
    mock_check_password,
    mock_check_password_fail,
    secret_fixture,
    signup_user_dict_fixture
)
from src.test.fixtures.user_fixtures import (
    mock_db,
    mock_db_conflict,
    mock_db_fail,
    user_fixture
)

from src.main.controllers.auth_controller import signup_user, login_user

# LOGIN
def test_login_user_success(
        secret_fixture,
        mock_get_user_email,
        mock_check_password,
        login_user_dict_fixture):
    response = login_user(login_user_dict_fixture)
    assert response[1] == 200

def test_login_user_unauthorized():
    with pytest.raises(Exception) as e:
        login_user({})
    assert e.value.code == 401
    assert e.value.description == 'Login required.'

def test_login_user_no_user(
        secret_fixture,
        mock_get_user_email_empty,
        login_user_dict_fixture):
    with pytest.raises(Exception) as e:
        login_user(login_user_dict_fixture)
    assert e.value.code == 401
    assert e.value.description == 'User does not exist.'

def test_login_user_wrong_password(
        secret_fixture, 
        mock_get_user_email, 
        mock_check_password_fail, 
        login_user_dict_fixture):
    with pytest.raises(Exception) as e:
        login_user(login_user_dict_fixture)
    assert e.value.code == 403
    assert e.value.description == 'Wrong password.'

# SIGNUP
def test_signup_user_success(
        mock_get_user_email_empty,
        mock_db,
        signup_user_dict_fixture):
    response = signup_user(signup_user_dict_fixture)
    assert response[1] == 201
    assert response[0] == 'User successfully registered.'

def test_signup_user_exists(mock_get_user_email, signup_user_dict_fixture):
    response = signup_user(signup_user_dict_fixture)
    assert response[1] == 202
    assert response[0] == 'User already exists.'

def test_signup_user_conflict(
        mock_get_user_email_empty,
        mock_db_conflict,
        signup_user_dict_fixture):
    with pytest.raises(Exception) as e:
        signup_user(signup_user_dict_fixture)
    assert e.value.code == 409
    assert e.value.description == 'Database conflict.'

def test_signup_user_exception(
        mock_get_user_email_empty,
        mock_db_fail,
        signup_user_dict_fixture):
    with pytest.raises(Exception) as e:
        signup_user(signup_user_dict_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'
