<template>
  <div id="app" class="app-container">
    <ChatInterface />
  </div>
</template>

<script setup>
import ChatInterface from './components/chat/ChatInterface.vue'
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

#app {
  height: 100vh;
}
</style>
