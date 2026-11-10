from httpx import AsyncClient, ASGITransport
from main import app

async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get('/health')
        assert response.status_code == 200

async def test_validation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post('/chat', json={"conversation_id": 1, "message": ""})
        assert response.status_code == 422