<template>
  <q-page class="page-shell q-pa-lg">
    <div class="entity-hero q-mb-lg">
      <div>
        <q-breadcrumbs class="text-grey-7 q-mb-sm">
          <q-breadcrumbs-el label="Дипы в Расколе 2026" to="/tournaments/spring" />
          <q-breadcrumbs-el label="A-trip 29.05.2026" />
        </q-breadcrumbs>
        <div class="text-h4 text-weight-bold">A-trip 29.05.2026</div>
        <div class="text-body1 text-grey-8">
          Конкретное соревнование: итоги, матчи, результаты и изменения рейтингов по каждому матчу.
        </div>
      </div>
      <q-btn color="primary" icon="link" label="Kickertools" outline no-caps />
    </div>

    <div class="row q-col-gutter-md q-mb-lg">
      <div v-for="place in podium" :key="place.label" class="col-12 col-md-4">
        <q-card flat bordered class="metric-card">
          <q-icon :name="place.icon" :color="place.color" size="32px" />
          <div class="text-subtitle1 text-weight-medium q-mt-sm">{{ place.label }}</div>
          <div class="text-body2 text-grey-7">{{ place.player }}</div>
        </q-card>
      </div>
    </div>

    <q-card flat bordered class="surface-card">
      <q-card-section class="row items-center justify-between">
        <div>
          <div class="text-h6">Матчи и изменения рейтинга</div>
          <div class="text-caption text-grey-7">Один матч может менять сразу несколько рейтингов.</div>
        </div>
        <q-btn-toggle v-model="deltaMode" dense unelevated toggle-color="primary" :options="deltaOptions" />
      </q-card-section>

      <q-table flat :rows="matchRows" :columns="columns" row-key="id" :pagination="{ rowsPerPage: 10 }" />
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { matchRows } from 'src/data/mock-dashboard';

const deltaMode = ref('all');
const deltaOptions = [
  { label: 'Все', value: 'all' },
  { label: 'Глобальный', value: 'global' },
  { label: 'Лига', value: 'league' },
  { label: 'Турнир', value: 'tournament' }
];

const podium = [
  { label: '1 место', player: 'Илья Нестеров', icon: 'emoji_events', color: 'amber-8' },
  { label: '2 место', player: 'Ярослав Двойных', icon: 'military_tech', color: 'grey-7' },
  { label: '3 место', player: 'Илья Вострилов', icon: 'workspace_premium', color: 'deep-orange-6' }
];

const columns = [
  { name: 'round', label: 'Раунд', field: 'round', align: 'left' as const },
  { name: 'teamA', label: 'Команда A', field: 'teamA', align: 'left' as const },
  { name: 'score', label: 'Счет', field: 'score', align: 'center' as const },
  { name: 'teamB', label: 'Команда B', field: 'teamB', align: 'left' as const },
  { name: 'globalDelta', label: 'Глоб.', field: 'globalDelta', align: 'right' as const },
  { name: 'leagueDelta', label: 'Лига', field: 'leagueDelta', align: 'right' as const },
  { name: 'tournamentDelta', label: 'Турнир', field: 'tournamentDelta', align: 'right' as const }
];
</script>
