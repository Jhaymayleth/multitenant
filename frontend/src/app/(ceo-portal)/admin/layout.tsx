/**
 * Cara 2: Layout del Panel del CEO del restaurante.
 * 
 * Basado en docs/02-DECISIONES.md 1.3 y docs/03-ARQUITECTURA.md 4.2.
 * Vive en ruta privada /admin dentro del subdominio del tenant.
 * Solo para el CEO del restaurante; el backend valida sesión y rol en cada petición.
 */

import Link from 'next/link';

export default function CeoPortalLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      {/* Sidebar de navegación del CEO */}
      <aside style={{ width: '250px', backgroundColor: '#1e293b', color: '#f8fafc', padding: '24px 16px' }}>
        <div style={{ marginBottom: '32px' }}>
          <h2 style={{ margin: 0, fontSize: '1.25rem', color: '#38bdf8' }}>Lixus CEO</h2>
          <p style={{ margin: '4px 0 0', fontSize: '0.8rem', color: '#94a3b8' }}>Panel del Restaurante</p>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <Link href="/admin" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            📊 Resumen
          </Link>
          <Link href="/admin/menu" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            🍽️ Menú y Catálogo
          </Link>
          <Link href="/admin/mesas" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            🪑 Mesas y QR
          </Link>
          <Link href="/admin/pedidos" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            🧾 Pedidos y Cocina
          </Link>
          <Link href="/admin/caja" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            💳 Caja Ligera
          </Link>
          <Link href="/admin/configuracion" style={{ color: '#e2e8f0', textDecoration: 'none', padding: '8px', borderRadius: '4px' }}>
            ⚙️ Configuración Web
          </Link>
          <div style={{ marginTop: '24px', borderTop: '1px solid #334155', paddingTop: '16px' }}>
            <Link href="/" style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.85rem' }}>
              ← Salir al inicio
            </Link>
          </div>
        </nav>
      </aside>

      {/* Contenido principal del panel */}
      <main style={{ flex: 1, backgroundColor: '#f1f5f9', padding: '32px' }}>
        {children}
      </main>
    </div>
  );
}

