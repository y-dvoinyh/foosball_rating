<template>
  <q-page class="page-shell q-pa-lg">
    <div class="row items-start justify-between q-col-gutter-md q-mb-lg">
      <div>
        <div class="text-h4 text-weight-bold">Рейтинг игроков</div>
        <div class="text-body1 text-grey-7">Единая таблица с переключением контекста рейтинга.</div>
      </div>

      <div class="row q-gutter-sm">
        <q-btn-toggle v-model="ratingContext" unelevated rounded toggle-color="primary" :options="contextOptions" />
        <q-btn color="primary" icon="add" label="Матч" no-caps />
      </div>
    </div>

    <q-card flat bordered class="surface-card">
      <q-card-section class="row q-col-gutter-md items-center">
        <div class="col-12 col-md-4">
          <q-select v-model="league" dense outlined :options="leagues" label="Лига" />
        </div>
        <div class="col-12 col-md-4">
          <q-select v-model="period" dense outlined :options="periods" label="Период" />
        </div>
        <div class="col-12 col-md-4">
          <q-input v-model="search" dense outlined clearable placeholder="Поиск игрока">
            <template #prepend>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </q-card-section>

      <q-separator />

      <q-table
        flat
        :rows="players"
        :columns="columns"
        row-key="id"
        :filter="search"
        :pagination="{ rowsPerPage: 10 }"
      >
        <template #body-cell-name="props">
          <q-td :props="props">
            <router-link class="table-link" :to="`/players/${props.row.id}`">{{ props.row.name }}</router-link>
          </q-td>
        </template>

        <template #body-cell-delta="props">
          <q-td :props="props">
            <q-badge :color="props.row.delta >= 0 ? 'positive' : 'negative'" outline>
              {{ props.row.delta > 0 ? '+' : '' }}{{ props.row.delta }}
            </q-badge>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { leagues, players } from 'src/data/mock-dashboard';

const ratingContext = ref('league');
const league = ref('Ярославская лига');
const period = ref('Текущий сезон');
const search = ref('');

const contextOptions = [
  { label: 'Глобальный', value: 'global' },
  { label: 'Лига', value: 'league' },
  { label: 'Сезон', value: 'season' },
  { label: 'Турнир', value: 'tournament' }
];

const periods = ['Все время', 'Текущий сезон', '2026 год', '90 дней', '30 дней'];

const columns = [
  { name: 'rank', label: '№', field: 'rank', align: 'left' as const, sortable: true },
  { name: 'name', label: 'Игрок', field: 'name', align: 'left' as const, sortable: true },
  { name: 'tier', label: 'Ранг', field: 'tier', align: 'left' as const, sortable: true },
  { name: 'rating', label: 'Рейтинг', field: 'rating', align: 'right' as const, sortable: true },
  { name: 'delta', label: '+/-', field: 'delta', align: 'right' as const, sortable: true },
  { name: 'matches', label: 'Матчей', field: 'matches', align: 'right' as const, sortable: true },
  { name: 'goals', label: 'Голов', field: 'goals', align: 'right' as const, sortable: true },
  { name: 'winRate', label: 'Побед', field: 'winRate', align: 'right' as const, sortable: true }
];
</script>
