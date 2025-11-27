# AI Chat Connector - OpenAI

A clean, async Python application that connects to OpenAI's API and provides a simple chat interface with conversation memory and streaming responses. Available as both a **command-line application** and a **web application** with React.js frontend.

## Features

-  **Streaming Responses**: Real-time display of AI responses as they're generated
-  **Conversation Memory**: Maintains full conversation history across multiple interactions
-  **Async/Await**: Built with Python async/await for efficient I/O handling
-  **Environment Variables**: Secure API key management via `.env` file
-  **Unit Tests**: Comprehensive test coverage for core components
-  **Docker Support**: Easy containerization with included Dockerfile
-  **Web Application**: React.js frontend with FastAPI backend
-  **Clean Architecture**: Well-structured, commented code

## Requirements

### Backend
- Python 3.11 or higher
- OpenAI API key
- pip (Python package manager)

### Frontend (for web application)
- Node.js 18+ and npm (or yarn/pnpm)

## Installation

### 1. Clone or download this repository

```bash
cd parlez-code-challenge
```

### 2. Create a virtual environment (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```bash
# On Windows (PowerShell)
New-Item -Path .env -ItemType File

# On macOS/Linux
touch .env
```

Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

**Note**: Replace `your_openai_api_key_here` with your actual OpenAI API key. You can get one from [OpenAI's website](https://platform.openai.com/api-keys).

The `OPENAI_MODEL` is optional and defaults to `gpt-4o-mini`. You can change it to other models like `gpt-4`, `gpt-3.5-turbo`, etc.

## How to Run

### Command-Line Application

#### Option 1: Run directly with Python

```bash
python main.py
```

#### Option 2: Run as a module

```bash
python -m src.chat_app
```

### Web Application

The web application consists of a FastAPI backend and a React.js frontend.

#### Step 1: Start the Backend API Server

In the project root directory:

```bash
# Make sure you have installed dependencies
pip install -r requirements.txt

# Start the API server
python api_server.py
```

Or using uvicorn directly:

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

You can test the API at:
- `http://localhost:8000` - API root with endpoint information
- `http://localhost:8000/api/health` - Health check endpoint
- `http://localhost:8000/docs` - Interactive API documentation (Swagger UI)

#### Step 2: Start the Frontend

In a new terminal, navigate to the frontend directory:

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

The React app will be available at `http://localhost:3000`

#### Step 3: Use the Web Application

1. Open your browser and navigate to `http://localhost:3000`
2. Start chatting! The interface supports:
   - Real-time streaming responses
   - Conversation history
   - Clear conversation button
   - Modern, responsive UI

**Note**: Make sure the backend API server is running before starting the frontend.

## Usage

Once the application starts, you'll see a welcome message and can begin chatting:

```
============================================================
AI Chat Connector - OpenAI
============================================================

Commands:
  Type your message and press Enter to chat
  Type '/clear' to clear conversation history
  Type '/quit' or '/exit' to exit
  Type '/help' to show this help message

------------------------------------------------------------

You: Hello, how are you?
```

The assistant's response will stream in real-time as it's generated.

### Available Commands

- `/clear` - Clear the conversation history (keeps system message)
- `/quit` or `/exit` - Exit the application
- `/help` - Show the help message

## Running Tests

To run the unit tests:

```bash
pytest tests/
```

To run with verbose output:

```bash
pytest tests/ -v
```

To run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Docker

### Build the Docker image

```bash
docker build -t ai-chat-connector .
```

### Run with Docker

You'll need to pass your API key as an environment variable:

```bash
docker run -it --env OPENAI_API_KEY=your_openai_api_key_here ai-chat-connector
```

Or use a `.env` file with Docker Compose (create `docker-compose.yml`):

```yaml
version: '3.8'
services:
  chat:
    build: .
    env_file:
      - .env
    stdin_open: true
    tty: true
```

Then run:

```bash
docker-compose up
```

## Project Structure

```
parlez-code-challenge/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration and environment variables
│   ├── conversation_manager.py # Conversation memory management
│   ├── openai_client.py       # OpenAI API client with streaming
│   ├── chat_app.py            # Main CLI application logic
│   └── api.py                 # FastAPI web API endpoints
├── frontend/                  # React.js frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── MessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   └── MessageInput.jsx
│   │   ├── services/          # API service layer
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── tests/
│   ├── __init__.py
│   ├── test_conversation_manager.py
│   └── test_openai_client.py
├── main.py                    # CLI entry point
├── api_server.py              # Web API server entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                 # Docker configuration
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Code Quality

- **Clean Code**: Well-structured, modular design with separation of concerns
- **Comments**: Comprehensive docstrings and inline comments
- **Type Hints**: Python type hints for better code clarity
- **Error Handling**: Proper exception handling throughout
- **Async Patterns**: Proper use of async/await for I/O operations

## Technical Details

### Streaming Implementation

The application uses OpenAI's streaming API to display responses in real-time. The `OpenAIClient.chat_completion()` method yields chunks as they arrive.

- **CLI**: `ChatApp.display_streaming_response()` prints chunks immediately to the terminal
- **Web**: The FastAPI backend streams chunks via Server-Sent Events (SSE), and the React frontend updates the UI in real-time

### Conversation Memory

The `ConversationManager` class maintains a list of messages in OpenAI's format:
- System message (set at initialization)
- User messages
- Assistant messages

This history is sent with each API request to maintain context.

### Async Architecture

The application uses Python's `asyncio` for:
- Non-blocking user input (CLI via `run_in_executor`)
- Streaming API responses
- Efficient I/O handling
- FastAPI async endpoints for the web API

### Web API Endpoints

- `POST /api/chat` - Send a message and receive streaming response (SSE)
- `POST /api/chat/sync` - Send a message and receive complete response (non-streaming)
- `POST /api/chat/clear` - Clear conversation history
- `GET /api/chat/history` - Get conversation history
- `GET /api/health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

## Troubleshooting

### "OPENAI_API_KEY environment variable is required"

Make sure you've created a `.env` file in the root directory with your API key.

### "ModuleNotFoundError: No module named 'src'"

Make sure you're running from the project root directory, or set `PYTHONPATH`:

```bash
# Windows PowerShell
$env:PYTHONPATH="."

# macOS/Linux
export PYTHONPATH=.
```

### API Errors

If you encounter API errors:
- Verify your API key is correct
- Check your OpenAI account has sufficient credits
- Ensure the model name is valid (e.g., `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo`)

### Web Application Issues

**Frontend can't connect to backend:**
- Ensure the backend API server is running on port 8000
- Check that CORS is properly configured (should work out of the box)
- Verify the API URL in `frontend/src/services/api.js` matches your backend URL

**Streaming not working:**
- Check browser console for errors
- Ensure your browser supports Server-Sent Events (SSE)
- Verify the backend is sending proper SSE-formatted responses

## License

This project is part of a coding challenge.
