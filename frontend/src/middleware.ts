/**
 * Middleware de Next.js para Lixus.
 *
 * La URL pública es /r/{slug} (D-124). No hay subdominios por tenant.
 * El middleware solo normaliza la ruta y fija el slug para el servidor;
 * la autorización y el schema los decide el backend (D-106).
 */

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const url = request.nextUrl.clone();
  const requestHeaders = new Headers(request.headers);

  const publicMatch = url.pathname.match(/^\/r\/([^/]+)(\/.*)?$/);
  if (publicMatch) {
    const slug = decodeURIComponent(publicMatch[1]);
    const rest = publicMatch[2] || '/';
    requestHeaders.set('x-tenant-slug', slug);
    requestHeaders.set('x-tenant-area', 'public-site');

    url.pathname = rest;
    return NextResponse.rewrite(url, { request: { headers: requestHeaders } });
  }

  if (url.pathname.startsWith('/admin') || url.pathname.startsWith('/app')) {
    requestHeaders.set('x-tenant-area', 'ceo-portal');
  } else if (url.pathname.startsWith('/portal') || url.pathname.startsWith('/lixus')) {
    requestHeaders.set('x-tenant-area', 'lixus-admin');
  } else if (url.pathname.startsWith('/solicita')) {
    requestHeaders.set('x-tenant-area', 'lixus-onboarding');
  } else {
    requestHeaders.set('x-tenant-area', 'public-site');
  }

  return NextResponse.next({ request: { headers: requestHeaders } });
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|api).*)'],
};
