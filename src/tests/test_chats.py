from httpx import AsyncClient, ASGITransport
import main as main
from main import app
import asyncio
import sys
import pytest

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.mark.asyncio
async def test_send_message(mocker):
    mock_client_class = mocker.patch('modules.ollama.AsyncClient')

    mock_response = mocker.MagicMock()
    mock_message = mocker.MagicMock()
    mock_message.role = 'assistant'
    mock_message.content = 'Привет! Чем могу помочь?'

    mock_response.message = mock_message

    mock_client_class.return_value.chat = mocker.AsyncMock(
        return_value=mock_response
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/chat",
            json={"conversation_id": 1, "message": "Привет"}
        )

    assert response.status_code == 200
    assert response.json()['content'] == 'Привет! Чем могу помочь?'
    assert response.json()['role'] == 'assistant'

    mock_client_class.assert_called_once()
    mock_client_class.return_value.chat.assert_awaited_once()

async def test_history_success():
    async with AsyncClient(transport=ASGITransport(app=main.app), base_url="http://test") as ac:
        response = await ac.get("/history/1")
        assert response.status_code == 200