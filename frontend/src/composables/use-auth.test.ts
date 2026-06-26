import { beforeEach, describe, expect, it, vi } from 'vitest';

const authApiService = {
  refresh: vi.fn(),
  me: vi.fn(),
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn()
};

vi.mock('src/services/api', () => ({
  authApiService
}));

describe('useAuth', () => {
  beforeEach(() => {
    vi.resetModules();
    vi.clearAllMocks();
    window.localStorage.clear();
    document.cookie = 'auth_session=; Max-Age=0; Path=/; SameSite=Lax';
  });

  it('does not refresh session when no auth session hint exists', async () => {
    const { useAuth } = await import('./use-auth');

    await useAuth().restoreSession();

    expect(authApiService.refresh).not.toHaveBeenCalled();
  });

  it('refreshes session when auth session hint exists', async () => {
    document.cookie = 'auth_session=1; Path=/; SameSite=Lax';
    authApiService.refresh.mockResolvedValue({
      access_token: 'access-token',
      token_type: 'bearer'
    });
    authApiService.me.mockResolvedValue({
      id: 1,
      email: 'user@example.com',
      is_active: true,
      is_superuser: false
    });

    const { useAuth } = await import('./use-auth');
    const auth = useAuth();

    await auth.restoreSession();

    expect(authApiService.refresh).toHaveBeenCalledOnce();
    expect(auth.isAuthenticated.value).toBe(true);
  });

  it('stores auth session hint cookie after login', async () => {
    authApiService.login.mockResolvedValue({
      access_token: 'access-token',
      token_type: 'bearer'
    });
    authApiService.me.mockResolvedValue({
      id: 1,
      email: 'user@example.com',
      is_active: true,
      is_superuser: false
    });

    const { useAuth } = await import('./use-auth');

    await useAuth().login({ email: 'user@example.com', password: 'password123' });

    expect(document.cookie).toContain('auth_session=1');
  });
});
