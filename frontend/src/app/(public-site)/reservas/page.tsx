/**
 * Cara 1: Reservas del restaurante.
 * 
 * Basado en docs/04-MODULOS.md 9.
 * Consulta disponibilidad pública y permite agendar a clientes registrados.
 */

import Link from 'next/link';

export default function PublicReservationsPage() {
  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '0 20px', fontFamily: 'sans-serif' }}>
      <nav style={{ marginBottom: '20px' }}>
        <Link href="/">← Volver al inicio</Link>
      </nav>

      <header style={{ borderBottom: '1px solid #eee', paddingBottom: '16px' }}>
        <h1 style={{ margin: 0, fontSize: '2rem' }}>Reserva tu Mesa</h1>
        <p style={{ color: '#666', margin: '4px 0 0' }}>
          Disponibilidad en tiempo real para este restaurante.
        </p>
      </header>

      <main style={{ marginTop: '24px' }}>
        <div style={{ border: '1px dashed #ccc', borderRadius: '8px', padding: '32px', textAlign: 'center', color: '#555' }}>
          <h3>Disponibilidad de Mesas</h3>
          <p>
            Consulta pública de horarios sin solapamientos con índice de concurrencia en la base de datos.
          </p>
        </div>
      </main>
    </div>
  );
}

