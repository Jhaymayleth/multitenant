'use client';

import { useState } from 'react';

import { apiFetch } from '@/lib/api';

interface Props {
  children: React.ReactNode;
}

/**
 * Guard interino del portal de Lixus (D-117).
 * La clave se pide en memoria, nunca se guarda ni se versiona.
 */
export function PlatformGuard({ children }: Props) {
  const [key, setKey] = useState('');
  const [authorized, setAuthorized] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!key.trim()) return;

    setLoading(true);
    setError(null);
    try {
      await apiFetch('/platform/tenants', {
        headers: { 'X-Platform-Admin-Key': key.trim() },
      });
      setAuthorized(true);
    } catch {
      setError('Clave de plataforma incorrecta o no configurada.');
    } finally {
      setLoading(false);
    }
  }

  if (authorized) return <>{children}</>;

  return (
    <div style={{ maxWidth: '420px', margin: '48px auto', padding: '24px', background: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
      <h1 style={{ fontSize: '1.3rem', color: '#0f172a' }}>Acceso de plataforma</h1>
      <p style={{ color: '#64748b' }}>
        Ingresa la clave de administración de Lixus para continuar. No se guarda en el navegador.
      </p>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <label htmlFor="platform-key" style={{ fontSize: '0.85rem', color: '#334155' }}>
          Clave de plataforma
        </label>
        <input
          id="platform-key"
          type="password"
          value={key}
          onChange={(event) => setKey(event.target.value)}
          autoComplete="off"
          style={{ padding: '10px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
        />
        <button type="submit" disabled={loading} style={{ padding: '10px', borderRadius: '4px', background: '#0f172a', color: '#fff', cursor: 'pointer' }}>
          {loading ? 'Verificando…' : 'Entrar'}
        </button>
        {error && <p role="alert" style={{ color: '#b91c1c' }}>{error}</p>}
      </form>
    </div>
  );
}
