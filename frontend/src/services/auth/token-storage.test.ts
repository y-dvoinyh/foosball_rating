import { beforeEach, describe, expect, it } from 'vitest';

import { TokenStorage } from './token-storage';

describe('TokenStorage', () => {
  const storage = new TokenStorage();

  beforeEach(() => {
    window.localStorage.clear();
  });

  it('returns null when token pair is incomplete', () => {
    expect(storage.getTokens()).toBeNull();

    window.localStorage.setItem('foosball_rating.access_token', 'access');

    expect(storage.getTokens()).toBeNull();
  });

  it('saves and reads token pair', () => {
    storage.saveTokens({
      accessToken: 'access',
      refreshToken: 'refresh'
    });

    expect(storage.getTokens()).toEqual({
      accessToken: 'access',
      refreshToken: 'refresh'
    });
  });

  it('clears token pair', () => {
    storage.saveTokens({
      accessToken: 'access',
      refreshToken: 'refresh'
    });

    storage.clearTokens();

    expect(storage.getTokens()).toBeNull();
  });
});
