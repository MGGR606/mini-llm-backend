# Mini LLM Backend

A lightweight asynchronous backend for interacting with locally hosted Large Language Models (LLMs) through [Ollama](https://ollama.com/).

The application uses FastAPI to expose a REST API, PostgreSQL to store conversations and message history, and Ollama to generate AI responses.

## Features

- **LLM Integration** — asynchronous communication with locally hosted models through Ollama.
- **Conversation Management** — automatically create conversations when sending messages.
- **Message History** — store and retrieve conversation history from PostgreSQL.
- **Chat Deletion** — delete conversations and their associated messages.
- **Input Validation** — validate incoming requests using Pydantic.
- **Error Handling** — handle database connection errors, Ollama errors, missing models, and request timeouts.
- **Asynchronous Architecture** — use asynchronous operations for database access and LLM requests.
- **Automated Tests** — API, chat, and Ollama-related tests using pytest.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| FastAPI | REST API framework |
| Pydantic | Request validation |
| PostgreSQL | Database |
| Psycopg 3 | Asynchronous PostgreSQL driver |
| Ollama | Local LLM inference |
| HTTPX | Asynchronous HTTP client for API testing |
| pytest | Testing framework |
| pytest-asyncio | Asynchronous test support |
| pytest-mock | Mocking dependencies in tests |
| python-dotenv | Environment variable management |

## Project Structure

```text
Mini_LLM_Backend/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── schema.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── ollama.py
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_chats.py
│   │   └── test_ollama.py
│   ├── __init__.py
│   ├── main.py
│   └── pytest.ini
├── .env.example
├── .gitignore
└── requirements.txt
```

## Requirements

Before running the application, make sure you have installed:

- Python 3.12 or newer
- PostgreSQL
- Ollama
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Mini_LLM_Backend.git
cd Mini_LLM_Backend
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## Configuration

### 1. Create the environment file

Copy `.env.example` and rename the copy to `.env`.

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

### 2. Configure environment variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/database
OLLAMA_URL=http://localhost:11434
LLM_MODEL=qwen2.5-coder:7b
TIMEOUT_SECONDS=30.0
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `OLLAMA_URL` | Ollama server address |
| `LLM_MODEL` | Model used to generate responses |
| `TIMEOUT_SECONDS` | Maximum time allowed for an LLM request |

Make sure the PostgreSQL database specified in `DATABASE_URL` already exists.

The application automatically creates the `chats` and `messages` tables during startup if they do not exist.

## Ollama Setup

### 1. Start Ollama

Make sure the Ollama service is running.

### 2. Download the model

```bash
ollama pull qwen2.5-coder:7b
```

You can use another locally available Ollama model by changing `LLM_MODEL` in `.env`.

## Running the Application

From the project root, activate the virtual environment and navigate to the `src` directory:

**Windows (PowerShell):**

```powershell
cd src
uvicorn main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API availability |
| POST | `/chat` | Send a message and receive an AI response |
| GET | `/history/{conversation_id}` | Retrieve conversation history |
| DELETE | `/chat/del/{conversation_id}` | Delete a conversation |

### 1. Health Check

**GET** `/health`

Checks whether the API is responding.

Example response:

```json
{
  "status": "ok"
}
```

### 2. Send a Message

**POST** `/chat`

Request body:

```json
{
  "conversation_id": 1,
  "message": "Hello! Tell me about Python."
}
```

Example response:

```json
{
  "role": "assistant",
  "content": "Python is a high-level programming language..."
}
```

The application stores the user's message, sends the conversation history to Ollama, stores the generated response, and returns it to the client.

### 3. Retrieve Conversation History

**GET** `/history/{conversation_id}`

Example:

```text
GET /history/1
```

Returns the messages associated with the specified conversation.

Example response:

```json
[
  {
    "role": "user",
    "content": "Hello!"
  },
  {
    "role": "assistant",
    "content": "Hello! How can I help you?"
  }
]
```

### 4. Delete a Conversation

**DELETE** `/chat/del/{conversation_id}`

Example:

```text
DELETE /chat/del/1
```

Deletes the specified conversation and its associated messages.

## Running Tests

Make sure PostgreSQL is running and the `.env` file is configured.

From the project root, navigate to `src`:

```powershell
cd src
pytest -v
```

The test suite covers:

- Health endpoint.
- Request validation.
- Message submission and mocked LLM responses.
- Conversation history retrieval.
- Handling of an unavailable Ollama model.

**Note:** Tests use the configured PostgreSQL database. The Ollama error-handling test also communicates with the actual Ollama server. Make sure these services are available before running the complete test suite.

## Current Limitations

This project is an educational MVP and a foundation for further backend development.

Current limitations include:

- No authentication or user management.
- No rate limiting.
- No production-grade database connection pooling.
- No database migration management.
- No dedicated service layer for business logic.
- No conversation pagination.

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.