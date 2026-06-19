<template>
  <q-page class="page-shell q-pa-lg">
    <div class="player-layout">
      <q-card flat bordered class="surface-card player-summary">
        <q-card-section class="column items-center text-center">
          <q-avatar size="92px" color="primary" text-color="white" class="q-mb-md">ЯД</q-avatar>
          <div class="text-h5 text-weight-bold">Ярослав Двойных</div>
          <q-chip color="indigo-1" text-color="indigo-9" class="q-mt-sm">semi-pro</q-chip>
          <div class="text-h3 text-weight-bold q-mt-lg">1656</div>
          <div class="text-caption text-grey-7">текущий рейтинг</div>
        </q-card-section>
        <q-separator />
        <q-list dense>
          <q-item v-for="stat in summaryStats" :key="stat.label">
            <q-item-section>{{ stat.label }}</q-item-section>
            <q-item-section side>{{ stat.value }}</q-item-section>
          </q-item>
        </q-list>
      </q-card>

      <div class="column q-gutter-md">
        <q-card flat bordered class="surface-card">
          <q-card-section class="row items-center justify-between">
            <div>
              <div class="text-h6">Статистика игрока</div>
              <div class="text-caption text-grey-7">Переключение между рейтингами, лигами, сезонами и турнирами.</div>
            </div>
            <q-btn-toggle v-model="context" unelevated toggle-color="primary" :options="contextOptions" />
          </q-card-section>

          <q-card-section>
            <div class="rating-chart">
              <div v-for="point in chartPoints" :key="point.label" class="chart-point" :style="{ height: point.height }">
                <q-tooltip>{{ point.label }} · {{ point.value }}</q-tooltip>
              </div>
            </div>
          </q-card-section>
        </q-card>

        <div class="row q-col-gutter-md">
          <div v-for="block in statBlocks" :key="block.title" class="col-12 col-md-4">
            <q-card flat bordered class="metric-card">
              <q-icon :name="block.icon" color="primary" size="28px" />
              <div class="metric-value">{{ block.value }}</div>
              <div class="metric-label">{{ block.title }}</div>
            </q-card>
          </div>
        </div>

        <q-card flat bordered class="surface-card">
          <q-card-section class="row items-center justify-between">
            <div class="text-h6">События игрока</div>
            <q-btn flat color="primary" label="Все события" to="/events" no-caps />
          </q-card-section>
          <q-timeline color="primary" layout="dense">
            <q-timeline-entry
              v-for="event in timelineEvents.slice(0, 3)"
              :key="event.id"
              :title="event.title"
              :subtitle="event.date"
              :icon="event.icon"
              :color="event.color"
            >
              {{ event.subtitle }}
            </q-timeline-entry>
          </q-timeline>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { timelineEvents } from 'src/data/mock-dashboard';

const context = ref('global');
const contextOptions = [
  { label: 'Глобально', value: 'global' },
  { label: 'Лиги', value: 'leagues' },
  { label: 'Сезоны', value: 'seasons' },
  { label: 'Турниры', value: 'tournaments' }
];

const summaryStats = [
  { label: 'Турниров', value: '93' },
  { label: 'Матчей', value: '853' },
  { label: 'Голов', value: '4647' },
  { label: 'Побед', value: '492' }
];

const statBlocks = [
  { title: 'Процент побед', value: '58%', icon: 'percent' },
  { title: 'Лучшая серия', value: '12', icon: 'local_fire_department' },
  { title: 'Медали', value: '62', icon: 'military_tech' }
];

const chartPoints = [
  { label: 'Янв', value: 1510, height: '32%' },
  { label: 'Фев', value: 1550, height: '48%' },
  { label: 'Мар', value: 1613, height: '68%' },
  { label: 'Апр', value: 1655, height: '86%' },
  { label: 'Май', value: 1656, height: '88%' }
];
</script>
