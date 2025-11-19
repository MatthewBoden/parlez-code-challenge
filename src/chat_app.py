"""
Main chat application with async input/output handling.
"""
import asyncio
import sys
from typing import Optional
from src.config import Config
from src.conversation_manager import ConversationManager
from src.openai_client import OpenAIClient


class ChatApp:
    """
    Main chat application that orchestrates user input, API calls,
    and response display with conversation memory.
    """
    
    def __init__(self):
        """Initialize the chat application."""
        Config.validate()
        self.conversation = ConversationManager()
        self.client = OpenAIClient()
        self.running = True
    
    async def get_user_input(self) -> Optional[str]:
        """
        Asynchronously get user input from stdin.
        
        Returns:
            User input string, or None if input is empty/whitespace.
        """
        loop = asyncio.get_event_loop()
        try:
            # Use input() instead of sys.stdin.readline() for better Windows compatibility
            # input() will handle the prompt and wait for user input
            user_input = await loop.run_in_executor(None, lambda: input("You: "))
            return user_input.strip() if user_input else None
        except (EOFError, KeyboardInterrupt):
            return None
    
    async def display_streaming_response(self, stream: any) -> str:
        """
        Display streaming response from OpenAI in real-time.
        
        Args:
            stream: AsyncIterator of response chunks.
        
        Returns:
            Complete accumulated response.
        """
        full_response = ""
        print("\nAssistant: ", end="", flush=True)
        
        async for chunk in stream:
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print("\n")  # New line after response
        return full_response
    
    async def process_message(self, user_input: str) -> None:
        """
        Process a user message: add to conversation, call API, display response.
        
        Args:
            user_input: The user's message.
        """
        # Add user message to conversation
        self.conversation.add_user_message(user_input)
        
        # Get streaming response from OpenAI
        try:
            stream = self.client.chat_completion(
                self.conversation.get_messages(),
                stream=True
            )
            
            # Display streaming response
            response = await self.display_streaming_response(stream)
            
            # Add assistant response to conversation history
            self.conversation.add_assistant_message(response)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n{error_msg}\n")
    
    def print_welcome(self) -> None:
        """Print welcome message and instructions."""
        print("\n" + "="*60)
        print("AI Chat Connector - OpenAI")
        print("="*60)
        print("\nCommands:")
        print("  Type your message and press Enter to chat")
        print("  Type '/clear' to clear conversation history")
        print("  Type '/history' to view conversation history")
        print("  Type '/quit' or '/exit' to exit")
        print("  Type '/help' to show this help message")
        print("\n" + "-"*60 + "\n")
    
    async def handle_command(self, command: str) -> bool:
        """
        Handle special commands.
        
        Args:
            command: The command string (without leading slash).
        
        Returns:
            True if the command should exit the app, False otherwise.
        """
        command = command.lower()
        
        if command in ['quit', 'exit']:
            print("\nGoodbye!\n")
            return True
        
        elif command == 'clear':
            self.conversation.clear()
            print("\nConversation history cleared.\n")
            return False
        
        elif command == 'help':
            self.print_welcome()
            return False
        
        elif command == 'history':
            # Show conversation history for debugging
            print("\n" + "="*60)
            print("Conversation History:")
            print("="*60)
            for i, msg in enumerate(self.conversation.get_messages()):
                role = msg["role"].upper()
                content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                print(f"\n[{i}] {role}: {content}")
            print("\n" + "="*60 + "\n")
            return False
        
        else:
            print(f"\nUnknown command: /{command}\n")
            return False
    
    async def run(self) -> None:
        """Main application loop."""
        self.print_welcome()
        
        while self.running:
            try:
                # Get user input (prompt is handled by input() function)
                user_input = await self.get_user_input()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    should_exit = await self.handle_command(user_input[1:])
                    if should_exit:
                        break
                    continue
                
                # Process regular message
                await self.process_message(user_input)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Exiting...\n")
                break
            except Exception as e:
                print(f"\nUnexpected error: {str(e)}\n")
                break


async def main():
    """Entry point for the chat application."""
    app = ChatApp()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())

