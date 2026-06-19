<template>
  <q-page class="page-shell q-pa-lg">
    <div class="dashboard-hero q-mb-lg">
      <div class="dashboard-hero__content">
        <q-chip color="white" text-color="primary" icon="leaderboard">Ярославская лига</q-chip>
        <div class="text-h3 text-weight-bold q-mt-md">Публичная статистика кикера</div>
        <div class="text-body1 q-mt-sm">
          Рейтинги, матчи, турниры, события игроков и динамика результатов в разных лигах.
        </div>
      </div>
      <div class="dashboard-hero__actions">
        <q-btn color="white" text-color="primary" icon="leaderboard" label="Открыть рейтинг" to="/rating" no-caps />
        <q-btn outline color="white" icon="compare_arrows" label="Сравнить игроков" to="/compare" no-caps />
      </div>
    </div>

    <div class="row q-col-gutter-md q-mb-lg">
      <div v-for="metric in metrics" :key="metric.label" class="col-6 col-md-3">
        <q-card flat bordered class="metric-card">
          <q-icon :name="metric.icon" color="primary" size="28px" />
          <div class="metric-value">{{ metric.value }}</div>
          <div class="metric-label">{{ metric.label }}</div>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-lg">
      <div class="col-12 col-lg-7">
        <q-card flat bordered class="surface-card">
          <q-card-section class="row items-center justify-between">
            <div>
              <div class="text-h6">Топ игроков</div>
              <div class="text-caption text-grey-7">Рейтинг выбранной лиги.</div>
            </div>
            <q-btn flat color="primary" label="Весь рейтинг" to="/rating" no-caps />
          </q-card-section>
          <q-table flat :rows="players" :columns="playerColumns" row-key="id" hide-bottom :pagination="{ rowsPerPage: 4 }">
            <template #body-cell-name="props">
              <q-td :props="props">
                <router-link class="table-link" :to="`/players/${props.row.id}`">{{ props.row.name }}</router-link>
              </q-td>
            </template>
          </q-table>
        </q-card>
      </div>

      <div class="col-12 col-lg-5">
        <q-card flat bordered class="surface-card q-mb-lg">
          <q-card-section class="row items-center justify-between">
            <div>
              <div class="text-h6">Активные турниры</div>
              <div class="text-caption text-grey-7">Соревнования с отдельным рейтингом.</div>
            </div>
            <q-btn flat color="primary" label="Лига" to="/leagues/yaroslavl" no-caps />
          </q-card-section>
          <q-list separator>
            <q-item v-for="tournament in tournaments" :key="tournament.id" clickable :to="`/tournaments/${tournament.id}`">
              <q-item-section>
                <q-item-label class="text-weight-medium">{{ tournament.title }}</q-item-label>
                <q-item-label caption>{{ tournament.league }} · {{ tournament.period }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-chip dense>{{ tournament.players }} игроков</q-chip>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>

        <q-card flat bordered class="surface-card">
          <q-card-section>
            <div class="text-h6">Последние события</div>
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

    <q-banner rounded class="bg-white text-grey-8 q-mt-lg">
      Backend health: {{ healthStatus }}
    </q-banner>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { healthApiService } from 'src/services/api';
import { players, timelineEvents, tournaments } from 'src/data/mock-dashboard';

const healthStatus = ref('checking...');

const metrics = [
  { label: 'Игроков', value: '140', icon: 'groups' },
  { label: 'Матчей', value: '4 820', icon: 'sports' },
  { label: 'Голов', value: '26 940', icon: 'sports_soccer' },
  { label: 'Лиг', value: '12', icon: 'public' }
];

const playerColumns = [
  { name: 'rank', label: '№', field: 'rank', align: 'left' as const },
  { name: 'name', label: 'Игрок', field: 'name', align: 'left' as const },
  { name: 'rating', label: 'Рейтинг', field: 'rating', align: 'right' as const },
  { name: 'delta', label: '+/-', field: 'delta', align: 'right' as const }
];

onMounted(async () => {
  try {
    const data = await healthApiService.getHealth();
    healthStatus.value = `${data.status}, database: ${data.database}`;
  } catch {
    healthStatus.value = 'unavailable';
  }
});
</script>
