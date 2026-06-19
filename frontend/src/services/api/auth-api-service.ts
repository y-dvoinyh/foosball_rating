import { ApiService } from './api-service';

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AccessTokenResponse {
  access_token: string;
  token_type: 'bearer';
}

export interface CurrentUserResponse {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

export class AuthApiService extends ApiService {
  register(payload: RegisterRequest): Promise<AccessTokenResponse> {
    return this.post<RegisterRequest, AccessTokenResponse>('/auth/register', payload);
  }

  login(payload: LoginRequest): Promise<AccessTokenResponse> {
    return this.post<LoginRequest, AccessTokenResponse>('/auth/login', payload);
  }

  refresh(): Promise<AccessTokenResponse> {
    return this.post<undefined, AccessTokenResponse>('/auth/refresh');
  }

  logout(): Promise<void> {
    return this.post<undefined, void>('/auth/logout');
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
