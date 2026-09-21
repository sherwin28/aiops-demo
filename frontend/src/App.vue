<template>
  <div class="app">
    <header>
      <h1>AIOps Demo</h1>
      <span class="status" :class="{ green: status === 'ok' }">
        {{ status }}
      </span>
    </header>

    <main>
      <section class="incidents">
        <h2>Active Incidents</h2>
        <div v-for="inc in incidents" :key="inc.id" class="card">
          <div class="title">{{ inc.service }} - {{ inc.diagnosis?.root_cause }}</div>
          <div class="confidence">Confidence: {{ inc.diagnosis?.confidence }}</div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const status = ref('loading')
const incidents = ref([])

onMounted(async () => {
  const r = await fetch('/health')
  const j = await r.json()
  status.value = j.status

  // WebSocket connection
  const ws = new WebSocket(`ws://${location.host}/ws/incidents`)
  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data)
    if (msg.type === 'incident') {
      incidents.value.push(msg.data)
    }
  }
})
</script>
