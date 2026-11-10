from httpx import AsyncClient, ASGITransport

from main import app
from modules import ollama as olm
from modules.ollama import send_message

async def test_hacked_model(monkeypatch):
    monkeypatch.setattr(olm, "LLM_MODEL", "HACKED_MODEL")
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post('/chat', json={'conversation_id': 1, 'message': 'Привет!'})
        assert response.status_code == 404
        