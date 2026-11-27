# Índice maestro

**Estado:** Vigente
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Producto

## 1. Gobierno

| Documento | Qué contiene | Estado |
|---|---|---|
| [convenciones.md](convenciones.md) | Nombres, IDs, estados y reglas de escritura | Vigente |
| [glosario.md](glosario.md) | Lenguaje común del producto | Vigente |
| [decisiones.md](decisiones.md) | Decisiones aprobadas y propuestas, desde D-101 | Vigente |
| [decisiones-por-definir.md](decisiones-por-definir.md) | Decisiones abiertas con default propuesto | Vigente |
| [estado-producto.md](estado-producto.md) | Qué existe hoy, qué es parcial y qué no | Vigente |
| [changelog.md](changelog.md) | Historia de producto y documentación | Vigente |

## 2. Producto

| Documento | Qué contiene |
|---|---|
| [identidad.md](../01-producto/identidad.md) | Qué es Lixus, misión, visión y promesa |
| [problema-y-oportunidad.md](../01-producto/problema-y-oportunidad.md) | Dolor del restaurante y espacio de mercado |
| [propuesta-de-valor.md](../01-producto/propuesta-de-valor.md) | Por qué comprar Lixus y no otra cosa |
| [personas.md](../01-producto/personas.md) | Comprador, decisor, usuario interno y cliente final |
| [alcance-producto.md](../01-producto/alcance-producto.md) | Qué incluye y qué no incluye la versión que se vende |
| [marca.md](../01-producto/marca.md) | Tono, identidad, dominio e idiomas |
| [roadmap.md](../01-producto/roadmap.md) | Plan de 6 a 12 meses |
| [backlog.md](../01-producto/backlog.md) | Trabajo priorizado por valor comercial |

## 3. Negocio

| Documento | Qué contiene |
|---|---|
| [modelo-de-negocio.md](../02-negocio/modelo-de-negocio.md) | Cómo gana dinero Lixus |
| [planes-y-precios.md](../02-negocio/planes-y-precios.md) | Estructura de planes y política comercial |
| [competencia.md](../02-negocio/competencia.md) | Alternativas del mercado y diferenciación |
| [go-to-market.md](../02-negocio/go-to-market.md) | Cómo se consigue el primer cliente y los siguientes |
| [metricas.md](../02-negocio/metricas.md) | Métricas de éxito y salud del negocio |

## 4. Arquitectura

| Documento | Qué contiene |
|---|---|
| [sistema.md](../03-arquitectura/sistema.md) | Vista de sistema y componentes |
| [multitenancy.md](../03-arquitectura/multitenancy.md) | Aislamiento, resolución de tenant y aprovisionamiento |
| [modelo-de-datos.md](../03-arquitectura/modelo-de-datos.md) | Entidades globales y por tenant |
| [seguridad.md](../03-arquitectura/seguridad.md) | Autenticación, autorización, sesión y amenazas |
| [integraciones.md](../03-arquitectura/integraciones.md) | R2, correo, IA, pagos y Google |

## 5. Backend

| Documento | Qué contiene |
|---|---|
| [dominios.md](../04-backend/dominios.md) | Mapa de dominios y responsabilidades |
| [api.md](../04-backend/api.md) | Contrato HTTP y convenciones |
| [datos.md](../04-backend/datos.md) | Persistencia y reglas de datos |
| [migraciones.md](../04-backend/migraciones.md) | Cadenas Alembic y operación |
| [features/](../04-backend/features/) | Una ficha por funcionalidad |

## 6. Frontend

| Documento | Qué contiene |
|---|---|
| [areas.md](../05-frontend/areas.md) | Las tres caras del producto |
| [pantallas.md](../05-frontend/pantallas.md) | Mapa de rutas y estados |
| [componentes.md](../05-frontend/componentes.md) | Componentes y patrones de interfaz |
| [cliente-api.md](../05-frontend/cliente-api.md) | Especificación técnica de BL-01 |
| [identidad-api.md](../05-frontend/identidad-api.md) | Especificación técnica de BL-02 |
| [menu-api.md](../05-frontend/menu-api.md) | Especificación técnica de BL-03 |
| [pedidos-api.md](../05-frontend/pedidos-api.md) | Especificación técnica de BL-04 |
| [mesas-qr-api.md](../05-frontend/mesas-qr-api.md) | Especificación técnica de BL-05 |
| [sitio-publico-api.md](../05-frontend/sitio-publico-api.md) | Especificación técnica de BL-06 |
| [accesibilidad.md](../05-frontend/accesibilidad.md) | Criterios de accesibilidad |
| [features/](../05-frontend/features/) | Una ficha por funcionalidad, espejo del backend |

## 7. Infraestructura y operación

| Documento | Qué contiene |
|---|---|
| [entornos.md](../06-infra-ops/entornos.md) | Local, producción y diferencias |
| [despliegue.md](../06-infra-ops/despliegue.md) | Cómo se publica |
| [ci-cd.md](../06-infra-ops/ci-cd.md) | Pipeline y reglas de rama |
| [observabilidad.md](../06-infra-ops/observabilidad.md) | Salud, logs y alertas |
| [backups.md](../06-infra-ops/backups.md) | Copias y restauración |
| [incidentes.md](../06-infra-ops/incidentes.md) | Respuesta y comunicación |
| [variables-entorno.md](../06-infra-ops/variables-entorno.md) | Inventario de variables |
| [soporte-operacion.md](../06-infra-ops/soporte-operacion.md) | Alta, soporte, horarios y SLA |

## 8. Calidad

| Documento | Qué contiene |
|---|---|
| [estrategia-pruebas.md](../07-calidad/estrategia-pruebas.md) | Qué se prueba y cómo |
| [criterios-aceptacion.md](../07-calidad/criterios-aceptacion.md) | Definición de terminado |
| [release.md](../07-calidad/release.md) | Cómo se libera una versión |
| [deuda-tecnica.md](../07-calidad/deuda-tecnica.md) | Deuda conocida y prioridad |
| [aislamiento.md](../07-calidad/aislamiento.md) | Especificación técnica de BL-08 |

## 9. Legal

| Documento | Estado |
|---|---|
| [README.md](../08-legal/README.md) | Todo por definir, diferido |
| [terminos-servicio.md](../08-legal/terminos-servicio.md) | Borrador |
| [politica-privacidad.md](../08-legal/politica-privacidad.md) | Borrador |
| [politica-cookies.md](../08-legal/politica-cookies.md) | Borrador |
| [retencion-datos.md](../08-legal/retencion-datos.md) | Borrador |
| [encargados-tratamiento.md](../08-legal/encargados-tratamiento.md) | Borrador |
| [facturacion.md](../08-legal/facturacion.md) | Borrador |
| [aviso-legal.md](../08-legal/aviso-legal.md) | Borrador |

## 10. Legado

| Documento | Qué contiene |
|---|---|
| [_legado/README.md](../_legado/README.md) | Documentos anteriores y su equivalencia con el árbol vigente |
