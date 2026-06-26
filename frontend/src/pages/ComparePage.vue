<template>
  <q-page class="page-shell q-pa-lg">
    <div class="text-h4 text-weight-bold">Сравнение игроков</div>
    <div class="text-body1 text-grey-7 q-mb-lg">Очные встречи, рейтинг и метрики в выбранном контексте.</div>

    <q-card flat bordered class="surface-card q-mb-lg">
      <q-card-section class="row q-col-gutter-md">
        <div class="col-12 col-md-4">
          <q-select v-model="playerA" outlined dense :options="playerOptions" label="Игрок A" />
        </div>
        <div class="col-12 col-md-4">
          <q-select v-model="playerB" outlined dense :options="playerOptions" label="Игрок B" />
        </div>
        <div class="col-12 col-md-4">
          <q-select v-model="context" outlined dense :options="contexts" label="Контекст рейтинга" />
        </div>
      </q-card-section>
    </q-card>

    <div class="comparison-grid">
      <q-card flat bordered class="surface-card player-versus">
        <q-avatar color="primary" text-color="white" size="72px">ЯД</q-avatar>
        <div class="text-h6 q-mt-sm">Ярослав Двойных</div>
        <div class="text-h4 text-weight-bold">1656</div>
      </q-card>

      <q-card flat bordered class="surface-card metric-versus">
        <div v-for="metric in metrics" :key="metric.label" class="versus-row">
          <div class="versus-value">{{ metric.a }}</div>
          <div class="versus-label">{{ metric.label }}</div>
          <div class="versus-value">{{ metric.b }}</div>
        </div>
      </q-card>

      <q-card flat bordered class="surface-card player-versus">
        <q-avatar color="deep-orange-7" text-color="white" size="72px">ИН</q-avatar>
        <div class="text-h6 q-mt-sm">Илья Нестеров</div>
        <div class="text-h4 text-weight-bold">1652</div>
      </q-card>
    </div>

    <q-card flat bordered class="surface-card q-mt-lg">
      <q-card-section>
        <div class="text-h6">Личные встречи</div>
        <div class="text-caption text-grey-7">Баланс очных матчей и последние результаты.</div>
      </q-card-section>
      <q-table flat :rows="headToHead" :columns="columns" row-key="date" hide-bottom />
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const playerA = ref('Ярослав Двойных');
const playerB = ref('Илья Нестеров');
const context = ref('Ярославская лига');

const playerOptions = ['Ярослав Двойных', 'Илья Нестеров', 'Илья Вострилов', 'Николай Шергесов'];
const contexts = ['Глобальный рейтинг', 'Ярославская лига', 'Сезон 2026', 'Дипы в Расколе 2026'];

const metrics = [
  { label: 'Рейтинг', a: '1656', b: '1652' },
  { label: 'Матчей', a: '853', b: '284' },
  { label: 'Побед', a: '492', b: '189' },
  { label: 'Winrate', a: '58%', b: '67%' },
  { label: 'Голов', a: '4647', b: '1644' }
];

const headToHead = [
  { date: '29.05.2026', event: 'A-trip', score: '7:5', winner: 'Ярослав Двойных' },
  { date: '22.05.2026', event: 'Пятница', score: '4:7', winner: 'Илья Нестеров' },
  { date: '15.05.2026', event: '15 мая', score: '7:3', winner: 'Ярослав Двойных' }
];

const columns = [
  { name: 'date', label: 'Дата', field: 'date', align: 'left' as const },
  { name: 'event', label: 'Событие', field: 'event', align: 'left' as const },
  { name: 'score', label: 'Счет', field: 'score', align: 'center' as const },
  { name: 'winner', label: 'Победитель', field: 'winner', align: 'left' as const }
];
</script>
