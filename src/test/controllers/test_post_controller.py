import pytest

from src.main.controllers.post_controller import (
    create_post_response,
    delete_post_response,
    get_post_response,
    get_posts_response,
    get_user_posts_response,
    update_post_response
)
from src.test.fixtures.post_fixtures import (
    create_post_dict_fixture,
    edit_post_dict_fixture,
    mock_db,
    mock_db_fail,
    mock_db_conflict,
    mock_get_post,
    mock_get_post_empty,
    mock_get_post_fail,
    mock_get_posts,
    mock_get_posts_empty,
    mock_get_user_posts,
    mock_get_user_posts_empty,
    mock_get_user_posts_fail,
    mock_cache,
    post_fixture
)
from src.test.fixtures.user_fixtures import user_fixture

# CREATE POST
def test_create_post_response_success(
        mock_db,
        mock_cache,
        post_fixture,
        create_post_dict_fixture,
        user_fixture):
    response = create_post_response(create_post_dict_fixture, user_fixture)
    assert response[1] == 201
    assert response[0].title == post_fixture.title

def test_create_post_response_unauthorized(create_post_dict_fixture):
    with pytest.raises(Exception) as e:
        create_post_response(create_post_dict_fixture, None)
    assert e.value.code == 401
    assert e.value.description == 'Unauthorized.'

def test_create_post_response_exception(
        mock_db_fail,
        create_post_dict_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        create_post_response(create_post_dict_fixture, user_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

# GET POST
def test_get_post_response_success(mock_get_post, post_fixture):
    response = get_post_response(post_fixture.id)
    assert response[1] == 200
    assert response[0].title == post_fixture.title

def test_get_post_response_not_found(mock_get_post_empty, post_fixture):
    with pytest.raises(Exception) as e:
        get_post_response(post_fixture.id)
    assert e.value.code == 404
    assert e.value.description == 'Post not found.'

def test_get_post_response_exception(mock_get_post_fail, post_fixture):
    with pytest.raises(Exception) as e:
        get_post_response(post_fixture.id)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

# GET POSTS
def test_get_posts_response_success(mock_get_posts, post_fixture):
    response = get_posts_response()
    assert response[1] == 200
    assert response[0][0].title == post_fixture.title

def test_get_posts_response_not_found(mock_get_posts_empty):
    response = get_posts_response()
    assert response[1] == 204
    assert response[0] == []

def test_get_posts_response_exception(mock_get_post_fail):
    with pytest.raises(Exception) as e:
        get_posts_response()
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

# GET USER POSTS
def test_get_user_posts_response_success(mock_get_user_posts, post_fixture, user_fixture):
    response = get_user_posts_response(user_fixture.id)
    assert response[1] == 200
    assert response[0][0].title == post_fixture.title

def test_get_user_posts_response_not_found(mock_get_user_posts_empty, user_fixture):
    response = get_user_posts_response(user_fixture.id)
    assert response[1] == 204
    assert response[0] == []

def test_get_user_posts_response_exception(mock_get_user_posts_fail, user_fixture):
    with pytest.raises(Exception) as e:
        get_user_posts_response(user_fixture.id)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

# UPDATE POST
def test_update_post_response_success(
        mock_get_post,
        mock_db,
        mock_cache,
        post_fixture,
        edit_post_dict_fixture,
        user_fixture):
    response = update_post_response(
        post_fixture.id,
        edit_post_dict_fixture,
        user_fixture)
    assert response[1] == 201
    assert response[0].title == post_fixture.title

def test_update_post_response_unauthorized(
        mock_get_post,
        post_fixture,
        edit_post_dict_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        post_fixture.author_id += 1
        update_post_response(post_fixture.id, edit_post_dict_fixture, user_fixture)
    assert e.value.code == 401
    assert e.value.description == 'Unauthorized.'

def test_update_post_response_not_found(
        mock_get_post_empty,
        post_fixture,
        edit_post_dict_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        update_post_response(post_fixture.id, edit_post_dict_fixture, user_fixture)
    assert e.value.code == 404
    assert e.value.description == 'Post not found.'

def test_update_post_response_conflict(
        mock_get_post,
        mock_db_conflict,
        post_fixture,
        edit_post_dict_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        update_post_response(post_fixture.id, edit_post_dict_fixture, user_fixture)
    assert e.value.code == 409
    assert e.value.description == 'Database conflict.'

def test_update_post_response_exception(
        mock_get_post_fail,
        post_fixture,
        edit_post_dict_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        update_post_response(post_fixture.id, edit_post_dict_fixture, user_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

# DELETE POST
def test_delete_post_response_success(
        mock_get_post,
        mock_db,
        mock_cache,
        post_fixture,
        user_fixture):
    response = delete_post_response(post_fixture.id, user_fixture)
    assert response[1] == 204
    assert response[0] == 'Post successfully deleted.'

def test_delete_post_response_unauthorized(mock_get_post, post_fixture, user_fixture):
    with pytest.raises(Exception) as e:
        post_fixture.author_id += 1
        delete_post_response(post_fixture.id, user_fixture)
    assert e.value.code == 401
    assert e.value.description == 'Unauthorized.'

def test_delete_post_response_not_found(
        mock_get_post_empty,
        post_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        delete_post_response(post_fixture.id, user_fixture)
    assert e.value.code == 404
    assert e.value.description == 'Post not found.'

def test_delete_post_response_exception(
        mock_get_post_fail,
        post_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        delete_post_response(post_fixture.id, user_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'

def test_delete_post_response_db_exception(
        mock_get_post,
        mock_db_fail,
        post_fixture,
        user_fixture):
    with pytest.raises(Exception) as e:
        delete_post_response(post_fixture.id, user_fixture)
    assert e.value.code == 500
    assert e.value.description == 'An error occurred.'
