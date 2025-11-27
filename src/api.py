"""
FastAPI web API for the AI Chat Connector.
Provides REST endpoints for chat functionality with streaming support.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
import json
import asyncio
from src.config import Config
from src.conversation_manager import ConversationManager
from src.openai_client import OpenAIClient

# Initialize FastAPI app
app = FastAPI(title="AI Chat Connector API", version="1.0.0")

# Configure CORS to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global conversation manager (in production, use session management)
conversation_manager = ConversationManager()
openai_client = OpenAIClient()


class ChatMessage(BaseModel):
    """Request model for chat messages."""
    message: str
    conversation_id: Optional[str] = None  # For future session management


class ChatResponse(BaseModel):
    """Response model for chat messages."""
    response: str
    conversation_id: Optional[str] = None


class ClearResponse(BaseModel):
    """Response model for clear conversation."""
    message: str
    success: bool


class HistoryResponse(BaseModel):
    """Response model for conversation history."""
    messages: List[Dict[str, str]]
    conversation_length: int


@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup."""
    try:
        Config.validate()
    except ValueError as e:
        print(f"Warning: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Chat Connector API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/chat": "Send a chat message and get streaming response",
            "POST /api/chat/sync": "Send a chat message and get complete response",
            "POST /api/chat/clear": "Clear conversation history",
            "GET /api/chat/history": "Get conversation history"
        }
    }


@app.post("/api/chat")
async def chat_stream(message: ChatMessage):
    """
    Send a chat message and receive a streaming response.
    Uses Server-Sent Events (SSE) for real-time streaming.
    """
    if not message.message or not message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Add user message to conversation
    conversation_manager.add_user_message(message.message.strip())
    
    async def generate_stream():
        """Generator function for streaming response."""
        try:
            full_response = ""
            messages = conversation_manager.get_messages()
            
            # Get streaming response from OpenAI
            async for chunk in openai_client.chat_completion(messages, stream=True):
                full_response += chunk
                # Send chunk as SSE formatted data
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
            
            # Add assistant response to conversation history
            conversation_manager.add_assistant_message(full_response)
            
            # Send final message indicating completion
            yield f"data: {json.dumps({'chunk': '', 'done': True, 'full_response': full_response})}\n\n"
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            yield f"data: {json.dumps({'error': error_msg, 'done': True})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable buffering in nginx
        }
    )


@app.post("/api/chat/sync", response_model=ChatResponse)
async def chat_sync(message: ChatMessage):
    """
    Send a chat message and receive a complete response (non-streaming).
    Useful for testing or when streaming is not needed.
    """
    if not message.message or not message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Add user message to conversation
        conversation_manager.add_user_message(message.message.strip())
        
        # Get complete response from OpenAI
        messages = conversation_manager.get_messages()
        response = await openai_client.chat_completion_sync(messages)
        
        # Add assistant response to conversation history
        conversation_manager.add_assistant_message(response)
        
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.post("/api/chat/clear", response_model=ClearResponse)
async def clear_conversation():
    """Clear the conversation history (keeps system message)."""
    try:
        conversation_manager.clear()
        return ClearResponse(
            message="Conversation history cleared successfully",
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing conversation: {str(e)}")


@app.get("/api/chat/history", response_model=HistoryResponse)
async def get_history():
    """Get the current conversation history."""
    try:
        messages = conversation_manager.get_messages()
        return HistoryResponse(
            messages=messages,
            conversation_length=conversation_manager.get_conversation_length()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api_key_configured": bool(Config.OPENAI_API_KEY),
        "model": Config.OPENAI_MODEL
    }

