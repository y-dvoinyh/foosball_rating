<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="app-header">
      <q-toolbar class="q-gutter-sm">
        <q-btn flat dense round icon="sports_soccer" to="/" aria-label="Foosball Rating" />

        <q-toolbar-title class="app-title">Foosball Rating</q-toolbar-title>

        <q-select
          v-model="selectedLeague"
          dense
          dark
          borderless
          use-input
          hide-selected
          fill-input
          input-debounce="0"
          :options="filteredLeagues"
          class="league-select gt-sm"
          @filter="filterLeagues"
        >
          <template #prepend>
            <q-icon name="location_on" />
          </template>
        </q-select>

        <q-input
          v-model="search"
          dense
          dark
          borderless
          placeholder="Игрок, лига, турнир"
          class="global-search gt-md"
        >
          <template #prepend>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-tabs shrink stretch class="main-nav gt-sm">
          <q-route-tab to="/rating" label="Рейтинг" />
          <q-route-tab to="/leagues/yaroslavl" label="Лига" />
          <q-route-tab to="/tournaments/spring" label="Турнир" />
          <q-route-tab to="/events" label="События" />
          <q-route-tab to="/compare" label="Сравнение" />
        </q-tabs>

        <q-space />

        <template v-if="isAuthenticated">
          <q-btn-dropdown flat no-caps class="profile-button">
            <template #label>
              <q-avatar size="28px" color="white" text-color="primary" class="q-mr-sm">{{
                userInitials
              }}</q-avatar>
              <span class="gt-xs">{{ currentUserEmail }}</span>
            </template>
            <q-list>
              <q-item v-close-popup clickable>
                <q-item-section avatar><q-icon name="person" /></q-item-section>
                <q-item-section>{{ currentUserEmail }}</q-item-section>
              </q-item>
              <q-item v-if="currentUser?.is_superuser" v-close-popup clickable>
                <q-item-section avatar><q-icon name="admin_panel_settings" /></q-item-section>
                <q-item-section>Администрирование</q-item-section>
              </q-item>
              <q-separator />
              <q-item v-close-popup clickable @click="handleLogout">
                <q-item-section avatar><q-icon name="logout" /></q-item-section>
                <q-item-section>Выйти</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </template>

        <template v-else>
          <q-btn flat label="Войти" no-caps @click="loginDialog = true" />
          <q-btn outline label="Регистрация" no-caps class="gt-xs" @click="registerDialog = true" />
        </template>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-dialog v-model="loginDialog">
      <q-card class="auth-card">
        <q-card-section>
          <div class="text-h6">Вход</div>
        </q-card-section>
        <q-form @submit.prevent="handleLogin">
          <q-card-section class="q-gutter-md">
            <q-banner v-if="authError" rounded class="bg-red-1 text-negative">{{
              authError
            }}</q-banner>
            <q-input v-model="loginEmail" outlined dense label="Email" type="email" />
            <q-input v-model="loginPassword" outlined dense label="Пароль" type="password" />
          </q-card-section>
          <q-card-actions align="between">
            <q-btn flat label="Регистрация" no-caps @click="openRegister" />
            <q-btn color="primary" label="Войти" no-caps type="submit" :loading="authLoading" />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>

    <q-dialog v-model="registerDialog">
      <q-card class="auth-card">
        <q-card-section>
          <div class="text-h6">Регистрация</div>
        </q-card-section>
        <q-form @submit.prevent="handleRegister">
          <q-card-section class="q-gutter-md">
            <q-banner v-if="authError" rounded class="bg-red-1 text-negative">{{
              authError
            }}</q-banner>
            <q-input v-model="registerEmail" outlined dense label="Email" type="email" />
            <q-input v-model="registerPassword" outlined dense label="Пароль" type="password" />
          </q-card-section>
          <q-card-actions align="right">
            <q-btn v-close-popup flat label="Отмена" no-caps />
            <q-btn
              color="primary"
              label="Создать аккаунт"
              no-caps
              type="submit"
              :loading="authLoading"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { leagues } from 'src/data/mock-dashboard';
import { useAuth } from 'src/composables/use-auth';

const selectedLeague = ref('Ярославская лига');
const filteredLeagues = ref(leagues);
const search = ref('');
const loginDialog = ref(false);
const registerDialog = ref(false);
const loginEmail = ref('');
const loginPassword = ref('');
const registerEmail = ref('');
const registerPassword = ref('');
const { state: authState, isAuthenticated, restoreSession, login, register, logout } = useAuth();
const currentUser = computed(() => authState.currentUser);
const currentUserEmail = computed(() => currentUser.value?.email ?? 'Профиль');
const userInitials = computed(() => (currentUser.value?.email.slice(0, 2) || '??').toUpperCase());
const authLoading = computed(() => authState.loading);
const authError = computed(() => authState.errorMessage);

onMounted(() => {
  void restoreSession();
});

const filterLeagues = (value: string, update: (callback: () => void) => void) => {
  update(() => {
    const needle = value.toLowerCase();
    filteredLeagues.value = leagues.filter((league) => league.toLowerCase().includes(needle));
  });
};

const openRegister = () => {
  loginDialog.value = false;
  registerDialog.value = true;
};

const handleLogin = async () => {
  await login({
    email: loginEmail.value,
    password: loginPassword.value
  });
  loginDialog.value = false;
  loginPassword.value = '';
};

const handleRegister = async () => {
  await register({
    email: registerEmail.value,
    password: registerPassword.value
  });
  registerDialog.value = false;
  registerPassword.value = '';
};

const handleLogout = () => {
  void logout();
};
</script>
