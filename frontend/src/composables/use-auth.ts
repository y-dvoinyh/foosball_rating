import { computed, reactive } from 'vue';

import type {
  CurrentUserResponse,
  LoginRequest,
  RegisterRequest,
  AccessTokenResponse
} from 'src/services/api';
import { authApiService } from 'src/services/api';

interface AuthState {
  accessToken: string | null;
  currentUser: CurrentUserResponse | null;
  loading: boolean;
  initialized: boolean;
  errorMessage: string | null;
}

clearLegacyStoredTokens();

const state = reactive<AuthState>({
  accessToken: null,
  currentUser: null,
  loading: false,
  initialized: false,
  errorMessage: null
});

const AUTH_SESSION_HINT_COOKIE_NAME = 'auth_session';

const isAuthenticated = computed(() => state.currentUser !== null && state.accessToken !== null);

export function useAuth() {
  const restoreSession = async (): Promise<void> => {
    if (state.initialized || state.loading) {
      return;
    }

    state.loading = true;
    state.errorMessage = null;

    try {
      if (!hasAuthSessionHint()) {
        clearSession();
        return;
      }

      const tokens = await authApiService.refresh();
      await applyAccessToken(tokens);
    } catch {
      clearSession();
    } finally {
      state.initialized = true;
      state.loading = false;
    }
  };

  const login = async (payload: LoginRequest): Promise<void> => {
    await authenticate(() => authApiService.login(payload));
  };

  const register = async (payload: RegisterRequest): Promise<void> => {
    await authenticate(() => authApiService.register(payload));
  };

  const logout = async (): Promise<void> => {
    clearSession();

    try {
      await authApiService.logout();
    } catch {
      // Local logout should not be blocked by a stale server-side refresh token.
    }
  };

  return {
    state,
    isAuthenticated,
    restoreSession,
    login,
    register,
    logout
  };
}

async function authenticate(request: () => Promise<AccessTokenResponse>): Promise<void> {
  state.loading = true;
  state.errorMessage = null;

  try {
    const tokens = await request();
    await applyAccessToken(tokens);
  } catch (error) {
    state.errorMessage = error instanceof Error ? error.message : 'Auth request failed';
    throw error;
  } finally {
    state.loading = false;
  }
}

async function applyAccessToken(tokens: AccessTokenResponse): Promise<void> {
  state.accessToken = tokens.access_token;
  state.currentUser = await authApiService.me(tokens.access_token);
  saveAuthSessionHint();
}

function clearSession(): void {
  state.accessToken = null;
  state.currentUser = null;
  state.errorMessage = null;
  clearAuthSessionHint();
}

function hasAuthSessionHint(): boolean {
  return document.cookie
    .split('; ')
    .some((cookie) => cookie === `${AUTH_SESSION_HINT_COOKIE_NAME}=1`);
}

function saveAuthSessionHint(): void {
  document.cookie = `${AUTH_SESSION_HINT_COOKIE_NAME}=1; Max-Age=2592000; Path=/; SameSite=Lax`;
}

function clearAuthSessionHint(): void {
  document.cookie = `${AUTH_SESSION_HINT_COOKIE_NAME}=; Max-Age=0; Path=/; SameSite=Lax`;
}

function clearLegacyStoredTokens(): void {
  window.localStorage.removeItem('foosball_rating.access_token');
  window.localStorage.removeItem('foosball_rating.refresh_token');
}
