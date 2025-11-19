# AI Chat Connector - OpenAI

A clean, async Python application that connects to OpenAI's API and provides a simple chat interface with conversation memory and streaming responses.

## Features

- ✅ **Streaming Responses**: Real-time display of AI responses as they're generated
- ✅ **Conversation Memory**: Maintains full conversation history across multiple interactions
- ✅ **Async/Await**: Built with Python async/await for efficient I/O handling
- ✅ **Environment Variables**: Secure API key management via `.env` file
- ✅ **Unit Tests**: Comprehensive test coverage for core components
- ✅ **Docker Support**: Easy containerization with included Dockerfile
- ✅ **Clean Architecture**: Well-structured, commented code

## Requirements

- Python 3.11 or higher
- OpenAI API key
- pip (Python package manager)

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

### Option 1: Run directly with Python

```bash
python main.py
```

### Option 2: Run as a module

```bash
python -m src.chat_app
```

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
│   └── chat_app.py            # Main application logic
├── tests/
│   ├── __init__.py
│   ├── test_conversation_manager.py
│   └── test_openai_client.py
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
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

The application uses OpenAI's streaming API to display responses in real-time. The `OpenAIClient.chat_completion()` method yields chunks as they arrive, and `ChatApp.display_streaming_response()` prints them immediately.

### Conversation Memory

The `ConversationManager` class maintains a list of messages in OpenAI's format:
- System message (set at initialization)
- User messages
- Assistant messages

This history is sent with each API request to maintain context.

### Async Architecture

The application uses Python's `asyncio` for:
- Non-blocking user input (via `run_in_executor`)
- Streaming API responses
- Efficient I/O handling

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

## License

This project is part of a coding challenge.
