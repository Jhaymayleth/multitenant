'use client';

import { useCallback, useEffect, useState } from 'react';

import { AppError } from '@/lib/api';
import {
  createCategory,
  createProduct,
  deleteCategory,
  deleteProduct,
  listCategories,
  listProducts,
  publishProduct,
  reorderProduct,
  updateCategory,
  updateProduct,
  type MenuCategory,
  type MenuProduct,
} from '@/lib/menu';

const inputStyle = { width: '100%', padding: '8px', boxSizing: 'border-box' as const, borderRadius: '4px', border: '1px solid #cbd5e1' };
const buttonStyle = { padding: '8px 12px', borderRadius: '4px', border: 'none', cursor: 'pointer', background: '#0284c7', color: '#fff' };

export default function CeoMenuPage() {
  const [categories, setCategories] = useState<MenuCategory[]>([]);
  const [products, setProducts] = useState<MenuProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [categoryName, setCategoryName] = useState('');
  const [categoryOrder, setCategoryOrder] = useState(0);
  const [editingCategory, setEditingCategory] = useState<string | null>(null);

  const [productName, setProductName] = useState('');
  const [productDescription, setProductDescription] = useState('');
  const [productPrice, setProductPrice] = useState('');
  const [productCategory, setProductCategory] = useState('');
  const [productPublished, setProductPublished] = useState(false);
  const [editingProduct, setEditingProduct] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const message = (caught: unknown) =>
    caught instanceof AppError ? caught.message : 'No pudimos completar la acción. Intenta de nuevo.';

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [categoryList, productList] = await Promise.all([listCategories(), listProducts()]);
      setCategories(categoryList.filter((item) => item.is_active));
      setProducts(productList.filter((item) => item.is_active));
    } catch (caught) {
      setError(message(caught));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  function resetCategoryForm() {
    setCategoryName('');
    setCategoryOrder(0);
    setEditingCategory(null);
  }

  function resetProductForm() {
    setProductName('');
    setProductDescription('');
    setProductPrice('');
    setProductCategory('');
    setProductPublished(false);
    setEditingProduct(null);
  }

  async function saveCategory(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError(null);
    try {
      const payload = { name: categoryName, display_order: categoryOrder, is_active: true };
      if (editingCategory) await updateCategory(editingCategory, payload);
      else await createCategory(payload);
      resetCategoryForm();
      await load();
    } catch (caught) {
      setError(message(caught));
    } finally {
      setSaving(false);
    }
  }

  async function saveProduct(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError(null);
    try {
      const payload = {
        category_id: productCategory || categories[0]?.id || '',
        name: productName,
        description: productDescription || null,
        price_cents: Number(productPrice),
        image_url: null,
        is_active: true,
        is_published: productPublished,
        display_order: 0,
      };
      if (!payload.category_id) throw new AppError('INVALID_CATEGORY', 'Crea una categoría antes de agregar productos.', 422);
      if (!Number.isInteger(payload.price_cents) || payload.price_cents < 1) {
        throw new AppError('INVALID_PRICE', 'El precio debe ser un número entero mayor que cero.', 422);
      }
      if (editingProduct) await updateProduct(editingProduct, payload);
      else await createProduct(payload);
      resetProductForm();
      await load();
    } catch (caught) {
      setError(message(caught));
    } finally {
      setSaving(false);
    }
  }

  async function removeCategory(id: string) {
    if (!window.confirm('¿Retirar esta categoría?')) return;
    try {
      await deleteCategory(id);
      await load();
    } catch (caught) {
      setError(message(caught));
    }
  }

  async function removeProduct(id: string) {
    if (!window.confirm('¿Retirar este producto? No afecta pedidos anteriores.')) return;
    try {
      await deleteProduct(id);
      await load();
    } catch (caught) {
      setError(message(caught));
    }
  }

  async function togglePublication(product: MenuProduct) {
    try {
      await publishProduct(product.id, !product.is_published);
      await load();
    } catch (caught) {
      setError(message(caught));
    }
  }

  async function move(product: MenuProduct, delta: number) {
    try {
      await reorderProduct(product.id, Math.max(0, product.display_order + delta));
      await load();
    } catch (caught) {
      setError(message(caught));
    }
  }

  if (loading) return <p role="status">Cargando menú…</p>;

  return (
    <div style={{ fontFamily: 'sans-serif', color: '#0f172a' }}>
      <h1 style={{ fontSize: '1.8rem', margin: 0 }}>Menú y catálogo</h1>
      <p style={{ color: '#64748b' }}>Categorías y productos del restaurante. Los cambios se guardan en tu schema.</p>

      {error && <p role="alert" style={{ color: '#b91c1c' }}>{error} <button type="button" onClick={() => void load()}>Reintentar</button></p>}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px', marginTop: '24px' }}>
        <section style={{ background: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h2 style={{ fontSize: '1.1rem' }}>{editingCategory ? 'Editar categoría' : 'Nueva categoría'}</h2>
          <form onSubmit={saveCategory} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <label htmlFor="category-name">Nombre</label>
            <input id="category-name" required minLength={2} maxLength={80} value={categoryName} onChange={(event) => setCategoryName(event.target.value)} style={inputStyle} />
            <label htmlFor="category-order">Orden</label>
            <input id="category-order" type="number" min={0} value={categoryOrder} onChange={(event) => setCategoryOrder(Number(event.target.value))} style={inputStyle} />
            <div style={{ display: 'flex', gap: '8px' }}>
              <button type="submit" disabled={saving} style={buttonStyle}>{saving ? 'Guardando…' : 'Guardar'}</button>
              {editingCategory && <button type="button" onClick={resetCategoryForm}>Cancelar</button>}
            </div>
          </form>

          <h3 style={{ fontSize: '1rem', marginTop: '24px' }}>Categorías</h3>
          {categories.length === 0 ? <p>Aún no hay categorías. Crea la primera.</p> : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {categories.map((category) => (
                <li key={category.id} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #e2e8f0' }}>
                  <span>{category.display_order}. {category.name}</span>
                  <span>
                    <button type="button" onClick={() => { setEditingCategory(category.id); setCategoryName(category.name); setCategoryOrder(category.display_order); }}>Editar</button>
                    {' '}
                    <button type="button" onClick={() => void removeCategory(category.id)}>Retirar</button>
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section style={{ background: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h2 style={{ fontSize: '1.1rem' }}>{editingProduct ? 'Editar producto' : 'Nuevo producto'}</h2>
          <form onSubmit={saveProduct} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <label htmlFor="product-category">Categoría</label>
            <select id="product-category" value={productCategory} onChange={(event) => setProductCategory(event.target.value)} style={inputStyle} required>
              <option value="">Selecciona una categoría</option>
              {categories.map((category) => <option key={category.id} value={category.id}>{category.name}</option>)}
            </select>
            <label htmlFor="product-name">Nombre</label>
            <input id="product-name" required minLength={2} maxLength={80} value={productName} onChange={(event) => setProductName(event.target.value)} style={inputStyle} />
            <label htmlFor="product-description">Descripción</label>
            <input id="product-description" maxLength={500} value={productDescription} onChange={(event) => setProductDescription(event.target.value)} style={inputStyle} />
            <label htmlFor="product-price">Precio (centavos)</label>
            <input id="product-price" type="number" min={1} required value={productPrice} onChange={(event) => setProductPrice(event.target.value)} style={inputStyle} />
            <label style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <input type="checkbox" checked={productPublished} onChange={(event) => setProductPublished(event.target.checked)} />
              Publicado en la página
            </label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button type="submit" disabled={saving} style={buttonStyle}>{saving ? 'Guardando…' : 'Guardar'}</button>
              {editingProduct && <button type="button" onClick={resetProductForm}>Cancelar</button>}
            </div>
          </form>
        </section>
      </div>

      <section style={{ background: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0', marginTop: '20px' }}>
        <h2 style={{ fontSize: '1.1rem' }}>Productos</h2>
        {products.length === 0 ? <p>No hay productos. Agrega el primero.</p> : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                <th>Orden</th><th>Producto</th><th>Precio</th><th>Publicado</th><th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
                  <td>
                    <button type="button" onClick={() => void move(product, -1)} aria-label={`Subir ${product.name}`}>↑</button>
                    {' '}{product.display_order}{' '}
                    <button type="button" onClick={() => void move(product, 1)} aria-label={`Bajar ${product.name}`}>↓</button>
                  </td>
                  <td>{product.name}</td>
                  <td>{product.price_cents} centavos</td>
                  <td>
                    <input
                      type="checkbox"
                      checked={product.is_published}
                      onChange={() => void togglePublication(product)}
                      aria-label={`Publicar ${product.name}`}
                    />
                  </td>
                  <td>
                    <button
                      type="button"
                      onClick={() => {
                        setEditingProduct(product.id);
                        setProductName(product.name);
                        setProductDescription(product.description || '');
                        setProductPrice(String(product.price_cents));
                        setProductCategory(product.category_id || '');
                        setProductPublished(product.is_published);
                      }}
                    >
                      Editar
                    </button>
                    {' '}
                    <button type="button" onClick={() => void removeProduct(product.id)}>Retirar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
