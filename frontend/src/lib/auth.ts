/**
 * Sesión del usuario. La autoridad es el backend: aquí solo se guarda
 * el contexto en memoria mientras vive la página.
 */

import { apiFetch } from './api';

export interface TenantBrief {
  id: string;
  slug: string;
  name: string;
  status: string;
}

export interface SessionUser {
  id: string;
  email: string;
  fullName: string;
  activeTenantId: string | null;
  activeTenant: TenantBrief | null;
  role: string | null;
  permissions: string[];
}

interface MeResponse {
  id: string;
  email: string;
  full_name?: string;
  fullName?: string;
  active_tenant_id?: string | null;
  active_tenant?: TenantBrief | null;
  role?: string | null;
  permissions?: string[];
}

interface TokenResponse {
  token_type: string;
  expires_in_minutes: number;
}

interface MessageResponse {
  message: string;
}

export async function getCurrentUser(): Promise<SessionUser> {
  const me = await apiFetch<MeResponse>('/auth/me');
  return {
    id: me.id,
    email: me.email,
    fullName: me.full_name || me.fullName || '',
    activeTenantId: me.active_tenant_id ?? me.active_tenant?.id ?? null,
    activeTenant: me.active_tenant ?? null,
    role: me.role ?? null,
    permissions: me.permissions ?? [],
  };
}

export async function login(email: string, password: string, tenantSlug?: string): Promise<SessionUser> {
  const body: Record<string, string> = { email, password };
  const slug = tenantSlug?.trim();
  if (slug) {
    body.tenant_slug = slug;
  }

  await apiFetch<TokenResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(body),
  });

  return getCurrentUser();
}

export async function logout(): Promise<void> {
  try {
    await apiFetch<MessageResponse>('/auth/logout', { method: 'POST' });
  } catch {
    // La sesión local se limpia aunque falle la llamada.
  }
}

export async function switchTenant(tenantId: string): Promise<SessionUser> {
  await apiFetch<TokenResponse>('/auth/switch-tenant', {
    method: 'POST',
    body: JSON.stringify({ tenant_id: tenantId }),
  });
  return getCurrentUser();
}
