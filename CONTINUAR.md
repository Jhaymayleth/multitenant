# Prompt para continuar

Copia este archivo como primer mensaje en una nueva sesión del agente.

---

Continúa el trabajo de Lixus desde el estado actual del repositorio.

## Contexto obligatorio

1. Lee `docs/README.md`, `docs/00-gobierno/decisiones.md`, `docs/00-gobierno/decisiones-por-definir.md`, `docs/00-gobierno/estado-producto.md` y `docs/01-producto/backlog.md` antes de escribir nada.
2. La fuente de verdad es `docs/`. Los documentos en `docs/_legado/` solo son trazabilidad.
3. El foco es el **MVP de la aplicación** (D-151). No hay operación de venta activa: lo comercial, lo operativo y lo legal están diferidos. La entrevista de producto está cerrada; no reabrir preguntas de negocio, soporte ni legal salvo petición explícita.
4. Todo lo legal está suspendido: ver `docs/08-legal/README.md`. D-150 está cancelada y PD-14 a PD-17 y PD-28 siguen `POR DEFINIR`.
5. Decisiones críticas que ya no se reabren sin evidencia:
   - D-145: Lixus no gestiona caja ni recibe dinero de pedidos. No hay rol de cajero. El pedido se cobra con la pasarela del restaurante; la suscripción con una pasarela separada (D-140).
   - D-124: URL pública por ruta `/r/{slug}`, sin subdominios.
   - D-133 y D-134: límites del producto y prueba de cumplimiento de la promesa.
   - D-146: matriz de permisos con owner, admin, mesero y cocinero.
   - D-147: domicilio con zonas, tarifa fija y entrega propia.
   - D-149: alta asistida con verificación manual y acceso en 48 h.

## Reglas de trabajo

- Documentación en español, tono profesional y directo. Sin lenguaje académico ni términos de entrega evalutable.
- Un `.md` por tema. Features separadas en fichas backend/frontend espejo.
- No inventar datos de negocio: precios, cifras, clientes ni jurisdicción se escriben como `POR DEFINIR` con propuesta.
- Decisiones nuevas desde `D-152`, con ID, fecha, área, decisión, motivo, estado y documentos afectados.
- No tocar código, configuración ni despliegue salvo autorización explícita del usuario. El trabajo es producto y documentación.
- Ningún secreto real en archivos versionados; solo nombres de variables.

## Estado del trabajo

- Árbol documental completo en `docs/00-gobierno` a `docs/08-legal`.
- Especificación técnica de BL-01 lista en `docs/05-frontend/cliente-api.md`.
- Bloqueos P0 del MVP: BL-01, BL-02, BL-03, BL-04, BL-05, BL-06 y BL-08.
- Verificación previa: 0 enlaces rotos y decisiones registradas hasta D-151.

## Próximo paso

1. Confirmar con el usuario si quiere continuar por BL-04 (pedidos con líneas y total en servidor) o BL-03 (menú CRUD).
2. Escribir la ficha técnica con el mismo formato que `docs/05-frontend/cliente-api.md`: objetivo, estado actual, alcance, contrato, diseño, flujos, archivos, estados, pruebas, criterios, dependencias, riesgos y definición de terminado.
3. Actualizar `docs/00-gobierno/indice.md`, `docs/01-producto/backlog.md` y `docs/00-gobierno/changelog.md`.
4. Verificar enlaces, IDs de decisión y que no queden términos académicos.

## Commits

- Usar el usuario registrado del repositorio: `Jhaymayleth <josemrn2006@gmail.com>`.
- No añadir coautores ni líneas `Co-authored-by`.
- Mensajes de commit en español, cortos y descriptivos.
- No hacer push sin que el usuario lo pida.
