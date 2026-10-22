/**
 * Cara 2: Configuración Visual de la Web Pública (CEO).
 * 
 * Basado en docs/02-DECISIONES.md 1.2 y docs/04-MODULOS.md 11.
 * Personalización permitida: nombre, logo, colores primario/secundario, horarios y presentación.
 */

export default function CeoSiteConfigPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Configuración de la Web Pública</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Personaliza la identidad visual de la web del restaurante</p>
      </header>

      <div style={{ backgroundColor: '#fff', padding: '24px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <p style={{ color: '#475569' }}>
          Personalización sobre la plantilla estándar del restaurante (colores, logo, datos de contacto y horarios). Se almacena en la tabla singleton <code>tenant_settings</code>.
        </p>
      </div>
    </div>
  );
}

