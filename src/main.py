from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.schema import ChatRequest
from modules.database import add_message, history_message, delete_chat, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    
app = FastAPI(title='Mini LLM Backend', version='1.0.0', lifespan=lifespan)   

@app.get('/health')
async def check_health():
    return {'status': 'ok'}

@app.post('/chat')
async def send_message(payload: ChatRequest):
    result = await add_message(id=payload.conversation_id, mes=payload.message)
    return result

@app.get('/history/{conversation_id}')
async def get_history_dialog(conversation_id: int):
    result = await history_message(id=conversation_id)
    return result

@app.delete('/chat/del/{conversation_id}')
async def del_chat(conversation_id: int):
    result = await delete_chat(id=conversation_id)
    return result