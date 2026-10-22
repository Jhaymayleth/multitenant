/**
 * Cara 2: Administración del Menú (CEO).
 * 
 * Basado en docs/04-MODULOS.md 6.
 * CRUD de categorías y productos con precios enteros en centavos y fotos.
 */

export default function CeoMenuPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Gestión del Menú</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Categorías y productos ofertados</p>
      </header>

      <div style={{ backgroundColor: '#fff', padding: '24px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <p style={{ color: '#475569' }}>
          Estructura de catálogo del tenant. Los cambios se persisten en el schema del tenant respectivo vía <code>/api/v1/tenant/menu</code>.
        </p>
      </div>
    </div>
  );
}

