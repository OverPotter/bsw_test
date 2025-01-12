import pytest
from fastapi.testclient import TestClient
from bet_maker_service.src.main import app as bet_maker_app
from line_provider_service.src.main import app as line_provider_app


@pytest.fixture
def bet_maker_app_client():
    return TestClient(bet_maker_app)


@pytest.fixture
def line_provider_app_client():
    return TestClient(line_provider_app)


@pytest.fixture
def mock_repository_manager(mocker):
    mock_repo_manager = mocker.MagicMock()
    mock_repo_manager.get_bet_repository.return_value.create.return_value = {
        "event_id": 5,
        "amount": 100,
    }
    return mock_repo_manager
