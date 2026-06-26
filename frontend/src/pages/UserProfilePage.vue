<template>
  <q-page class="page-shell q-pa-lg">
    <div class="user-profile-layout">
      <q-card flat bordered class="surface-card user-profile-summary">
        <q-card-section class="column items-center text-center">
          <q-avatar size="88px" color="primary" text-color="white" class="q-mb-md">
            {{ userInitials }}
          </q-avatar>
          <div class="text-h5 text-weight-bold">{{ currentUserEmail }}</div>
          <q-chip
            v-if="currentUser?.is_superuser"
            color="primary"
            text-color="white"
            icon="admin_panel_settings"
            class="q-mt-sm"
          >
            Администратор
          </q-chip>
          <q-chip v-else color="grey-2" text-color="grey-8" icon="person" class="q-mt-sm">
            Пользователь
          </q-chip>
        </q-card-section>
      </q-card>

      <div class="column q-gutter-md">
        <q-card flat bordered class="surface-card">
          <q-card-section>
            <div class="text-h6">Профиль пользователя</div>
            <div class="text-body2 text-grey-7 q-mt-sm">
              Здесь позже появятся имя, настройки аккаунта, активные сессии и привязка к
              игровому профилю.
            </div>
          </q-card-section>
          <q-list separator>
            <q-item>
              <q-item-section avatar><q-icon name="mail" /></q-item-section>
              <q-item-section>
                <q-item-label>Email</q-item-label>
                <q-item-label caption>{{ currentUserEmail }}</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar><q-icon name="verified_user" /></q-item-section>
              <q-item-section>
                <q-item-label>Статус</q-item-label>
                <q-item-label caption>{{ currentUserStatus }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>

        <q-card flat bordered class="surface-card">
          <q-card-section class="row items-center justify-between">
            <div>
              <div class="text-h6">Быстрые действия</div>
              <div class="text-caption text-grey-7">Заглушки будущих пользовательских настроек.</div>
            </div>
          </q-card-section>
          <q-card-section class="row q-gutter-sm">
            <q-btn outline color="primary" icon="settings" label="Настройки" no-caps disable />
            <q-btn outline color="primary" icon="sports_soccer" label="Игровой профиль" no-caps disable />
            <q-btn outline color="primary" icon="password" label="Сменить пароль" no-caps disable />
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAuth } from 'src/composables/use-auth';

const { state } = useAuth();

const currentUser = computed(() => state.currentUser);
const currentUserEmail = computed(() => currentUser.value?.email ?? 'Профиль');
const userInitials = computed(() => (currentUser.value?.email.slice(0, 2) || '??').toUpperCase());
const currentUserStatus = computed(() =>
  currentUser.value?.is_superuser ? 'Суперпользователь' : 'Обычный пользователь'
);
</script>
