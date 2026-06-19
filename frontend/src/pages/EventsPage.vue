<template>
  <q-page class="page-shell q-pa-lg">
    <div class="row items-start justify-between q-col-gutter-md q-mb-lg">
      <div>
        <div class="text-h4 text-weight-bold">События</div>
        <div class="text-body1 text-grey-7">Вертикальная шкала достижений, изменений рейтинга и спортивных результатов.</div>
      </div>
      <div class="row q-gutter-sm">
        <q-select v-model="league" dense outlined :options="leagues" label="Лига" style="min-width: 220px" />
        <q-select v-model="eventType" dense outlined :options="eventTypes" label="Тип" style="min-width: 180px" />
      </div>
    </div>

    <q-card flat bordered class="surface-card">
      <q-card-section>
        <q-timeline color="primary">
          <q-timeline-entry
            v-for="event in timelineEvents"
            :key="event.id"
            :title="event.title"
            :subtitle="event.date"
            :icon="event.icon"
            :color="event.color"
          >
            <div class="text-body2">{{ event.subtitle }}</div>
          </q-timeline-entry>
        </q-timeline>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { leagues, timelineEvents } from 'src/data/mock-dashboard';

const league = ref('Ярославская лига');
const eventType = ref('Все события');
const eventTypes = ['Все события', 'Победы', 'Рейтинг', 'Ранги', 'Медали', 'Рекорды'];
</script>
