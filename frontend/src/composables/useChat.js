import { ref } from 'vue'
import apiService from '@/services/api'

export function useChat() {
  const isLoading = ref(false)
  const error = ref(null)

  const createThread = async (title) => {
    try {
      isLoading.value = true
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.create_chat_thread',
        args: { title }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getThread = async (threadId) => {
    try {
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.get_chat_thread',
        args: { thread_id: threadId }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const sendMessage = async (threadId, content) => {
    try {
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.send_message',
        args: { thread_id: threadId, content }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const listThreads = async () => {
    try {
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.list_chat_threads'
      })
      return response.message.threads
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    isLoading,
    error,
    createThread,
    getThread,
    sendMessage,
    listThreads
  }
}
