"""
Unit tests for OpenAIClient with mocked API calls.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.openai_client import OpenAIClient


class TestOpenAIClient:
    """Test cases for OpenAIClient."""
    
    @pytest.fixture
    def mock_openai_client(self):
        """Create a mock OpenAI client."""
        with patch('src.openai_client.AsyncOpenAI') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            yield mock_client
    
    @pytest.mark.asyncio
    async def test_chat_completion_streaming(self, mock_openai_client):
        """Test streaming chat completion."""
        # Mock streaming response chunks
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = "Hello"
        
        mock_chunk2 = MagicMock()
        mock_chunk2.choices = [MagicMock()]
        mock_chunk2.choices[0].delta.content = " there"
        
        # Create async generator for streaming response
        async def mock_stream():
            yield mock_chunk1
            yield mock_chunk2
        
        # Make the mock response itself an async iterable
        mock_response = mock_stream()
        
        mock_chat = MagicMock()
        mock_chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai_client.chat = mock_chat
        
        client = OpenAIClient(api_key="test-key", model="gpt-4")
        messages = [{"role": "user", "content": "Hi"}]
        
        chunks = []
        async for chunk in client.chat_completion(messages, stream=True):
            chunks.append(chunk)
        
        assert chunks == ["Hello", " there"]
        mock_chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_chat_completion_non_streaming(self, mock_openai_client):
        """Test non-streaming chat completion."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello there!"
        
        mock_chat = MagicMock()
        mock_chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai_client.chat = mock_chat
        
        client = OpenAIClient(api_key="test-key", model="gpt-4")
        messages = [{"role": "user", "content": "Hi"}]
        
        response = await client.chat_completion_sync(messages)
        
        assert response == "Hello there!"
        mock_chat.completions.create.assert_called_once_with(
            model="gpt-4",
            messages=messages,
            stream=False
        )
    
    @pytest.mark.asyncio
    async def test_chat_completion_error_handling(self, mock_openai_client):
        """Test error handling in chat completion."""
        mock_chat = MagicMock()
        mock_chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
        mock_openai_client.chat = mock_chat
        
        client = OpenAIClient(api_key="test-key", model="gpt-4")
        messages = [{"role": "user", "content": "Hi"}]
        
        with pytest.raises(Exception) as exc_info:
            async for _ in client.chat_completion(messages):
                pass
        
        assert "OpenAI API error" in str(exc_info.value)

