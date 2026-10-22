/**
 * Cara 1: Sesión de mesa por código QR anónimo.
 * 
 * Basado en docs/04-MODULOS.md 7.
 * El cliente escanea el QR de la mesa y obtiene un token opaco para solicitar mesero o cuenta.
 */

import Link from 'next/link';

interface TableQRPageProps {
  params: Promise<{
    token: string;
  }>;
}

export default async function TableQRPage({ params }: TableQRPageProps) {
  const { token } = await params;

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '0 20px', fontFamily: 'sans-serif' }}>
      <nav style={{ marginBottom: '20px' }}>
        <Link href="/">← Volver al inicio</Link>
      </nav>

      <header style={{ borderBottom: '1px solid #eee', paddingBottom: '16px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem' }}>Atención en Mesa</h1>
        <p style={{ color: '#666', margin: '4px 0 0' }}>
          Sesión anónima iniciada mediante código QR.
        </p>
      </header>

      <main style={{ marginTop: '24px' }}>
        <div style={{ backgroundColor: '#f0f9ff', border: '1px solid #bae6fd', borderRadius: '8px', padding: '20px' }}>
          <p style={{ margin: 0, fontSize: '0.9rem', color: '#0369a1' }}>
            Token de sesión de mesa: <code>{token}</code>
          </p>
          <p style={{ fontSize: '0.85rem', color: '#0284c7', marginTop: '8px' }}>
            La sesión es anónima y no requiere cuenta personal ni expone el ID interno de la mesa.
          </p>
        </div>
      </main>
    </div>
  );
}

