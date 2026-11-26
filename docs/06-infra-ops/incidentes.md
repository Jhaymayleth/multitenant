# Incidentes

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Operación / Ingeniería

## 1. Severidad

| Nivel | Definición | Ejemplo | Respuesta objetivo |
|---|---|---|---|
| S1 | Servicio caído o pérdida de datos | 502 general, schema corrupto | Inmediata |
| S2 | Función crítica inoperante | No se pueden cobrar pedidos | < 1 hora |
| S3 | Función degradada | QR lento, página pública intermitente | < 4 horas |
| S4 | Molestia menor | Texto incorrecto, estilo | Siguiente release |

Los tiempos son propuestas hasta definir SLA (PD-12).

## 2. Flujo

1. **Detectar:** alerta, reporte de cliente o revisión.
2. **Registrar:** hora, síntoma, alcance, tenant afectado.
3. **Contener:** evitar que empeore; rollback si aplica.
4. **Comunicar:** avisar al dueño y a los clientes afectados.
5. **Resolver:** corregir y verificar.
6. **Cerrar:** registrar causa y acción preventiva.

## 3. Comunicación

- Canal interno: POR DEFINIR.
- Canal con clientes: correo o WhatsApp del restaurante.
- Mensaje inicial: qué pasa, a quién afecta, qué se está haciendo, cuándo se actualiza.
- No se promete una hora de solución sin diagnóstico.

## 4. Roles

| Rol | Responsabilidad |
|---|---|
| Responsable de incidente | Coordina y decide |
| Ingeniería | Diagnostica y corrige |
| Operación | Comunica y atiende al cliente |
| Dueño | Decide impacto comercial |

En la etapa inicial, una persona puede cubrir varios roles.

## 5. Postmortem

Para S1 y S2:

- Línea de tiempo.
- Causa raíz.
- Impacto y datos afectados.
- Qué funcionó y qué no.
- Acciones con dueño y fecha.
- Cambio en documentación o pruebas.

## 6. Incidentes previsibles

| Incidente | Primer paso |
|---|---|
| 502 en el sitio | Revisar Nginx, backend y logs |
| Certificado vencido | Renovar y recargar Nginx |
| Base de datos inaccesible | Revisar RDS, credenciales y TLS |
| Tenant no puede entrar | Verificar estado, membresía y cookie |
| Pedido duplicado | Revisar idempotencia y logs |
| Página pública en 404 | Verificar publicación y slug |
| Backup fallido | Revisar RDS y alerta |

## 7. Registro

Cada incidente se documenta con `INC-##` y se enlaza desde el changelog si cambió el producto.
