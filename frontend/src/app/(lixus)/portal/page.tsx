/**
 * Cara 3: Visión Global de la Plataforma Lixus.
 * 
 * Monitoreo de tenants, estados de aprovisionamiento y salud de la plataforma.
 */

export default function LixusPortalOverviewPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Portal Administrativo Lixus</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Supervisión y control del SaaS multitenant</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>Tenants Activos</h3>
          <p style={{ margin: '8px 0 0', fontSize: '1.8rem', fontWeight: 'bold', color: '#059669' }}>0</p>
        </div>
        <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>En Aprovisionamiento</h3>
          <p style={{ margin: '8px 0 0', fontSize: '1.8rem', fontWeight: 'bold', color: '#d97706' }}>0</p>
        </div>
        <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>Solicitudes Pendientes</h3>
          <p style={{ margin: '8px 0 0', fontSize: '1.8rem', fontWeight: 'bold', color: '#2563eb' }}>0</p>
        </div>
      </div>
    </div>
  );
}

