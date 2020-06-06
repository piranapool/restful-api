import pytest


BASE_API_URL = "http://127.0.0.1:5000/"


@pytest.fixture
def groups_route():
    return BASE_API_URL + "/groups"


@pytest.fixture
def users_route():
    return BASE_API_URL + "/users"
