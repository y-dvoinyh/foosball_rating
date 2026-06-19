import type { AxiosInstance, AxiosRequestConfig } from 'axios';

import { api } from 'boot/axios';
import { toApiRequestError } from './api-error';

export class ApiService {
  constructor(protected readonly client: AxiosInstance = api) {}

  protected async get<ResponseData>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<ResponseData> {
    return this.request<ResponseData>(() => this.client.get(url, config));
  }

  protected async post<RequestData, ResponseData>(
    url: string,
    data?: RequestData,
    config?: AxiosRequestConfig
  ): Promise<ResponseData> {
    return this.request<ResponseData>(() => this.client.post(url, data, config));
  }

  private async request<ResponseData>(
    requestFn: () => Promise<{ data: ResponseData }>
  ): Promise<ResponseData> {
    try {
      const response = await requestFn();
      return response.data;
    } catch (error) {
      throw toApiRequestError(error);
    }
  }
}
