import pytest
from unittest.mock import patch, Mock
from Movies_Apis.tasks import update_movie_rating

# Define a fixture to mock requests.get and requests.patch
@pytest.fixture
def mock_requests():
    with patch('Movies_Apis.tasks.requests') as mock_requests:
        yield mock_requests

# Test case for update_movie_rating task
def test_update_movie_rating(mock_requests):
    # Mock the response for GET request to 'http://127.0.0.1:8000/get_movie_api/'
    movies_data = [
        { 'id': 1,'rating': 5,'status': 'in_progress'},
        { 'id': 2, 'rating': 8,'status': 'in_progress'}
    ]
    mock_response_get = Mock()
    mock_response_get.status_code = 200
    mock_response_get.json.return_value = movies_data
    mock_requests.get.return_value = mock_response_get

    # Mock the response for PATCH request to 'http://127.0.0.1:8000/get_movie_api/{movie_id}/'
    mock_response_patch = Mock()
    mock_response_patch.status_code = 200
    mock_requests.patch.return_value = mock_response_patch

    # Call the update_movie_rating task
    update_movie_rating()

    # Check that GET request was made
    mock_requests.get.assert_called_once_with('http://127.0.0.1:8000/get_movie_api/')

    # Check that PATCH requests were made for 'Movie 1' and 'Movie 2'
    expected_patch_calls = [
        ((f'http://127.0.0.1:8000/get_movie_api/{movie["id"]}/',), {'json': {'rating': movie["rating"]}})
        for movie in movies_data
    ]
    actual_patch_calls = mock_requests.patch.call_args_list
    print("Expected PATCH calls:", expected_patch_calls)
    print("Actual PATCH calls:", actual_patch_calls)

    mock_requests.patch.assert_has_calls(expected_patch_calls, any_order=True)