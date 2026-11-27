/**
 * Constantes de dominio y roles de Lixus.
 * 
 * Basado en las especificaciones de docs/04-MODULOS.md y docs/07-MODELO-DATOS.md
 */

export const ROLES = {
  OWNER: 'owner',     // CEO del restaurante (único con control total)
  ADMIN: 'admin',     // Administrador delegado
  WAITER: 'waiter',   // Mesero
  COOK: 'cook',       // Cocinero (sin rol de cajero, D-145)
} as const;

export type UserRole = (typeof ROLES)[keyof typeof ROLES];

export const TENANT_STATUS = {
  PROVISIONING: 'provisioning',
  PROVISIONING_FAILED: 'provisioning_failed',
  PENDING_VERIFICATION: 'pending_verification',
  ACTIVE: 'active',
  SUSPENDED: 'suspended',
  CANCELLED: 'cancelled',
} as const;

export type TenantStatus = (typeof TENANT_STATUS)[keyof typeof TENANT_STATUS];

export const ORDER_STATUS = {
  DRAFT: 'draft',
  CONFIRMED: 'confirmed',
  IN_PREPARATION: 'in_preparation',
  READY: 'ready',
  SERVED: 'served',
  CLOSED: 'closed',
  CANCELLED: 'cancelled',
} as const;

export type OrderStatus = (typeof ORDER_STATUS)[keyof typeof ORDER_STATUS];

export const TABLE_STATUS = {
  AVAILABLE: 'available',
  OCCUPIED: 'occupied',
  PENDING_PAYMENT: 'pending_payment',
  RESERVED: 'reserved',
  INACTIVE: 'inactive',
} as const;

export type TableStatus = (typeof TABLE_STATUS)[keyof typeof TABLE_STATUS];

export const PAYMENT_STATUS = {
  UNPAID: 'unpaid',
  PENDING: 'pending',
  PAID: 'paid',
  REFUNDED: 'refunded',
  NOT_APPLICABLE: 'not_applicable',
} as const;

export type PaymentStatus = (typeof PAYMENT_STATUS)[keyof typeof PAYMENT_STATUS];

