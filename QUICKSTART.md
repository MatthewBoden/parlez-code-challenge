# Quick Start Guide - Web Application

## Prerequisites

1. **Backend**: Python 3.11+ with dependencies installed
2. **Frontend**: Node.js 18+ and npm

## Setup Steps

### 1. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

This will install FastAPI, uvicorn, and other required packages.

### 2. Configure Environment

Make sure you have a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 3. Start the Backend API

```bash
python api_server.py
```

The API will run on `http://localhost:8000`

You can verify it's working by visiting:
- `http://localhost:8000` - API information
- `http://localhost:8000/docs` - Interactive API docs

### 4. Install Frontend Dependencies

In a new terminal:

```bash
cd frontend
npm install
```

### 5. Start the Frontend

```bash
npm run dev
```

The React app will run on `http://localhost:3000`

### 6. Open in Browser

Navigate to `http://localhost:3000` and start chatting!

## Troubleshooting

**Backend won't start:**
- Make sure you've installed all requirements: `pip install -r requirements.txt`
- Check that your `.env` file has a valid `OPENAI_API_KEY`

**Frontend can't connect:**
- Ensure the backend is running on port 8000
- Check the browser console for CORS errors
- Verify the API URL in `frontend/src/services/api.js`

**Streaming not working:**
- Check browser console for errors
- Ensure your browser supports Server-Sent Events (SSE)
- Try the non-streaming endpoint: `POST /api/chat/sync`

