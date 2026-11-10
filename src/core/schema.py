from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    conversation_id: int = Field(..., gt=0, description='ID чата должен быть положительным числом!')
    message: str = Field(..., min_length=1, description='Сообщение не может быть пустым!')