<template>
  <div class="chat-interface">
    <div class="chat-header">
      <h1>{{ currentThread?.title || 'New Chat' }}</h1>
      <button @click="createNewChat" class="btn-new">+ New Chat</button>
    </div>

    <div class="chat-content">
      <div class="messages">
        <div v-if="messages.length === 0" class="empty-state">
          <h2>How can I help you today?</h2>
          <p>Start a conversation by typing a message below.</p>
        </div>

        <div v-for="msg in messages" :key="msg.name" class="message"
             :class="msg.role">
          <div class="message-content">
            <p>{{ msg.content }}</p>
          </div>
          <div class="message-meta">
            <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
          </div>
        </div>

        <div v-if="isLoading" class="message assistant loading">
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="input-area">
      <textarea v-model="inputText"
                @keydown.enter.prevent="handleEnter"
                placeholder="Type your message..."
                rows="3"></textarea>
      <button @click="sendMessage" :disabled="isLoading || !inputText.trim()">
        Send
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useChatStore } from '@/stores/chatStore'
import { useChat } from '@/composables/useChat'

const chatStore = useChatStore()
const { createThread, getThread, sendMessage: sendChatMessage, listThreads } = useChat()

const inputText = ref('')
const isLoading = ref(false)

const currentThread = computed(() => chatStore.currentThread)
const messages = computed(() => chatStore.messages)

const createNewChat = async () => {
  try {
    const thread = await createThread('New Chat')
    chatStore.setCurrentThread(thread)
    chatStore.setMessages([])
    inputText.value = ''
  } catch (error) {
    console.error('Failed to create chat:', error)
    alert('Failed to create new chat. Please try again.')
  }
}

const sendMessage = async () => {
  if (!inputText.value.trim() || !currentThread.value) return

  try {
    isLoading.value = true
    const response = await sendChatMessage(
      currentThread.value.thread_id,
      inputText.value
    )

    // Reload thread to get updated messages
    const threadData = await getThread(currentThread.value.thread_id)
    chatStore.setMessages(threadData.messages)
    inputText.value = ''
  } catch (error) {
    console.error('Failed to send message:', error)
    alert('Failed to send message. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const handleEnter = (event) => {
  if (!event.shiftKey) {
    sendMessage()
  } else {
    // Allow newline with Shift+Enter
    return true
  }
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  try {
    const threads = await listThreads()
    if (threads.length > 0) {
      const threadData = await getThread(threads[0].thread_id)
      chatStore.setCurrentThread(threadData.thread)
      chatStore.setMessages(threadData.messages)
    } else {
      await createNewChat()
    }
  } catch (error) {
    console.error('Failed to load initial data:', error)
    // Create new chat anyway
    await createNewChat()
  }
})
</script>

<style scoped>
.chat-interface {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #fff;
}

.chat-header {
  padding: 1rem 2rem;
  border-bottom: 1px solid #e5e5e5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fafafa;
}

.chat-header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
}

.btn-new {
  padding: 0.5rem 1rem;
  background: #10a37f;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-new:hover {
  background: #0e8c6f;
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background: #ffffff;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 900px;
  margin: 0 auto;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.empty-state h2 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.message {
  padding: 1rem 1.25rem;
  border-radius: 12px;
  max-width: 80%;
  word-wrap: break-word;
}

.message.user {
  background: #10a37f;
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 4px;
}

.message.assistant {
  background: #f7f7f8;
  color: #353740;
  margin-right: auto;
  border-bottom-left-radius: 4px;
}

.message.loading {
  background: #f7f7f8;
}

.message-content p {
  margin: 0;
  line-height: 1.6;
  white-space: pre-wrap;
}

.message-meta {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  opacity: 0.7;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #666;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    opacity: 0.3;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-4px);
  }
}

.input-area {
  padding: 1rem 2rem;
  border-top: 1px solid #e5e5e5;
  display: flex;
  gap: 0.75rem;
  background: #fff;
}

textarea {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  transition: border-color 0.2s;
}

textarea:focus {
  outline: none;
  border-color: #10a37f;
}

.input-area button {
  padding: 0.75rem 1.5rem;
  background: #10a37f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  transition: background 0.2s;
}

.input-area button:hover:not(:disabled) {
  background: #0e8c6f;
}

.input-area button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .chat-header {
    padding: 0.75rem 1rem;
  }

  .chat-header h1 {
    font-size: 1.25rem;
  }

  .chat-content {
    padding: 1rem;
  }

  .message {
    max-width: 90%;
  }

  .input-area {
    padding: 0.75rem 1rem;
  }
}
</style>
