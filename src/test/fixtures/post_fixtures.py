import pytest

from src.main.constants import STATUS_LIVE
from src.main.models.post import Post
from unittest.mock import Mock
from sqlalchemy.exc import IntegrityError
from src.test.fixtures.user_fixtures import user_fixture

### POST ###
@pytest.fixture
def post_fixture(user_fixture):
    '''Basic post for testing'''
    return Post(
        id=7,
        title='My Post Title',
        author_id=user_fixture.id,
        content='Exciting blog content',
        status=STATUS_LIVE    
    )

@pytest.fixture
def create_post_dict_fixture():
    '''Input to create new post'''
    return {
        'title': 'My Post Title',
        'content': 'Exciting blog content'
    }

@pytest.fixture
def edit_post_dict_fixture():
    '''Input to edit post info'''
    return {
        'title': 'New Post Title',
        'content': 'Updates to my blog'
    }

@pytest.fixture
def mock_db(mocker):
    '''Mock a successful db update'''
    mock = Mock()
    mocker.patch('src.main.controllers.post_controller.update_db')
    return mock

@pytest.fixture
def mock_db_fail(mocker):
    '''Mock a failed db update'''
    mock = Mock()
    mocker.patch(
        'src.main.controllers.post_controller.update_db', 
        side_effect=Exception('Mocked error')
    )
    return mock

@pytest.fixture
def mock_db_conflict(mocker):
    '''Mock a db conflict'''
    mock = Mock()
    mocker.patch(
        'src.main.controllers.post_controller.update_db', 
        side_effect=IntegrityError('Conflict', None, None)
    )
    return mock

@pytest.fixture
def mock_get_post(mocker, post_fixture):
    '''Mock fetching a post from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.post_controller.get_post_by_id', return_value=post_fixture)
    return mock

@pytest.fixture
def mock_get_post_fail(mocker):
    '''Mock an error fetching a post from db'''
    mock = Mock()
    mocker.patch(
        'src.main.controllers.post_controller.get_post_by_id',
        side_effect=Exception('Mocked error')
    )
    return mock

@pytest.fixture
def mock_get_post_empty(mocker):
    '''Mock fetching no post from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.post_controller.get_post_by_id', return_value=None)
    return mock

@pytest.fixture
def mock_get_posts(mocker, post_fixture):
    '''Mock fetching posts from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.post_controller.get_posts', return_value=[post_fixture])
    return mock

@pytest.fixture
def mock_get_posts_empty(mocker):
    '''Mock fetching no posts from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.post_controller.get_posts', return_value=[])
    return mock

@pytest.fixture
def mock_get_user_posts(mocker, post_fixture):
    '''Mock fetching posts from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.post_controller.get_user_posts', return_value=[post_fixture])
    return mock

@pytest.fixture
def mock_get_user_posts_empty(mocker):
    '''Mock fetching no posts from db'''
    mock = Mock()
    mocker.patch('src.main.controllers.post_controller.get_user_posts', return_value=[])
    return mock

@pytest.fixture
def mock_get_user_posts_fail(mocker):
    '''Mock an error fetching a post from db'''
    mock = Mock()
    mocker.patch(
        'src.main.controllers.post_controller.get_user_posts',
        side_effect=Exception('Mocked error')
    )
    return mock

@pytest.fixture
def mock_cache(mocker):
    '''Mock caching functionality'''
    mock = Mock()
    mocker.patch('src.main.controllers.post_controller.cache')
    return mock
