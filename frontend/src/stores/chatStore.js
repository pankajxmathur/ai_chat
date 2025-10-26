import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const currentThread = ref(null)
  const messages = ref([])
  const isLoading = ref(false)

  const messageCount = computed(() => messages.value.length)

  const setCurrentThread = (thread) => {
    currentThread.value = thread
  }

  const setMessages = (msgs) => {
    messages.value = msgs
  }

  const addMessage = (msg) => {
    messages.value.push(msg)
  }

  const clearMessages = () => {
    messages.value = []
  }

  return {
    currentThread,
    messages,
    isLoading,
    messageCount,
    setCurrentThread,
    setMessages,
    addMessage,
    clearMessages
  }
})
