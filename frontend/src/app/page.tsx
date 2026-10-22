/**
 * Entrada principal del Frontend de Lixus.
 * 
 * Enrutador visual de las tres caras de la arquitectura decidida:
 * 1. Web pública del restaurante (Plantilla por tenant)
 * 2. Panel privado del CEO del restaurante (/admin)
 * 3. Sitio de solicitud y Portal de Lixus (/solicita, /portal)
 */

import Link from 'next/link';

export default function HomePage() {
  return (
    <main style={{ maxWidth: '960px', margin: '40px auto', padding: '0 20px', lineHeight: 1.6 }}>
      <header style={{ borderBottom: '2px solid #eaeaea', paddingBottom: '20px', marginBottom: '30px' }}>
        <h1 style={{ margin: 0, fontSize: '2.4rem', color: '#111' }}>Lixus</h1>
        <p style={{ margin: '8px 0 0', fontSize: '1.2rem', color: '#666' }}>
          Plataforma SaaS Multitenant para Restaurantes — Arquitectura Base
        </p>
      </header>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
        {/* Cara 1: Web Pública del Restaurante */}
        <article style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px', backgroundColor: '#fafafa' }}>
          <h2 style={{ marginTop: 0, fontSize: '1.3rem', color: '#0066cc' }}>1. Web Pública del Restaurante</h2>
          <p style={{ fontSize: '0.95rem', color: '#444' }}>
            Presencia pública por subdominio propio. Plantilla común con personalización de marca, menú publicado y disponibilidad de mesas.
          </p>
          <ul style={{ paddingLeft: '20px', fontSize: '0.9rem' }}>
            <li><Link href="/menu">Ver Menú Público</Link></li>
            <li><Link href="/reservas">Reservas de Mesa</Link></li>
            <li><Link href="/mesa/demo-token">Sesión QR Anónima (Mesa)</Link></li>
          </ul>
        </article>

        {/* Cara 2: Panel Privado del CEO */}
        <article style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px', backgroundColor: '#fafafa' }}>
          <h2 style={{ marginTop: 0, fontSize: '1.3rem', color: '#d97706' }}>2. Panel del CEO del Restaurante</h2>
          <p style={{ fontSize: '0.95rem', color: '#444' }}>
            Ruta privada dentro del subdominio (<code>/admin</code>). Exclusivo para el CEO/Owner del tenant, protegido por sesión y membresía activa.
          </p>
          <ul style={{ paddingLeft: '20px', fontSize: '0.9rem' }}>
            <li><Link href="/admin">Dashboard del Restaurante</Link></li>
            <li><Link href="/admin/menu">Gestión de Catálogo y Menú</Link></li>
            <li><Link href="/admin/mesas">Mesas y Generación de Códigos QR</Link></li>
            <li><Link href="/admin/pedidos">Monitor de Pedidos y Cocina</Link></li>
            <li><Link href="/admin/caja">Caja Ligera y Comprobantes</Link></li>
          </ul>
        </article>

        {/* Cara 3: Ecosistema Lixus */}
        <article style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px', backgroundColor: '#fafafa' }}>
          <h2 style={{ marginTop: 0, fontSize: '1.3rem', color: '#059669' }}>3. Solicitud y Portal de Lixus</h2>
          <p style={{ fontSize: '0.95rem', color: '#444' }}>
            Sitio externo de captación y portal administrativo del SaaS para aprovisionamiento, verificación de tenants y planes.
          </p>
          <ul style={{ paddingLeft: '20px', fontSize: '0.9rem' }}>
            <li><Link href="/solicita">Solicitud de Nuevo Restaurante (Onboarding)</Link></li>
            <li><Link href="/portal">Portal Administrativo Lixus</Link></li>
            <li><Link href="/portal/tenants">Gestión de Tenants y Schemas</Link></li>
            <li><Link href="/portal/planes">Gestión de Planes y Suscripciones</Link></li>
          </ul>
        </article>
      </section>

      <footer style={{ marginTop: '50px', borderTop: '1px solid #eee', paddingTop: '20px', fontSize: '0.85rem', color: '#777' }}>
        <strong>Aislamiento Multitenant:</strong> PostgreSQL con schema global <code>platform</code> y schemas aislados <code>tenant_&lt;id&gt;</code>.
        Resolución autoritativa desde el servidor (FastAPI) con <code>SET LOCAL search_path</code>.
      </footer>
    </main>
  );
}
