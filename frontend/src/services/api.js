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
    let accumulatedResponse = ''
    let completed = false

    try {
      while (true) {
        const { done, value } = await reader.read()
        
        if (done) {
          // Stream ended - ensure completion callback is called if not already
          if (!completed) {
            completed = true
            onComplete(accumulatedResponse || '')
          }
          break
        }

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              
              if (data.error) {
                if (!completed) {
                  completed = true
                  onComplete(accumulatedResponse || '')
                }
                throw new Error(data.error)
              }
              
              if (data.chunk) {
                accumulatedResponse += data.chunk
                onChunk(data.chunk)
              }
              
              if (data.done) {
                if (!completed) {
                  completed = true
                  if (data.full_response) {
                    onComplete(data.full_response)
                  } else {
                    onComplete(accumulatedResponse || '')
                  }
                }
                return
              }
            } catch (e) {
              // If it's a JSON parse error, just skip this line
              if (e instanceof SyntaxError) {
                console.error('Error parsing SSE JSON:', e)
                continue
              }
              // If it's an actual error from server, complete and throw
              if (!completed) {
                completed = true
                onComplete(accumulatedResponse || '')
              }
              throw e
            }
          }
        }
      }
    } catch (streamError) {
      // Ensure completion callback is called even on stream errors
      if (!completed) {
        completed = true
        onComplete(accumulatedResponse || '')
      }
      throw streamError
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

