/**
 * API service for communicating with the backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Send a chat message and receive streaming response.
 * @param {string} message - The user's message
 * @param {function} onChunk - Callback for each chunk received
 * @param {function} onComplete - Callback when streaming is complete
 */
export async function sendMessage(message, onChunk, onComplete) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to send message')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            
            if (data.error) {
              throw new Error(data.error)
            }
            
            if (data.chunk) {
              onChunk(data.chunk)
            }
            
            if (data.done) {
              if (data.full_response) {
                onComplete(data.full_response)
              } else {
                onComplete('')
              }
              return
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e)
          }
        }
      }
    }
  } catch (error) {
    console.error('Error sending message:', error)
    throw error
  }
}

/**
 * Clear the conversation history.
 */
export async function clearConversation() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat/clear`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to clear conversation')
    }

    return await response.json()
  } catch (error) {
    console.error('Error clearing conversation:', error)
    throw error
  }
}

/**
 * Get conversation history.
 */
export async function getHistory() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat/history`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to get history')
    }

    return await response.json()
  } catch (error) {
    console.error('Error getting history:', error)
    throw error
  }
}

