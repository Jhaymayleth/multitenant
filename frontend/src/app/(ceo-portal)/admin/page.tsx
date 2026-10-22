/**
 * Cara 2: Dashboard principal del CEO del restaurante.
 * 
 * Resumen de indicadores del restaurante: mesas activas, pedidos y caja.
 */

export default function CeoDashboardPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Dashboard del Restaurante</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Vista general de operaciones en tiempo real</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
        <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>Mesas Ocupadas</h3>
          <p style={{ margin: '8px 0 0', fontSize: '1.8rem', fontWeight: 'bold', color: '#0f172a' }}>0 / 12</p>
        </div>
        <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>Pedidos Activos</h3>
          <p style={{ margin: '8px 0 0', fontSize: '1.8rem', fontWeight: 'bold', color: '#0f172a' }}>0</p>
        </div>
        <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>Ventas Hoy</h3>
          <p style={{ margin: '8px 0 0', fontSize: '1.8rem', fontWeight: 'bold', color: '#0f172a' }}>$0 COP</p>
        </div>
      </div>
    </div>
  );
}

