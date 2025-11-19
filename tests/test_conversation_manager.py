"""
Unit tests for ConversationManager.
"""
import pytest
from src.conversation_manager import ConversationManager


class TestConversationManager:
    """Test cases for ConversationManager."""
    
    def test_init_with_default_system_message(self):
        """Test initialization with default system message."""
        manager = ConversationManager()
        assert len(manager.messages) == 1
        assert manager.messages[0]["role"] == "system"
        assert "helpful" in manager.messages[0]["content"].lower()
    
    def test_init_with_custom_system_message(self):
        """Test initialization with custom system message."""
        custom_message = "You are a coding assistant."
        manager = ConversationManager(system_message=custom_message)
        assert manager.messages[0]["content"] == custom_message
    
    def test_add_user_message(self):
        """Test adding user messages."""
        manager = ConversationManager()
        manager.add_user_message("Hello")
        
        assert len(manager.messages) == 2
        assert manager.messages[1]["role"] == "user"
        assert manager.messages[1]["content"] == "Hello"
    
    def test_add_assistant_message(self):
        """Test adding assistant messages."""
        manager = ConversationManager()
        manager.add_assistant_message("Hi there!")
        
        assert len(manager.messages) == 2
        assert manager.messages[1]["role"] == "assistant"
        assert manager.messages[1]["content"] == "Hi there!"
    
    def test_conversation_history(self):
        """Test maintaining conversation history."""
        manager = ConversationManager()
        manager.add_user_message("What is Python?")
        manager.add_assistant_message("Python is a programming language.")
        manager.add_user_message("Tell me more.")
        
        messages = manager.get_messages()
        assert len(messages) == 4
        assert messages[1]["role"] == "user"
        assert messages[2]["role"] == "assistant"
        assert messages[3]["role"] == "user"
    
    def test_clear_conversation(self):
        """Test clearing conversation while keeping system message."""
        manager = ConversationManager()
        manager.add_user_message("Hello")
        manager.add_assistant_message("Hi!")
        manager.clear()
        
        assert len(manager.messages) == 1
        assert manager.messages[0]["role"] == "system"
    
    def test_get_conversation_length(self):
        """Test getting conversation length excluding system message."""
        manager = ConversationManager()
        assert manager.get_conversation_length() == 0
        
        manager.add_user_message("Hello")
        assert manager.get_conversation_length() == 1
        
        manager.add_assistant_message("Hi!")
        assert manager.get_conversation_length() == 2

