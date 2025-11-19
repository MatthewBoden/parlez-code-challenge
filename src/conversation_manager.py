"""
Conversation memory manager for maintaining chat history.
"""
from typing import List, Dict, Any


class ConversationManager:
    """
    Manages conversation history and context for the chat application.
    
    Maintains a list of messages in the format expected by OpenAI's API,
    allowing for conversation continuity across multiple interactions.
    """
    
    def __init__(self, system_message: str = None):
        """
        Initialize the conversation manager.
        
        Args:
            system_message: Optional system message to set the assistant's behavior.
                           If None, a default helpful assistant message is used.
        """
        self.messages: List[Dict[str, str]] = []
        
        if system_message:
            self.messages.append({
                "role": "system",
                "content": system_message
            })
        else:
            self.messages.append({
                "role": "system",
                "content": "You are a helpful AI assistant. You are having a conversation with a user, and you should remember and reference previous messages in this conversation. Maintain context throughout the conversation."
            })
    
    def add_user_message(self, content: str) -> None:
        """
        Add a user message to the conversation history.
        
        Args:
            content: The user's message content.
        """
        self.messages.append({
            "role": "user",
            "content": content
        })
    
    def add_assistant_message(self, content: str) -> None:
        """
        Add an assistant message to the conversation history.
        
        Args:
            content: The assistant's message content.
        """
        self.messages.append({
            "role": "assistant",
            "content": content
        })
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        Get the current conversation history.
        
        Returns:
            List of message dictionaries in OpenAI format.
        """
        return self.messages.copy()
    
    def clear(self) -> None:
        """
        Clear the conversation history (except system message).
        """
        # Keep only the system message
        system_msg = self.messages[0] if self.messages and self.messages[0]["role"] == "system" else None
        self.messages = []
        if system_msg:
            self.messages.append(system_msg)
    
    def get_conversation_length(self) -> int:
        """
        Get the number of messages in the conversation (excluding system message).
        
        Returns:
            Number of user/assistant message pairs.
        """
        return len([msg for msg in self.messages if msg["role"] != "system"])

