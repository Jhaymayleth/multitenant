/**
 * Cara 3: Gestión de Tenants y Schemas de Lixus.
 * 
 * Basado en docs/03-ARQUITECTURA.md 2.3 y docs/04-MODULOS.md 3.
 * Flujo de aprovisionamiento: estado 'provisioning' -> creación de schema tenant_<12hex> ->
 * ejecución de migraciones de tenant -> inserción de CEO y membresía 'owner'.
 */

export default function LixusTenantsPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Gestión de Tenants</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Aprovisionamiento, schemas y verificación de restaurantes</p>
      </header>

      <div style={{ backgroundColor: '#fff', padding: '24px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <h3 style={{ marginTop: 0 }}>Ciclo de Vida del Tenant</h3>
        <p style={{ color: '#475569', fontSize: '0.95rem' }}>
          La creación de tenant es una operación protegida e idempotente mediante <code>Idempotency-Key</code> ejecutada en <code>/api/v1/platform/tenants</code>.
          Cada tenant dispone de su propio schema aislado PostgreSQL (ej. <code>tenant_a1b2c3d4e5f6</code>) y no comparte tablas con otros restaurantes.
        </p>
      </div>
    </div>
  );
}

