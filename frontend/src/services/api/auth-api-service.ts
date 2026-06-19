import { ApiService } from './api-service';

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface TokenPairResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}

export interface CurrentUserResponse {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

export class AuthApiService extends ApiService {
  register(payload: RegisterRequest): Promise<TokenPairResponse> {
    return this.post<RegisterRequest, TokenPairResponse>('/auth/register', payload);
  }

  login(payload: LoginRequest): Promise<TokenPairResponse> {
    return this.post<LoginRequest, TokenPairResponse>('/auth/login', payload);
  }

  refresh(payload: RefreshTokenRequest): Promise<TokenPairResponse> {
    return this.post<RefreshTokenRequest, TokenPairResponse>('/auth/refresh', payload);
  }

  logout(payload: RefreshTokenRequest): Promise<void> {
    return this.post<RefreshTokenRequest, void>('/auth/logout', payload);
  }

  me(accessToken: string): Promise<CurrentUserResponse> {
    return this.get<CurrentUserResponse>('/auth/me', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
  }
}

export const authApiService = new AuthApiService();
