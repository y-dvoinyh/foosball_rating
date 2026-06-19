<template>
  <q-page class="column items-center justify-center q-pa-md">
    <div class="text-h4 q-mb-sm">Foosball Rating</div>
    <div class="text-body1 text-grey-8 q-mb-lg">Frontend is ready.</div>

    <q-banner rounded class="bg-white text-dark shadow-1">
      Backend health: {{ healthStatus }}
    </q-banner>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { healthApiService } from 'src/services/api';

const healthStatus = ref('checking...');

onMounted(async () => {
  try {
    const data = await healthApiService.getHealth();
    healthStatus.value = `${data.status}, database: ${data.database}`;
  } catch {
    healthStatus.value = 'unavailable';
  }
});
</script>
