<template>
  <q-page class="page-shell q-pa-lg">
    <div class="entity-hero q-mb-lg">
      <div>
        <q-breadcrumbs class="text-grey-7 q-mb-sm">
          <q-breadcrumbs-el label="Ярославская лига" to="/leagues/yaroslavl" />
          <q-breadcrumbs-el label="Дипы в Расколе 2026" />
        </q-breadcrumbs>
        <div class="text-h4 text-weight-bold">Дипы в Расколе 2026</div>
        <div class="text-body1 text-grey-8">
          Серия регулярных соревнований с отдельным турнирным рейтингом и настройками расчета.
        </div>
      </div>
      <q-btn color="primary" icon="leaderboard" label="Рейтинг турнира" to="/rating" no-caps />
    </div>

    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-md-8">
        <q-card flat bordered class="surface-card">
          <q-card-section class="row items-center justify-between">
            <div>
              <div class="text-h6">Соревнования</div>
              <div class="text-caption text-grey-7">События внутри турнира с матчами и изменениями рейтинга.</div>
            </div>
            <q-btn flat color="primary" icon="add" label="Соревнование" no-caps />
          </q-card-section>
          <q-list separator>
            <q-item v-for="competition in competitions" :key="competition.id" clickable :to="`/competitions/${competition.id}`">
              <q-item-section>
                <q-item-label class="text-weight-medium">{{ competition.title }}</q-item-label>
                <q-item-label caption>{{ competition.date }} · победитель: {{ competition.winner }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-chip dense>{{ competition.matches }} матчей</q-chip>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card flat bordered class="surface-card">
          <q-card-section>
            <div class="text-h6 q-mb-md">Настройки рейтинга</div>
            <q-list dense>
              <q-item>
                <q-item-section>Коэффициент</q-item-section>
                <q-item-section side>x1.2</q-item-section>
              </q-item>
              <q-item>
                <q-item-section>Базовый рейтинг</q-item-section>
                <q-item-section side>1000</q-item-section>
              </q-item>
              <q-item>
                <q-item-section>Контекст</q-item-section>
                <q-item-section side>Лига + турнир</q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { competitions } from 'src/data/mock-dashboard';
</script>
