/**
 * Cara 2: Administración de Mesas y QR (CEO).
 * 
 * Basado en docs/04-MODULOS.md 7.
 * Configuración de mesas, capacidad y regeneración de tokens opacos para códigos QR.
 */

export default function CeoTablesPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Mesas y Códigos QR</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Control de distribución y generación de QR anónimos</p>
      </header>

      <div style={{ backgroundColor: '#fff', padding: '24px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <p style={{ color: '#475569' }}>
          Gestión de mesas para el restaurante. Los tokens QR son tokens criptográficos opacos que vinculan a la mesa sin exponer el ID interno.
        </p>
      </div>
    </div>
  );
}

