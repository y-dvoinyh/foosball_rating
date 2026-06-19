import { isAxiosError } from 'axios';

export class ApiRequestError extends Error {
  constructor(
    message: string,
    readonly status?: number,
    readonly details?: unknown
  ) {
    super(message);
    this.name = 'ApiRequestError';
  }
}

export function toApiRequestError(error: unknown): ApiRequestError {
  if (isAxiosError(error)) {
    const status = error.response?.status;
    const details = error.response?.data;
    const message =
      getErrorMessage(details) || error.message || 'API request failed';

    return new ApiRequestError(message, status, details);
  }

  if (error instanceof Error) {
    return new ApiRequestError(error.message);
  }

  return new ApiRequestError('API request failed');
}

function getErrorMessage(details: unknown): string | undefined {
  if (
    typeof details === 'object' &&
    details !== null &&
    'detail' in details &&
    typeof details.detail === 'string'
  ) {
    return details.detail;
  }

  return undefined;
}
