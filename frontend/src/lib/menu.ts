/** Cliente del dominio de menú. El contrato usa snake_case como el backend. */

import { apiFetch } from './api';

export interface MenuCategory {
  id: string;
  name: string;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface MenuProduct {
  id: string;
  category_id: string | null;
  name: string;
  description: string | null;
  price_cents: number;
  image_url: string | null;
  display_order: number;
  is_active: boolean;
  is_published: boolean;
  created_at: string;
}

interface CategoryPayload {
  name: string;
  display_order: number;
  is_active?: boolean;
}

interface ProductPayload {
  category_id: string;
  name: string;
  description?: string | null;
  price_cents: number;
  image_url?: string | null;
  is_active?: boolean;
  is_published?: boolean;
  display_order?: number;
}

export const listCategories = () => apiFetch<MenuCategory[]>('/tenant/menu/categories');
export const listProducts = () => apiFetch<MenuProduct[]>('/tenant/menu/products');

export const createCategory = (payload: CategoryPayload) =>
  apiFetch<MenuCategory>('/tenant/menu/categories', { method: 'POST', body: JSON.stringify(payload) });

export const updateCategory = (id: string, payload: CategoryPayload) =>
  apiFetch<MenuCategory>(`/tenant/menu/categories/${id}`, { method: 'PUT', body: JSON.stringify(payload) });

export const deleteCategory = (id: string) =>
  apiFetch<void>(`/tenant/menu/categories/${id}`, { method: 'DELETE' });

export const createProduct = (payload: ProductPayload) =>
  apiFetch<MenuProduct>('/tenant/menu/products', { method: 'POST', body: JSON.stringify(payload) });

export const updateProduct = (id: string, payload: ProductPayload) =>
  apiFetch<MenuProduct>(`/tenant/menu/products/${id}`, { method: 'PUT', body: JSON.stringify(payload) });

export const deleteProduct = (id: string) =>
  apiFetch<void>(`/tenant/menu/products/${id}`, { method: 'DELETE' });

export const publishProduct = (id: string, isPublished: boolean) =>
  apiFetch<MenuProduct>(`/tenant/menu/products/${id}/publication`, {
    method: 'PATCH',
    body: JSON.stringify({ is_published: isPublished }),
  });

export const reorderProduct = (id: string, displayOrder: number) =>
  apiFetch<MenuProduct>(`/tenant/menu/products/${id}/order`, {
    method: 'PATCH',
    body: JSON.stringify({ display_order: displayOrder }),
  });
