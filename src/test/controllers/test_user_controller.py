import pytest

from src.main.controllers.user_controller import (
    create_user_response,
    delete_user_response,
    get_user_response,
    get_users_response,
    update_user_response
)
from src.test.fixtures.user_fixtures import (
    create_user_dict_fixture,
    edit_user_dict_fixture,
    mock_db,
    mock_db_conflict,
    mock_db_fail,
    mock_get_user,
    mock_get_user_empty,
    mock_get_user_fail,
    mock_get_users,
    mock_get_users_empty,
    user_fixture
)

# CREATE USER
def test_create_user_response_success(mock_db, create_user_dict_fixture, user_fixture):
    response = create_user_response(create_user_dict_fixture)
    assert response[1] == 201
    assert response[0].username == user_fixture.username

def test_create_user_response_conflict(mock_db_conflict, create_user_dict_fixture):
    with pytest.raises(Exception) as e:
        create_user_response(create_user_dict_fixture)
    assert e.value.code == 409
    assert e.value.description == 'Database conflict.'

def test_create_user_response_exception(mock_db_fail, create_user_dict_fixture):
    with pytest.raises(Exception) as e:
        create_user_response(create_user_dict_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

## GET USER
def test_get_user_response_success(mock_get_user, user_fixture):
    response = get_user_response(user_fixture.id)
    assert response[1] == 200
    assert response[0].username == user_fixture.username

def test_get_user_response_not_found(mock_get_user_empty, user_fixture):
    with pytest.raises(Exception) as e:
        get_user_response(user_fixture.id)
    assert e.value.code == 404
    assert e.value.description == 'User not found.'

def test_get_user_response_exception(mock_get_user_fail, user_fixture):
    with pytest.raises(Exception) as e:
        get_user_response(user_fixture.id)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

## GET USERS
def test_get_users_response_success(mock_get_users, user_fixture):
    response = get_users_response()
    assert response[1] == 200
    assert response[0][0].username == user_fixture.username

def test_get_users_response_not_found(mock_get_users_empty):
    response = get_users_response()
    assert response[1] == 204
    assert response[0] == []

def test_get_users_response_exception(mock_get_user_fail):
    with pytest.raises(Exception) as e:
        get_users_response()
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

## UPDATE USER
def test_update_user_response_success(
        mock_get_user,
        mock_db,
        edit_user_dict_fixture,
        user_fixture):
    response = update_user_response(user_fixture.id, edit_user_dict_fixture, user_fixture)
    assert response[1] == 201
    assert response[0].username == user_fixture.username

def test_update_user_response_unauthorized(edit_user_dict_fixture, user_fixture):
    with pytest.raises(Exception) as e:
        update_user_response(user_fixture.id + 1, edit_user_dict_fixture, user_fixture)
    assert e.value.code == 401
    assert e.value.description == 'Unauthorized.'

def test_update_user_response_not_found(
        mock_get_user_empty,
        edit_user_dict_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        update_user_response(user_fixture.id, edit_user_dict_fixture, user_fixture)
    assert e.value.code == 404
    assert e.value.description == 'User not found.'

def test_update_user_response_conflict(
        mock_get_user,
        mock_db_conflict,
        edit_user_dict_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        update_user_response(user_fixture.id, edit_user_dict_fixture, user_fixture)
    assert e.value.code == 409
    assert e.value.description == 'Database conflict.'

def test_update_user_response_exception(
        mock_get_user_fail,
        edit_user_dict_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        update_user_response(user_fixture.id, edit_user_dict_fixture, user_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

## DELETE USER
def test_delete_user_response_success(mock_get_user, mock_db, user_fixture):
    response = delete_user_response(user_fixture.id, user_fixture)
    assert response[1] == 204
    assert response[0] == 'User successfully deleted.'

def test_delete_user_response_unauthorized(user_fixture):
    with pytest.raises(Exception) as e:
        delete_user_response(user_fixture.id + 1, user_fixture)
    assert e.value.code == 401
    assert e.value.description == 'Unauthorized.'

def test_delete_user_response_not_found(mock_get_user_empty, user_fixture):
    with pytest.raises(Exception) as e:
        delete_user_response(user_fixture.id, user_fixture)
    assert e.value.code == 404
    assert e.value.description == 'User not found.'

def test_delete_user_response_exception(mock_get_user_fail, user_fixture):
    with pytest.raises(Exception) as e:
        delete_user_response(user_fixture.id, user_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

def test_delete_user_response_db_exception(
        mock_get_user,
        mock_db_fail,
        user_fixture):
    with pytest.raises(Exception) as e:
        delete_user_response(user_fixture.id, user_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'
