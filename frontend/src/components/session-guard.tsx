'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

import { AppError } from '@/lib/api';
import { getCurrentUser, type SessionUser } from '@/lib/auth';

interface Props {
  children: React.ReactNode;
  allowedRoles?: string[];
}

export function SessionGuard({ children, allowedRoles }: Props) {
  const router = useRouter();
  const [user, setUser] = useState<SessionUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<string | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setMessage(null);

    getCurrentUser()
      .then((me) => {
        if (!alive) return;
        if (!me.activeTenantId || (me.activeTenant && me.activeTenant.status !== 'active')) {
          setMessage('Restaurante no disponible. Tu acceso está inactivo.');
          return;
        }
        setUser(me);
      })
      .catch((error: unknown) => {
        if (!alive) return;
        if (error instanceof AppError && error.status === 401) {
          router.replace('/login');
          return;
        }
        const text = error instanceof Error ? error.message.toLowerCase() : '';
        if (text.includes('restaurante') || text.includes('membresía') || text.includes('membership')) {
          setMessage('Restaurante no disponible. Tu acceso está inactivo.');
          return;
        }
        setMessage('No pudimos cargar tu sesión. Intenta de nuevo.');
      })
      .finally(() => {
        if (alive) setLoading(false);
      });

    return () => {
      alive = false;
    };
  }, [router, attempt]);

  if (loading) {
    return (
      <div role="status" aria-live="polite" style={{ padding: '32px', color: '#475569' }}>
        Cargando…
      </div>
    );
  }

  if (message) {
    return (
      <div role="alert" style={{ padding: '32px', maxWidth: '560px' }}>
        <h1 style={{ fontSize: '1.3rem', color: '#0f172a' }}>{message}</h1>
        <button
          type="button"
          onClick={() => setAttempt((value) => value + 1)}
          style={{ marginTop: '16px', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}
        >
          Reintentar
        </button>
      </div>
    );
  }

  if (!user) return null;

  if (allowedRoles && user.role && !allowedRoles.includes(user.role)) {
    return (
      <div role="alert" style={{ padding: '32px', maxWidth: '560px' }}>
        <h1 style={{ fontSize: '1.3rem', color: '#0f172a' }}>No tienes acceso a esta sección.</h1>
      </div>
    );
  }

  return <>{children}</>;
}
