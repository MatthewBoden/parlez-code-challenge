"""
OpenAI API client for chat completions with streaming support.
"""
import asyncio
from typing import AsyncIterator, List, Dict, Any, Optional
from openai import AsyncOpenAI
from src.config import Config


class OpenAIClient:
    """
    Client for interacting with OpenAI's Chat Completions API.
    
    Supports both streaming and non-streaming responses, with proper
    error handling and async/await patterns.
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key. If None, uses Config.OPENAI_API_KEY.
            model: Model to use. If None, uses Config.OPENAI_MODEL.
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model or Config.OPENAI_MODEL
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = True
    ) -> AsyncIterator[str]:
        """
        Send a chat completion request to OpenAI with streaming support.
        
        Args:
            messages: List of message dictionaries in OpenAI format.
            stream: Whether to stream the response. Defaults to True.
        
        Yields:
            Chunks of the assistant's response as they arrive.
        
        Raises:
            Exception: If the API request fails.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream
            )
            
            if stream:
                # Stream the response chunks
                async for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            else:
                # Return the full response
                yield response.choices[0].message.content
                
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def chat_completion_sync(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """
        Send a non-streaming chat completion request.
        
        Useful for testing or when streaming is not needed.
        
        Args:
            messages: List of message dictionaries in OpenAI format.
        
        Returns:
            Complete assistant response as a string.
        """
        full_response = ""
        async for chunk in self.chat_completion(messages, stream=False):
            full_response += chunk
        return full_response

