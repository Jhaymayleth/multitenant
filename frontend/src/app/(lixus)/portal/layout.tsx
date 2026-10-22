/**
 * Cara 3: Layout del Portal de Administración de Lixus.
 * 
 * Basado en docs/02-DECISIONES.md 1.5 y docs/03-ARQUITECTURA.md 4.3.
 * Panel exclusivo para el personal de Lixus (Platform Admins).
 * Gestiona tenants, creación de schemas, planes, verificaciones y suspensiones.
 */

import Link from 'next/link';

export default function LixusPortalLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      {/* Sidebar de administración Lixus */}
      <aside style={{ width: '260px', backgroundColor: '#0f172a', color: '#f8fafc', padding: '24px 16px' }}>
        <div style={{ marginBottom: '32px' }}>
          <h2 style={{ margin: 0, fontSize: '1.3rem', color: '#34d399' }}>Lixus Platform</h2>
          <p style={{ margin: '4px 0 0', fontSize: '0.8rem', color: '#94a3b8' }}>Administración Global SaaS</p>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <Link href="/portal" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            🌐 Panorama Global
          </Link>
          <Link href="/portal/tenants" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            🏢 Tenants y Schemas
          </Link>
          <Link href="/portal/planes" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            📦 Planes y Suscripciones
          </Link>
          <div style={{ marginTop: '24px', borderTop: '1px solid #334155', paddingTop: '16px' }}>
            <Link href="/" style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.85rem' }}>
              ← Salir al inicio
            </Link>
          </div>
        </nav>
      </aside>

      {/* Área de trabajo de plataforma */}
      <main style={{ flex: 1, backgroundColor: '#f8fafc', padding: '32px' }}>
        {children}
      </main>
    </div>
  );
}

