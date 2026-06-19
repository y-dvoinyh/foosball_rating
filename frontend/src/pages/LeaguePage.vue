<template>
  <q-page class="page-shell q-pa-lg">
    <div class="entity-hero q-mb-lg">
      <div>
        <q-breadcrumbs class="text-grey-7 q-mb-sm">
          <q-breadcrumbs-el label="Лиги" to="/rating" />
          <q-breadcrumbs-el label="Ярославская лига" />
        </q-breadcrumbs>
        <div class="text-h4 text-weight-bold">Ярославская лига</div>
        <div class="text-body1 text-grey-8">
          Открытая лига для городских дипов, регулярных встреч и локальных соревнований.
        </div>
      </div>
      <q-btn color="primary" icon="leaderboard" label="Рейтинг лиги" to="/rating" no-caps />
    </div>

    <div class="row q-col-gutter-md q-mb-lg">
      <div v-for="metric in metrics" :key="metric.label" class="col-6 col-md-3">
        <q-card flat bordered class="metric-card">
          <div class="metric-value">{{ metric.value }}</div>
          <div class="metric-label">{{ metric.label }}</div>
        </q-card>
      </div>
    </div>

    <q-card flat bordered class="surface-card">
      <q-card-section class="row items-center justify-between">
        <div class="text-h6">Турниры лиги</div>
        <q-btn flat color="primary" icon="add" label="Турнир" no-caps />
      </q-card-section>
      <q-list separator>
        <q-item v-for="tournament in tournaments" :key="tournament.id" clickable :to="`/tournaments/${tournament.id}`">
          <q-item-section>
            <q-item-label class="text-weight-medium">{{ tournament.title }}</q-item-label>
            <q-item-label caption>{{ tournament.period }} · {{ tournament.ratingMode }}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-chip dense color="primary" text-color="white">{{ tournament.competitions }} событий</q-chip>
          </q-item-section>
        </q-item>
      </q-list>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { tournaments } from 'src/data/mock-dashboard';

const metrics = [
  { label: 'Игроков', value: '140' },
  { label: 'Матчей', value: '4 820' },
  { label: 'Голов', value: '26 940' },
  { label: 'Активных турниров', value: '3' }
];
</script>
