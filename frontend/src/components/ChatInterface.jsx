import React, { useState, useRef, useEffect } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import { sendMessage, clearConversation } from '../services/api'
import './ChatInterface.css'

function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim() || isLoading) return

    // Add user message immediately
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: messageText.trim(),
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setError(null)

    // Create placeholder for assistant response
    const assistantMessageId = Date.now() + 1
    const assistantMessage = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true
    }
    setMessages(prev => [...prev, assistantMessage])

    try {
      await sendMessage(messageText.trim(), (chunk) => {
        // Update streaming message
        setMessages(prev => prev.map(msg => 
          msg.id === assistantMessageId
            ? { ...msg, content: msg.content + chunk, isStreaming: true }
            : msg
        ))
      }, (fullResponse) => {
        // Mark streaming as complete
        setMessages(prev => prev.map(msg => 
          msg.id === assistantMessageId
            ? { ...msg, content: fullResponse, isStreaming: false }
            : msg
        ))
      })
    } catch (err) {
      setError(err.message || 'Failed to send message')
      // Remove the assistant message on error
      setMessages(prev => prev.filter(msg => msg.id !== assistantMessageId))
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearConversation = async () => {
    if (!window.confirm('Are you sure you want to clear the conversation history?')) {
      return
    }

    try {
      await clearConversation()
      setMessages([])
      setError(null)
    } catch (err) {
      setError(err.message || 'Failed to clear conversation')
    }
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="header-content">
          <div className="header-text">
            <h1>AI Chat Connector</h1>
          </div>
        </div>
        <button 
          className="clear-button"
          onClick={handleClearConversation}
          disabled={messages.length === 0}
        >
          Clear Conversation
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      <MessageList messages={messages} />
      <div ref={messagesEndRef} />

      <MessageInput 
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  )
}

export default ChatInterface

