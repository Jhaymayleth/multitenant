/**
 * Cara 1: Menú público del restaurante.
 * 
 * Basado en docs/02-DECISIONES.md 1.2 y docs/04-MODULOS.md 6.
 * Muestra el catálogo activo del tenant resuelto sin exigir sesión.
 */

import Link from 'next/link';

export default function PublicMenuPage() {
  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '0 20px', fontFamily: 'sans-serif' }}>
      <nav style={{ marginBottom: '20px' }}>
        <Link href="/">← Volver al inicio</Link>
      </nav>

      <header style={{ borderBottom: '1px solid #eee', paddingBottom: '16px' }}>
        <h1 style={{ margin: 0, fontSize: '2rem' }}>Menú del Restaurante</h1>
        <p style={{ color: '#666', margin: '4px 0 0' }}>
          Platos y bebidas disponibles en este restaurante.
        </p>
      </header>

      <main style={{ marginTop: '24px' }}>
        <div style={{ border: '1px dashed #ccc', borderRadius: '8px', padding: '32px', textAlign: 'center', color: '#555' }}>
          <h3>Catálogo Multitenant</h3>
          <p>
            Los productos y categorías se consumen de <code>/api/v1/public/{'{slug}'}/menu</code> garantizando aislamiento de datos.
          </p>
        </div>
      </main>
    </div>
  );
}

