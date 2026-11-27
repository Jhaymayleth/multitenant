'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

import { AppError } from '@/lib/api';
import { login } from '@/lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [tenantSlug, setTenantSlug] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const user = await login(email, password, tenantSlug);
      if (!user.activeTenantId || (user.activeTenant && user.activeTenant.status !== 'active')) {
        setError('Restaurante no disponible. Tu acceso está inactivo.');
        return;
      }
      router.push('/admin');
    } catch (caught) {
      if (caught instanceof AppError && caught.status === 403) {
        setError('Restaurante no disponible. Revisa el slug e intenta de nuevo.');
        return;
      }
      setError('No pudimos iniciar sesión. Revisa tus datos.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: '420px', margin: '60px auto', padding: '32px', backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0', fontFamily: 'sans-serif' }}>
      <header style={{ marginBottom: '24px', textAlign: 'center' }}>
        <h1 style={{ margin: 0, fontSize: '1.6rem', color: '#0f172a' }}>Iniciar sesión</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b', fontSize: '0.9rem' }}>Panel de tu restaurante</p>
      </header>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div>
          <label htmlFor="login-email" style={{ display: 'block', fontSize: '0.85rem', color: '#334155', marginBottom: '4px' }}>
            Correo electrónico
          </label>
          <input
            id="login-email"
            type="email"
            required
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            autoComplete="email"
            placeholder="usuario@ejemplo.com"
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box', borderRadius: '4px', border: '1px solid #cbd5e1' }}
          />
        </div>
        <div>
          <label htmlFor="login-password" style={{ display: 'block', fontSize: '0.85rem', color: '#334155', marginBottom: '4px' }}>
            Contraseña
          </label>
          <input
            id="login-password"
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box', borderRadius: '4px', border: '1px solid #cbd5e1' }}
          />
        </div>
        <div>
          <label htmlFor="login-slug" style={{ display: 'block', fontSize: '0.85rem', color: '#334155', marginBottom: '4px' }}>
            Restaurante (slug)
          </label>
          <input
            id="login-slug"
            type="text"
            value={tenantSlug}
            onChange={(event) => setTenantSlug(event.target.value)}
            placeholder="Opcional si solo tienes un restaurante"
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box', borderRadius: '4px', border: '1px solid #cbd5e1' }}
          />
        </div>

        {error && <p role="alert" style={{ color: '#b91c1c', margin: 0 }}>{error}</p>}

        <button
          type="submit"
          disabled={loading}
          style={{ backgroundColor: '#0284c7', color: '#fff', padding: '10px', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: loading ? 'not-allowed' : 'pointer' }}
        >
          {loading ? 'Entrando…' : 'Entrar'}
        </button>
      </form>

      <footer style={{ marginTop: '24px', textAlign: 'center', fontSize: '0.85rem' }}>
        <Link href="/" style={{ color: '#64748b', textDecoration: 'none' }}>
          ← Volver al inicio
        </Link>
      </footer>
    </div>
  );
}
