/**
 * Tipos de datos compartidos de Lixus.
 * 
 * Basado en las especificaciones de docs/07-MODELO-DATOS.md
 */

import { UserRole, TenantStatus, OrderStatus, TableStatus, PaymentStatus } from './constants';

export interface User {
  id: string;
  email: string;
  fullName: string;
  status: 'pending' | 'active' | 'disabled';
  lastLoginAt: string | null;
  createdAt: string;
}

export interface Tenant {
  id: string;
  slug: string;
  name: string;
  legalName?: string | null;
  schemaName: string; // "tenant_<12hex>"
  status: TenantStatus;
  timezone: string;
  currency: string;
  contactEmail?: string | null;
  createdAt: string;
  activatedAt?: string | null;
}

export interface TenantMembership {
  id: string;
  tenantId: string;
  userId: string;
  role: UserRole;
  status: 'invited' | 'active' | 'disabled' | 'revoked';
  createdAt: string;
}

export interface MenuItem {
  id: string;
  categoryId: string | null;
  name: string;
  description?: string | null;
  priceCents: number;
  imageUrl?: string | null;
  isActive: boolean;
}

export interface MenuCategory {
  id: string;
  name: string;
  displayOrder: number;
  isActive: boolean;
}

export interface Table {
  id: string;
  number: string;
  capacity: number;
  status: TableStatus;
  qrToken?: string | null;
}

export interface Order {
  id: string;
  tableSessionId?: string | null;
  status: OrderStatus;
  paymentStatus: PaymentStatus;
  totalCents: number;
  notes?: string | null;
  createdAt: string;
}

export interface TenantPublicSiteConfig {
  displayName: string;
  tagline?: string | null;
  description?: string | null;
  logoUrl?: string | null;
  heroImageUrl?: string | null;
  colorPrimary?: string | null;
  colorSecondary?: string | null;
  address?: string | null;
  hours?: Record<string, string>;
  isPublished: boolean;
}

