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
        token_type: 'bearer'
      }
    });

    await service.refresh();

    expect(client.post).toHaveBeenCalledWith('/auth/refresh', undefined, undefined);
  });

  it('logs out with refresh cookie', async () => {
    const client = createMockClient();
    const service = new AuthApiService(client);
    vi.mocked(client.post).mockResolvedValue({ data: undefined });

    await expect(service.logout()).resolves.toBeUndefined();

    expect(client.post).toHaveBeenCalledWith('/auth/logout', undefined, undefined);
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
