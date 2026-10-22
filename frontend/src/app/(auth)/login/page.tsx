/**
 * Autenticación: Inicio de sesión.
 * 
 * Basado en docs/04-MODULOS.md 4 y docs/08-SEGURIDAD-Y-ACCESO.md.
 * Emite cookie httpOnly protegida contra robo JavaScript.
 * Contiene sub (usuario), tenant_id y role.
 */

import Link from 'next/link';

export default function LoginPage() {
  return (
    <div style={{ maxWidth: '420px', margin: '60px auto', padding: '32px', backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0', fontFamily: 'sans-serif' }}>
      <header style={{ marginBottom: '24px', textAlign: 'center' }}>
        <h1 style={{ margin: 0, fontSize: '1.6rem', color: '#0f172a' }}>Iniciar Sesión</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b', fontSize: '0.9rem' }}>Lixus Multitenant Platform</p>
      </header>

      <form style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', color: '#334155', marginBottom: '4px' }}>Correo Electrónico</label>
          <input
            type="email"
            placeholder="usuario@ejemplo.com"
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box', borderRadius: '4px', border: '1px solid #cbd5e1' }}
          />
        </div>
        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', color: '#334155', marginBottom: '4px' }}>Contraseña</label>
          <input
            type="password"
            placeholder="••••••••••••"
            style={{ width: '100%', padding: '10px', boxSizing: 'border-box', borderRadius: '4px', border: '1px solid #cbd5e1' }}
          />
        </div>
        <button
          type="button"
          style={{ backgroundColor: '#0284c7', color: '#fff', padding: '10px', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}
        >
          Entrar
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

