import { computed, reactive } from 'vue';

import type {
  CurrentUserResponse,
  LoginRequest,
  RegisterRequest,
  TokenPairResponse
} from 'src/services/api';
import { authApiService } from 'src/services/api';
import { tokenStorage } from 'src/services/auth/token-storage';

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  currentUser: CurrentUserResponse | null;
  loading: boolean;
  initialized: boolean;
  errorMessage: string | null;
}

const storedTokens = tokenStorage.getTokens();

const state = reactive<AuthState>({
  accessToken: storedTokens?.accessToken ?? null,
  refreshToken: storedTokens?.refreshToken ?? null,
  currentUser: null,
  loading: false,
  initialized: false,
  errorMessage: null
});

const isAuthenticated = computed(() => state.currentUser !== null && state.accessToken !== null);

export function useAuth() {
  const restoreSession = async (): Promise<void> => {
    if (state.initialized || state.loading) {
      return;
    }

    state.loading = true;
    state.errorMessage = null;

    try {
      if (state.accessToken) {
        state.currentUser = await authApiService.me(state.accessToken);
        return;
      }

      if (state.refreshToken) {
        const tokens = await authApiService.refresh({ refresh_token: state.refreshToken });
        await applyTokenPair(tokens);
      }
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
    const refreshToken = state.refreshToken;
    clearSession();

    if (refreshToken) {
      try {
        await authApiService.logout({ refresh_token: refreshToken });
      } catch {
        // Local logout should not be blocked by a stale server-side refresh token.
      }
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

async function authenticate(request: () => Promise<TokenPairResponse>): Promise<void> {
  state.loading = true;
  state.errorMessage = null;

  try {
    const tokens = await request();
    await applyTokenPair(tokens);
  } catch (error) {
    state.errorMessage = error instanceof Error ? error.message : 'Auth request failed';
    throw error;
  } finally {
    state.loading = false;
  }
}

async function applyTokenPair(tokens: TokenPairResponse): Promise<void> {
  state.accessToken = tokens.access_token;
  state.refreshToken = tokens.refresh_token;
  tokenStorage.saveTokens({
    accessToken: tokens.access_token,
    refreshToken: tokens.refresh_token
  });
  state.currentUser = await authApiService.me(tokens.access_token);
}

function clearSession(): void {
  state.accessToken = null;
  state.refreshToken = null;
  state.currentUser = null;
  state.errorMessage = null;
  tokenStorage.clearTokens();
}
