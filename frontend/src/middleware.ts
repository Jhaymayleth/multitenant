/**
 * Middleware de Next.js para Lixus Multitenant.
 * 
 * Responsabilidades:
 * 1. Resuelve el subdominio o contexto del tenant (ej. 'solicita', 'portal', o '<slug-restaurante>').
 * 2. Inyecta cabeceras 'x-tenant-slug' y 'x-tenant-area' para el renderizado del servidor.
 * 3. Encamina las peticiones según las tres caras de la arquitectura:
 *    - Web pública del restaurante (subdominio)
 *    - Panel del CEO (/admin o /app dentro del subdominio)
 *    - Captación y gestión de Lixus ('solicita' o '/lixus')
 */

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const url = request.nextUrl.clone();
  const hostname = request.headers.get('host') || '';

  // Determinar subdominio (soporta localhost con puertos o subdominios reales)
  // Ejemplos: 'solicita.lixus.local:3000' -> 'solicita', 'don-pepe.lixus.com' -> 'don-pepe'
  const currentHost = hostname.split(':')[0];
  const parts = currentHost.split('.');

  let subdomain: string | null = null;
  // Si tiene al menos 3 partes (ej. restaurante1.lixus.com) o 2 partes en .local
  if (parts.length > 2 || (parts.length === 2 && parts[1] === 'local')) {
    subdomain = parts[0];
  }

  // Soporte de query param ?tenant=slug en entorno local de desarrollo
  const queryTenant = url.searchParams.get('tenant');
  const tenantSlug = queryTenant || (subdomain && !['www', 'api', 'localhost'].includes(subdomain) ? subdomain : null);

  const requestHeaders = new Headers(request.headers);

  if (tenantSlug) {
    requestHeaders.set('x-tenant-slug', tenantSlug);
  }

  // Clasificación de área de negocio
  if (tenantSlug === 'solicita' || url.pathname.startsWith('/solicita')) {
    requestHeaders.set('x-tenant-area', 'lixus-onboarding');
  } else if (tenantSlug === 'portal' || url.pathname.startsWith('/lixus') || url.pathname.startsWith('/portal')) {
    requestHeaders.set('x-tenant-area', 'lixus-admin');
  } else if (url.pathname.startsWith('/admin') || url.pathname.startsWith('/app')) {
    requestHeaders.set('x-tenant-area', 'ceo-portal');
  } else {
    requestHeaders.set('x-tenant-area', 'public-site');
  }

  return NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
}

export const config = {
  matcher: [
    /*
     * Aplica a todas las rutas excepto archivos estáticos (_next, imágenes, favicon).
     */
    '/((?!_next/static|_next/image|favicon.ico|api).*)',
  ],
};
