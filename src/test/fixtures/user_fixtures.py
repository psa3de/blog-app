import pytest
from src.main.constants import STATUS_ACTIVE
from src.main.models.user import User
from unittest.mock import Mock
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def user_fixture():
    '''Basic user for testing'''
    return User(
        id=5,
        public_id='jwt_5',
        email='five@test.email',
        admin=False,
        username='mozart5',
        status=STATUS_ACTIVE    
    )

@pytest.fixture
def create_user_dict_fixture():
    '''Input to create new user'''
    return {
        'username': 'mozart5',
        'password': 'very_secure_password',
        'email': 'five@test.email'
    }

@pytest.fixture
def edit_user_dict_fixture():
    '''Input to edit user info'''
    return {
        'username': 'mozart55',
        'password': 'very_secure_password_2'
    }

@pytest.fixture
def mock_db(mocker):
    '''Mock a successful db update'''
    mock = Mock()
    mocker.patch('src.main.controllers.user_controller.update_db')
    return mock

@pytest.fixture
def mock_db_fail(mocker):
    '''Mock a failed db update'''
    mock = Mock()
    mocker.patch(
        'src.main.controllers.user_controller.update_db', 
        side_effect=Exception('Mocked error')
    )
    return mock

@pytest.fixture
def mock_db_conflict(mocker):
    '''Mock a db conflict'''
    mock = Mock()
    mocker.patch(
        'src.main.controllers.user_controller.update_db', 
        side_effect=IntegrityError('Conflict', None, None)
    )
    return mock

@pytest.fixture
def mock_get_user(mocker, user_fixture):
    '''Mock fetching a user from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.user_controller.get_user_by_id', return_value=user_fixture)
    return mock

@pytest.fixture
def mock_get_user_fail(mocker):
    '''Mock an error fetching a user from db'''
    mock = Mock()
    mocker.patch(
        'src.main.controllers.user_controller.get_user_by_id',
        side_effect=Exception('Mocked error')
    )
    return mock

@pytest.fixture
def mock_get_user_empty(mocker):
    '''Mock fetching no user from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.user_controller.get_user_by_id', return_value=None)
    return mock

@pytest.fixture
def mock_get_users(mocker, user_fixture):
    '''Mock fetching users from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.user_controller.get_users', return_value=[user_fixture])
    return mock

@pytest.fixture
def mock_get_users_empty(mocker):
    '''Mock fetching no users from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.user_controller.get_users', return_value=[])
    return mock
