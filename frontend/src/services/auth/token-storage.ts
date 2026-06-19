const ACCESS_TOKEN_KEY = 'foosball_rating.access_token';
const REFRESH_TOKEN_KEY = 'foosball_rating.refresh_token';

export interface StoredTokenPair {
  accessToken: string;
  refreshToken: string;
}

export class TokenStorage {
  getTokens(): StoredTokenPair | null {
    const accessToken = window.localStorage.getItem(ACCESS_TOKEN_KEY);
    const refreshToken = window.localStorage.getItem(REFRESH_TOKEN_KEY);

    if (!accessToken || !refreshToken) {
      return null;
    }

    return { accessToken, refreshToken };
  }

  saveTokens(tokens: StoredTokenPair): void {
    window.localStorage.setItem(ACCESS_TOKEN_KEY, tokens.accessToken);
    window.localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refreshToken);
  }

  clearTokens(): void {
    window.localStorage.removeItem(ACCESS_TOKEN_KEY);
    window.localStorage.removeItem(REFRESH_TOKEN_KEY);
  }
}

export const tokenStorage = new TokenStorage();
