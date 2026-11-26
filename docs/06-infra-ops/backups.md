# Backups y continuidad

**Estado:** Parcial
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería
**Decisión abierta:** PD-29

## 1. Qué se debe proteger

| Activo | Dónde vive | Pérdida |
|---|---|---|
| Datos de tenants | RDS PostgreSQL | Crítica |
| Configuración de plataforma | RDS | Crítica |
| Redis | Contenedor con AOF | Recuperable |
| Imágenes | R2 (previsto) | Alta |
| Secretos y `.env` | Servidor | Crítica |
| Certificados TLS | Servidor | Alta |

## 2. Estado actual

- RDS tiene backups automáticos de AWS, pero no hay evidencia de restauración probada.
- Redis usa AOF y guarda periódicamente.
- No hay backup propio de R2 porque aún no se usa.
- No hay procedimiento escrito de restauración.
- No hay alerta de backup fallido.

## 3. Política propuesta

| Tema | Propuesta |
|---|---|
| Frecuencia | Diaria automática + snapshot antes de migraciones |
| Retención | 30 días |
| RPO | 24 horas |
| RTO | 4 horas |
| Prueba de restauración | Mensual |
| Responsable | Ingeniería |
| Almacenamiento | RDS automated backups + copia cifrada externa |

Las cifras están pendientes en PD-29.

## 4. Procedimiento de restauración

1. Declarar el incidente y congelar cambios.
2. Identificar el punto de restauración.
3. Crear una instancia nueva desde el snapshot; no sobrescribir la actual.
4. Validar schema `platform` y un tenant de prueba.
5. Cambiar la aplicación a la instancia restaurada.
6. Verificar login, menú, pedidos y página pública.
7. Documentar el incidente y la pérdida de datos.

## 5. Prueba mensual

- Restaurar en una instancia aislada.
- Ejecutar una consulta por tenant.
- Verificar que un tenant no ve a otro.
- Medir el tiempo de restauración.
- Registrar el resultado.

## 6. Reglas

1. Un backup no cuenta hasta que se restaura.
2. No se prueba la restauración sobre producción.
3. Los backups se cifran y se acceden con mínimo privilegio.
4. La retención debe cumplir la política legal (PD-16).
5. Un tenant eliminado no se recupera sin decisión y contrato.
