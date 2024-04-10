import pytest

from unittest.mock import Mock
from src.test.fixtures.user_fixtures import user_fixture

@pytest.fixture
def secret_fixture(mocker):
    '''Secret key without app context'''
    mock = Mock()
    mocker.patch('src.main.controllers.auth_controller.get_secret', return_value='secret')
    return mock

@pytest.fixture
def login_user_dict_fixture():
    '''Input to login user'''
    return {
        'email': 'five@test.email',
        'password': 'very_secure_password'
    }

@pytest.fixture
def signup_user_dict_fixture():
    '''Input to sign up user'''
    return {
        'username': 'mozart55',
        'password': 'very_secure_password_2',
        'email': 'five@test.email'
    }

@pytest.fixture
def mock_get_user_email(mocker, user_fixture):
    '''Mock fetching a user from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.auth_controller.get_user_by_email', return_value=user_fixture)
    return mock

@pytest.fixture
def mock_get_user_email_empty(mocker):
    '''Mock fetching no user from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.auth_controller.get_user_by_email', return_value=None)
    return mock

@pytest.fixture
def mock_check_password(mocker):
    '''Mock password check'''
    mock = Mock()
    mocker.patch('src.main.models.user.User.authenticate', return_value=True)
    return mock

@pytest.fixture
def mock_check_password_fail(mocker):
    '''Mock password check'''
    mock = Mock()
    mocker.patch('src.main.models.user.User.authenticate', return_value=False)
    return mock
