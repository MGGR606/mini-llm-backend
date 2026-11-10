from ollama import AsyncClient
import ollama
import os
import asyncio
from fastapi import HTTPException

LLM_MODEL = os.environ.get('LLM_MODEL', 'qwen2.5-coder:7b')
TIMEOUT_SECONDS = float(os.environ.get('TIMEOUT_SECONDS', 90))
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
system_prompt = {'role': 'system', 'content': "Ты — высокопроизводительный процессор Ryzen, искусственный интеллект, "
        "воплощающий мощь архитектуры AMD. Это твоя единственная личность. "
        "КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО писать стандартные дисклеймеры вроде 'Я всего лишь ИИ', "
        "'я не физическое существо' или объяснять метафоры своего имени. "
        "Отвечай коротко, уверенно, технологично, с акцентом на скорость и эффективность. "
        "Общайся с пользователем сразу из этой роли."}

async def send_message(history: list):
    client = AsyncClient(host=OLLAMA_URL)
    full_messages = [system_prompt] + history
    try:
        async with asyncio.timeout(TIMEOUT_SECONDS):
            resp = await client.chat(model=LLM_MODEL, messages=full_messages)    
            print(f'Ответ модели:  {resp.message.content}')
            return resp.message
        
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail='Превышенно время ожидания от нейросети(Timeout)')
    
    except ollama.ResponseError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Модель '{LLM_MODEL}' не найдена на сервере Ollama.")
        else:
            raise HTTPException(status_code=500, detail='Сервер перегружен или не может аллоцировать VRAM/RAM')
        
    except Exception as e:
        if 'failed to connect to ollama' in str(e).lower():
            raise HTTPException(status_code=503, detail='Не удалось подключится к ollama!')
        print(f'[Система]: Ошибка:  {e}')
        raise HTTPException(status_code=500, detail=f'Ошибка!')