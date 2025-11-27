import React from 'react'
import Message from './Message'
import './MessageList.css'

function MessageList({ messages }) {
  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h2>Start a conversation</h2>
          <p>Type a message below to begin chatting with the AI assistant.</p>
        </div>
      ) : (
        messages.map((message) => (
          <Message key={message.id} message={message} />
        ))
      )}
    </div>
  )
}

export default MessageList

