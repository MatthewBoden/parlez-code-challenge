import React from 'react'
import './Message.css'

function Message({ message }) {
  const isUser = message.role === 'user'
  const isStreaming = message.isStreaming

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className="message-content">
        {message.content || (isStreaming ? '...' : '')}
        {isStreaming && (
          <span className="streaming-indicator">▋</span>
        )}
      </div>
      <div className="message-timestamp">
        {new Date(message.timestamp).toLocaleTimeString()}
      </div>
    </div>
  )
}

export default Message

