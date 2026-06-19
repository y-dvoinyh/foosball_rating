import type { AxiosInstance } from 'axios';
import { describe, expect, it, vi } from 'vitest';

import { AuthApiService } from './auth-api-service';

function createMockClient(): AxiosInstance {
  return {
    get: vi.fn(),
    post: vi.fn()
  } as unknown as AxiosInstance;
}

describe('AuthApiService', () => {
  it('registers a user', async () => {
    const client = createMockClient();
    const service = new AuthApiService(client);
    const response = {
      access_token: 'access',
      refresh_token: 'refresh',
      token_type: 'bearer' as const
    };
    vi.mocked(client.post).mockResolvedValue({ data: response });

    await expect(
      service.register({ email: 'user@example.com', password: 'password123' })
    ).resolves.toEqual(response);

    expect(client.post).toHaveBeenCalledWith('/auth/register', {
      email: 'user@example.com',
      password: 'password123'
    }, undefined);
  });

  it('logs in a user', async () => {
    const client = createMockClient();
    const service = new AuthApiService(client);
    vi.mocked(client.post).mockResolvedValue({
      data: {
        access_token: 'access',
        refresh_token: 'refresh',
        token_type: 'bearer'
      }
    });

    await service.login({ email: 'user@example.com', password: 'password123' });

    expect(client.post).toHaveBeenCalledWith('/auth/login', {
      email: 'user@example.com',
      password: 'password123'
    }, undefined);
  });

  it('refreshes tokens', async () => {
    const client = createMockClient();
    const service = new AuthApiService(client);
    vi.mocked(client.post).mockResolvedValue({
      data: {
        access_token: 'new-access',
        refresh_token: 'new-refresh',
        token_type: 'bearer'
      }
    });

    await service.refresh({ refresh_token: 'old-refresh' });

    expect(client.post).toHaveBeenCalledWith('/auth/refresh', {
      refresh_token: 'old-refresh'
    }, undefined);
  });

  it('logs out with refresh token', async () => {
    const client = createMockClient();
    const service = new AuthApiService(client);
    vi.mocked(client.post).mockResolvedValue({ data: undefined });

    await expect(service.logout({ refresh_token: 'refresh' })).resolves.toBeUndefined();

    expect(client.post).toHaveBeenCalledWith('/auth/logout', {
      refresh_token: 'refresh'
    }, undefined);
  });

  it('loads current user with bearer access token', async () => {
    const client = createMockClient();
    const service = new AuthApiService(client);
    vi.mocked(client.get).mockResolvedValue({
      data: {
        id: 1,
        email: 'user@example.com',
        is_active: true,
        is_superuser: false
      }
    });

    await service.me('access-token');

    expect(client.get).toHaveBeenCalledWith('/auth/me', {
      headers: {
        Authorization: 'Bearer access-token'
      }
    });
  });

  it('normalizes API errors', async () => {
    const client = createMockClient();
    const service = new AuthApiService(client);
    vi.mocked(client.post).mockRejectedValue({
      isAxiosError: true,
      message: 'Request failed',
      response: {
        status: 401,
        data: {
          detail: 'Invalid email or password'
        }
      }
    });

    await expect(
      service.login({ email: 'user@example.com', password: 'wrong-password' })
    ).rejects.toMatchObject({
      name: 'ApiRequestError',
      message: 'Invalid email or password',
      status: 401,
      details: {
        detail: 'Invalid email or password'
      }
    });
  });
});
