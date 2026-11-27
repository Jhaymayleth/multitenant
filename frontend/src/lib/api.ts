/**
 * Cliente HTTP único de Lixus.
 *
 * La cookie de sesión es HttpOnly y viaja con credentials: 'include'.
 * El frontend no guarda tokens y el tenant lo resuelve el servidor.
 * Los errores se normalizan: el backend puede devolver { detail } o
 * { error: { code, message, request_id } }.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
const DEFAULT_TIMEOUT_MS = 10_000;

export class AppError extends Error {
  readonly code: string;
  readonly status: number;
  readonly requestId?: string;

  constructor(code: string, message: string, status: number, requestId?: string) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.status = status;
    this.requestId = requestId;
  }
}

interface BackendError {
  detail?: string | { msg?: string; message?: string };
  error?: {
    code?: string;
    message?: string;
    request_id?: string;
  };
}

function normalizeError(payload: BackendError | null, status: number, statusText: string): AppError {
  if (payload?.error?.message) {
    return new AppError(
      payload.error.code || `HTTP_${status}`,
      payload.error.message,
      status,
      payload.error.request_id,
    );
  }

  const detail = payload?.detail;
  const message = typeof detail === 'string'
    ? detail
    : detail?.msg || detail?.message || `No pudimos completar la solicitud (${statusText || status}).`;

  return new AppError(`HTTP_${status}`, message, status);
}

export async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${API_BASE_URL}${path}`;
  const headers = new Headers(options.headers);

  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  let response: Response;
  try {
    response = await fetch(url, {
      ...options,
      headers,
      credentials: 'include',
      signal: options.signal || controller.signal,
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new AppError('NETWORK_ERROR', 'La solicitud tardó demasiado. Intenta de nuevo.', 0);
    }
    throw new AppError('NETWORK_ERROR', 'No pudimos conectar con el servidor.', 0);
  } finally {
    clearTimeout(timeout);
  }

  const isJson = response.headers.get('content-type')?.includes('application/json');
  let payload: unknown = null;
  if (isJson) {
    try {
      payload = await response.json();
    } catch {
      if (response.ok) {
        throw new AppError('PARSE_ERROR', 'El servidor devolvió una respuesta inesperada.', response.status);
      }
    }
  }

  if (!response.ok) {
    throw normalizeError((payload || {}) as BackendError, response.status, response.statusText);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return payload as T;
}

/** Alias conservado para código que ya usaba este nombre. */
export const apiClient = apiFetch;
