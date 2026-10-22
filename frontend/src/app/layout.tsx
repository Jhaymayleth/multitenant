/**
 * Layout base del sitio frontend de Lixus.
 * 
 * Provee la estructura HTML base y los estilos compartidos para:
 * 1. Web pública del restaurante
 * 2. Panel privado del CEO
 * 3. Portal y solicitud de Lixus
 */

import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Lixus — SaaS Multitenant para Restaurantes',
  description: 'Plataforma integral multitenant para gestión y presencia digital de restaurantes',
  // Cuando exista un favicon real, colocarlo en src/app/favicon.ico
  // y descomentar la siguiente línea:
  // icons: { icon: '/favicon.ico' },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body style={{ margin: 0, fontFamily: 'system-ui, -apple-system, sans-serif' }}>
        {children}
      </body>
    </html>
  );
}
