import { ApiService } from './api-service';

export interface HealthResponse {
  status: string;
  database: string;
}

export class HealthApiService extends ApiService {
  getHealth(): Promise<HealthResponse> {
    return this.get<HealthResponse>('/health');
  }
}

export const healthApiService = new HealthApiService();
