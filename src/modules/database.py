import psycopg
import os
from typing import Any
from fastapi import HTTPException

DATABASE_URL = os.environ.get('DATABASE_URL')

class DBConnection:
    def __init__(self):
        self.conn = None

    async def __aenter__(self):
        try:
            self.conn = await psycopg.AsyncConnection.connect(DATABASE_URL)
            return self.conn
        except psycopg.OperationalError as e:
            raise HTTPException(status_code=503, detail="База данных PostgreSQL недоступна. Проверьте подключение.")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                await self.conn.commit()
            else:
                await self.conn.rollback()
            await self.conn.close()

async def init_db():
    async with DBConnection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS chats (
                id SERIAL PRIMARY KEY)""")
            await cur.execute("""CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                chat_id INT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
                sender VARCHAR(20) NOT NULL CHECK (sender IN ('user', 'assistant', 'system')),
                content TEXT NOT NULL)""")
            
async def add_message(id: int, mes: str) -> dict[str, Any]:
    from modules.ollama import send_message 

    async with DBConnection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""INSERT INTO chats (id) VALUES (%s) ON CONFLICT (id) DO NOTHING;""", (id,))
            
            await cur.execute("""INSERT INTO messages (chat_id, sender, content) VALUES (%s, %s, %s)""", (id, 'user', mes,))
            print('Сообщение пользователя добавленно в базу данных!')
            await cur.execute("""SELECT sender, content
                        FROM messages
                        WHERE chat_id = %s
                        ORDER BY id ASC;""", (id,))
            rows = await cur.fetchall()
            
            db_messages = []
            for row in rows:
                db_messages.append({'role': row[0], 'content': row[1]})
                
            print(f'Все сообщения:  {db_messages}')
                
            message = await send_message(db_messages)
            await cur.execute("""INSERT INTO messages (chat_id, sender, content) VALUES (%s, %s, %s)""", (id, message.role, message.content,))
            print(f'Ответ ИИ добавлен в базу данных! {message.role}, {message.content}')
            return {"role": message.role, "content": message.content}
        
async def history_message(id: int):
    async with DBConnection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""SELECT sender, content
                FROM messages
                WHERE chat_id = %s
                ORDER BY id ASC;""", (id,))
            rows = await cur.fetchall()
                        
            db_messages = []
            for row in rows:
                db_messages.append({'role': row[0], 'content': row[1]})
                
            if not db_messages: 
                raise HTTPException(status_code=404, detail="Чат не найден или пуст.")
            return db_messages
        
async def delete_chat(id: int) -> str:
    async with DBConnection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id FROM chats WHERE id = %s", (id,))
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Чат для удаления не найден.")
                
            await cur.execute("""DELETE FROM chats WHERE id = %s""", (id,))
            return 'Чат успешно удален!'