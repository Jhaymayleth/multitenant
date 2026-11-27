# Glosario

**Estado:** Vigente
**Última revisión:** 27 de noviembre de 2026

| Término | Definición |
|---|---|
| **Lixus** | Plataforma SaaS que vende y opera el servicio. También se usa para el rol de administración global. |
| **Tenant** | Restaurante independiente dentro de la plataforma. Su límite físico es un schema de PostgreSQL. |
| **Schema `platform`** | Espacio global: usuarios, tenants, membresías, planes, suscripciones, verificación, idempotencia global y auditoría. |
| **Schema del tenant** | Espacio exclusivo del restaurante: menú, personal, mesas, pedidos, reservas, pagos y configuración. |
| **CEO del restaurante** | Persona que contrata el servicio y responde por el negocio. Es el comprador y el rol `owner`. |
| **Personal** | Empleados del restaurante con roles operativos: administrador, mesero y cocinero. No hay rol de cajero (D-145). |
| **Cliente registrado** | Persona con cuenta en un restaurante para reservar mesa o descargar comprobantes. El pedido se toma en mesa (D-156). |
| **Cliente anónimo de mesa** | Persona que escanea el QR de una mesa y envía solicitudes sin crear cuenta. |
| **Visitante** | Persona que consulta la página pública o el menú sin cuenta. |
| **Domicilio** | Canal que Lixus no gestiona. Se registra como pedido simple; zonas, tarifas y entrega los resuelve el restaurante por fuera (D-155). |
| **Etiqueta de mesa** | Nombre visible de la mesa, generado por el backend desde la configuración del restaurante. No es el identificador interno (D-158). |
| **Membresía** | Relación técnica entre una identidad y un tenant con un rol. No es una suscripción comercial. |
| **Suscripción** | Plan comercial que paga el tenant. El personal y los clientes no pagan licencia. |
| **Aprovisionamiento** | Creación de un tenant: schema, tablas, usuario CEO, membresía y configuración inicial. |
| **Tenant context** | Datos de la petición (tenant, schema, rol, usuario) que el backend resuelve y valida. |
| **Aislamiento** | Garantía de que un tenant no puede leer ni escribir datos de otro. |
| **Idempotencia** | Repetir una operación con la misma clave produce un solo efecto y la misma respuesta. |
| **Rate limiting** | Límite de peticiones por usuario, tenant o IP para evitar abuso. |
| **Webhook** | Evento HTTP que un proveedor externo envía a Lixus, firmado para verificar origen e integridad. |
| **Comprobante** | Documento simple de compra con numeración por tenant y token temporal. No tiene validez fiscal. |
| **Cobro de pedidos** | Pago del total con la pasarela del restaurante; Lixus solo confirma y emite comprobante. No es caja ni POS (D-145). |
| **SSG / ISR** | Generación estática y regeneración incremental para páginas públicas. |
| **CSR** | Renderizado en el cliente para paneles privados. |
| **RLS** | Row Level Security de PostgreSQL. Defensa adicional, no sustituto del schema por tenant. |
| **R2** | Cloudflare R2, almacenamiento de archivos compatible con S3. |
| **Slug** | Identificador legible del restaurante usado en la URL pública. |
