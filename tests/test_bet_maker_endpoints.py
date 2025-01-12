import pytest


@pytest.mark.asyncio
async def test_create_bet(bet_maker_app_client, mock_repository_manager):
    """Тест для эндпоинта POST /bet с использованием TestClient."""
    payload = {"event_id": 5, "bet_amount": 100}

    # Настройка mock-репозитория
    mock_repository_manager.get_bet_repository.return_value.create.return_value = {
        "event_id": 5,
        "bet_amount": 100,
    }

    # Асинхронный запрос
    response = bet_maker_app_client.post("/bet", json=payload)
    assert response.status_code == 200
    bet = response.json()

    # Проверки
    assert bet["event_id"] == 1
    assert bet["bet_amount"] == 100


@pytest.mark.asyncio
async def test_get_all_bets(bet_maker_app_client):
    """Тест для эндпоинта GET /bet/ с использованием TestClient."""
    response = bet_maker_app_client.get("/bet")
    assert response.status_code == 200
    events = response.json()

    assert len(events) == 1
    assert events[0]["id"] == 1
