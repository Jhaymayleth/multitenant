/**
 * Cara 3: Planes y Suscripciones de Lixus.
 * 
 * Basado en docs/04-MODULOS.md 12 y docs/07-MODELO-DATOS.md 2.5.
 * Control centralizado de capacidades y límites sin dispersión de lógica en el código.
 */

export default function LixusPlanesPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Planes y Capacidades</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Definición de paquetes, límites y capacidades por nivel</p>
      </header>

      <div style={{ backgroundColor: '#fff', padding: '24px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <p style={{ color: '#475569' }}>
          Gestión de planes SaaS: <code>basic</code>, <code>intermediate</code>, <code>advanced</code>.
          Las capacidades se guardan como JSONB en <code>platform.plans</code>.
        </p>
      </div>
    </div>
  );
}

