/**
 * Cara 2: Monitor de Pedidos y Cocina (CEO).
 * 
 * Basado en docs/04-MODULOS.md 8.
 * Flujo de estados: draft -> confirmed -> in_preparation -> ready -> served -> closed.
 */

export default function CeoOrdersPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Pedidos y Cola de Cocina</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Seguimiento del estado de preparación y despacho</p>
      </header>

      <div style={{ backgroundColor: '#fff', padding: '24px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <p style={{ color: '#475569' }}>
          Monitor en tiempo real de pedidos asociados a mesas presenciales y pedidos a domicilio. Los totales se calculan de manera autoritativa en el servidor.
        </p>
      </div>
    </div>
  );
}

