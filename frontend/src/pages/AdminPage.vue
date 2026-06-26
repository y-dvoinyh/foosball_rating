<template>
  <q-page class="page-shell q-pa-lg">
    <div class="admin-page-header q-mb-lg">
      <div>
        <div class="text-h4 text-weight-bold">Администрирование</div>
        <div class="text-body1 text-grey-7">
          Первый защищенный раздел для пользователей с правами суперпользователя.
        </div>
      </div>
      <div class="admin-access-badge">
        <q-icon name="admin_panel_settings" size="18px" />
        <span>Суперпользователь</span>
      </div>
    </div>

    <div class="row q-col-gutter-md">
      <div v-for="section in sections" :key="section.title" class="col-12 col-md-4">
        <q-card flat bordered class="surface-card admin-section-card">
          <q-card-section>
            <q-icon :name="section.icon" color="primary" size="32px" />
            <div class="text-h6 q-mt-md">{{ section.title }}</div>
            <div class="text-body2 text-grey-7 q-mt-sm">{{ section.description }}</div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
const sections = [
  {
    title: 'Пользователи',
    description: 'Управление учетными записями, доступом и будущими ролями.',
    icon: 'manage_accounts'
  },
  {
    title: 'Импорт',
    description: 'Запуск и мониторинг задач импорта внешних данных.',
    icon: 'cloud_upload'
  },
  {
    title: 'Рейтинги',
    description: 'Контроль пересчета рейтингов и истории изменений.',
    icon: 'leaderboard'
  }
];
</script>
