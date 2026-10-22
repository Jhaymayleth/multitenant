/**
 * Cara 3: Sitio de Solicitud de Lixus (Onboarding).
 * 
 * Basado en docs/02-DECISIONES.md 1.4 y docs/03-ARQUITECTURA.md 4.3.
 * Sitio separado (ej. solicita.tudominio.com). Solo recoge la solicitud de nuevo restaurante.
 * No crea tenant de manera automática; registra la solicitud pendiente para gestión de Lixus.
 */

import Link from 'next/link';

export default function LixusSolicitaPage() {
  return (
    <div style={{ maxWidth: '640px', margin: '60px auto', padding: '0 20px', fontFamily: 'sans-serif' }}>
      <nav style={{ marginBottom: '24px' }}>
        <Link href="/">← Volver al inicio</Link>
      </nav>

      <header style={{ borderBottom: '2px solid #059669', paddingBottom: '16px', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '2rem', color: '#065f46' }}>Lixus Onboarding</h1>
        <p style={{ margin: '6px 0 0', color: '#047857' }}>
          Solicita la incorporación de tu restaurante a la plataforma SaaS
        </p>
      </header>

      <div style={{ backgroundColor: '#ecfdf5', border: '1px solid #a7f3d0', borderRadius: '8px', padding: '24px' }}>
        <h3 style={{ margin: '0 0 12px', color: '#065f46' }}>Formulario de Captación</h3>
        <p style={{ color: '#047857', fontSize: '0.95rem', lineHeight: 1.5 }}>
          Esta página vive separada de la web de los restaurantes. El formulario recopila los datos del establecimiento
          (nombre, razón social, correo de contacto, teléfono) para ser evaluado y aprovisionado por el equipo de Lixus.
        </p>
      </div>
    </div>
  );
}

