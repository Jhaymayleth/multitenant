/**
 * Cara 2: Caja Ligera y Comprobantes (CEO / Cajero).
 * 
 * Basado en docs/02-DECISIONES.md D-070 y docs/04-MODULOS.md 10.
 * Registro de compra, confirmación de pagos, emisión de comprobantes y QR de descarga.
 */

export default function CeoCashierPage() {
  return (
    <div>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#0f172a' }}>Caja Ligera</h1>
        <p style={{ margin: '4px 0 0', color: '#64748b' }}>Confirmación de pagos en efectivo/línea y emisión de comprobantes</p>
      </header>

      <div style={{ backgroundColor: '#fff', padding: '24px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <p style={{ color: '#475569' }}>
          La confirmación del pago libera automáticamente la mesa. Se generan comprobantes ligeros no fiscales con token de descarga mediante QR.
        </p>
      </div>
    </div>
  );
}

