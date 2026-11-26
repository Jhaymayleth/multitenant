# 14 — Despliegue en producción (AWS · Nginx · TLS · Docker)

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 1.0
**Estado:** Producción operativa en `https://lixus.coderhivex.com`
**Requisitos:** RAC-06, RAC-07
**Última actualización:** 24 de noviembre de 2026

---

## 1. Resumen en una frase

Pasamos de "una app que corre en un servidor" a **un servicio publicado en internet, con HTTPS renovándose solo, redes separadas, contenedores que se reinician si fallan, y un despliegue que se repite con tres comandos**.

La idea central del día fue esta: **un servidor no es un lugar donde se copian archivos; es una receta que se puede volver a cocinar igual todas las veces.**

---

## 2. La analogía: el restaurante

Piensa en tu aplicación como un restaurante:

| Pieza técnica | En el restaurante | Qué hace en la realidad |
|---|---|---|
| DNS (`lixus.coderhivex.com`) | La dirección en el mapa | Traduce un nombre legible a la IP del servidor |
| **Nginx** | El portero / recepcionista | Recibe a todos en la puerta (80/443), decide a qué área va cada uno y no deja pasar sin verificar |
| **TLS / Let's Encrypt** | La identificación oficial en la puerta | Demuestra que el restaurante es quien dice ser; nadie puede leer lo que hablas con la recepción |
| **Frontend (Next.js)** | El salón y la carta | Lo que el cliente ve, toca y navega |
| **Backend (FastAPI)** | La cocina | Donde se prepara de verdad: reglas, platos, pedidos |
| **Redis** | La pizarra de comandas | Notas rápidas y temporales: rate limiting, sesiones |
| **PostgreSQL (RDS)** | El almacén refrigerado | Donde vive lo importante y no se puede perder |
| **Docker Compose** | El plano de la cocina | Describe qué áreas existen, cómo se conectan y qué necesita cada una |
| **`Dockerfile`** | La receta de cada área | Cómo se monta la cocina y el salón, paso a paso |
| **Healthcheck** | El jefe que pasa cada 15 s a ver si todo respira | Si un área se cae, el sistema lo detecta y la reinicia |
| **`edge` vs `internal`** | Vestíbulo público vs pasillo de servicio | El vestíbulo lo pisa cualquiera; por el pasillo solo pasa el personal |

Cuando decimos "el sitio daba 502" es exactamente: **el portero estaba en la puerta, pero la cocina o el salón no contestaban**.

---

## 3. Qué se construyó (arquitectura final)

```
Internet
   │
   ▼  :80 / :443
┌────────────────────────────────────────────┐
│  nginx  (contenedor, red edge)             │
│  · TLS Let's Encrypt                       │
│  · 301 http → https                        │
│  · HSTS, X-Frame-Options, etc.             │
│  · reto ACME /.well-known/acme-challenge   │
│  · /nginx-health                           │
└───────┬───────────────────────┬────────────┘
        │ /                     │ /api/  y  /health
        ▼                       ▼
┌───────────────┐       ┌─────────────────────┐
│ frontend      │       │ backend             │
│ Next.js 15.1.12│      │ FastAPI + uvicorn   │
│ next start    │       │ 2 workers           │
│ (edge)        │       │ (edge + internal)   │
└───────────────┘       └──────┬──────────────┘
                               │
                  ┌────────────┴─────────────┐
                  ▼                          ▼
          ┌──────────────┐         ┌──────────────────────┐
          │ redis (internal)│      │ RDS PostgreSQL (SSL) │
          │ AOF + maxmemory│      │ schema `platform`    │
          └──────────────┘         └──────────────────────┘
```

| Servicio | Imagen | Red | Puerto publicado | Reinicio |
|---|---|---|---|---|
| `nginx` | `nginx:1.27-alpine` | `edge` | `80`, `443` | `unless-stopped` |
| `frontend` | build `Dockerfile.prod` | `edge` | solo interno `3000` | `unless-stopped` |
| `backend` | build `backend/Dockerfile` | `edge` + `internal` | solo interno `8000` | `unless-stopped` |
| `redis` | `redis:7-alpine` | `internal` | no | `unless-stopped` |

**Detalle importante:** solo Nginx publica puertos al mundo. Frontend, backend y Redis son **invisibles desde internet**; se hablan por la red interna de Docker. Es como un restaurante donde el público solo entra por la puerta principal.

---

## 4. Por qué Nginx y no Caddy

Antes se usaba **Caddy**, que es más simple: obtiene el certificado solo, sin configuración extra.

Se cambió a **Nginx** por tres razones concretas:

1. **Es el estándar de la industria.** Cualquier documentación, tutorial o error que encuentres en internet está escrito para Nginx. Caddy no tiene ese respaldo.
2. **Control explícito.** Con Nginx ves y decides cada cabecera (`X-Forwarded-For`, HSTS, timeouts). Con Caddy buena parte es automático y opaco.
3. **Lo que se evalúa y lo que se encuentra en el trabajo real** es Nginx + Certbot. Saber montarlo vale más.

**Analogía:** Caddy es un portero automático que hace su trabajo; Nginx es un portero al que tú le escribes las instrucciones. Cuesta más dejarlo listo, pero cuando algo falla sabes exactamente qué línea mirar.

---

## 5. Por qué Nginx en contenedor y Certbot fuera

Esta combinación parece rara, y la razón es muy concreta:

| Pieza | Dónde corre | Por qué |
|---|---|---|
| **Nginx** | Contenedor `nginx:1.27-alpine` | La misma imagen corre igual en cualquier servidor. Se actualiza cambiando una etiqueta, no "rompiendo" el sistema operativo. |
| **Certbot** | Contenedor de usar y tirar, lanzado desde un *systemd timer* | El servidor es **Amazon Linux 2023 sobre ARM (aarch64)**, donde el paquete `certbot` no está garantizado y no hay `apt`. La imagen oficial de Certbot evita depender del sistema operativo. |

**Analogía:** Nginx es el portero contratado a tiempo completo (vive en el edificio). Certbot es un técnico que viene un minuto al día a renovar la credencial y se va. No necesitas tener al técnico viviendo dentro.

Y hay un detalle fino: Certbot **no** puede recargar Nginx desde dentro de su propio contenedor (no tiene acceso al proceso). Por eso la renovación solo **renueva el archivo del certificado** y un script posterior hace `docker exec lixus-nginx nginx -s reload`.

```
certbot-lixus.timer  (03:15 UTC, todos los días)
        │
        ▼
certbot-lixus.service
        │  docker run --rm certbot/certbot renew
        ▼
/etc/letsencrypt/…  (se actualiza el certificado)
        │
        ▼
docker exec lixus-nginx nginx -s reload
```

---

## 6. Las piezas, una por una

### 6.1 `docker-compose.prod.yml` — el plano de la cocina

**Qué es:** el archivo que declara los cuatro servicios, sus redes, volúmenes, límites y políticas de reinicio.

**Qué aporta frente al compose de desarrollo:**

| Elemento | Qué hace | Qué te facilita |
|---|---|---|
| `restart: unless-stopped` | Si un contenedor muere, vuelve solo | El sitio no se queda caído porque un proceso falló a las 3 a.m. |
| `healthcheck` | Pregunta cada 15 s "¿estás bien?" | Docker sabe si el servicio *funciona*, no solo si el proceso existe |
| `depends_on: condition: service_healthy` | El backend espera a que Redis esté sano | Evita arranques en falso por carreras de velocidad |
| `networks: edge / internal` | Separa lo público de lo privado | Redis no es accesible desde internet ni por error |
| `deploy.resources.limits` | Techo de CPU y memoria | Un bucle loco no se come el servidor entero |
| `logging: max-size/max-file` | Rota los logs | El disco no se llena con logs de hace un mes |
| `stop_grace_period` | Espera antes de matar | Las peticiones en curso terminan bien |
| `security_opt: no-new-privileges` | Impide escalar privilegios | Un fallo dentro del contenedor no se convierte en root del host |

**Analogía:** el compose de desarrollo es "abre la cocina y cocina". El de producción es "abre la cocina, cierra el pasillo de servicio con llave, pon un extintor, un techo de gas y un registro de lo que se cocinó".

### 6.2 `nginx/nginx.conf` — el manual del portero

Bloques y para qué sirven:

| Bloque | Qué hace | Por qué está |
|---|---|---|
| `server_tokens off` | Oculta la versión de Nginx | No dar pistas a quien busca vulnerabilidades |
| `upstream lixus_frontend / lixus_backend` | Agrupa destinos con `keepalive` | Reutiliza conexiones: más rápido y menos coste |
| `listen 80` + `/.well-known/acme-challenge/` | Sirve el reto de Let's Encrypt | Renovar el certificado sin apagar el sitio |
| `return 301 https://…` | Fuerza HTTPS | Nadie navega en texto plano |
| `listen 443 ssl` + `ssl_protocols TLSv1.2 TLSv1.3` | Cifrado moderno | Se rechazan protocolos viejos e inseguros |
| `add_header Strict-Transport-Security` | HSTS | El navegador recuerda "aquí solo HTTPS" |
| `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` | Cabeceras de seguridad | Mitigan clickjacking y sniffing |
| `location /api/` | Manda a FastAPI con `X-Forwarded-*` | El backend sabe la IP real y el esquema original |
| `location /` | Manda a Next.js con `Upgrade`/`Connection` | WebSockets y streaming funcionan |
| `location = /nginx-health` | Responde `ok` | El healthcheck puede probar el portero sin tocar la app |
| `client_max_body_size 25m` | Límite de subida | Evita que un archivo gigante tumbe el proceso |

**Analogía:** cada `location` es una señal en el vestíbulo: "menú → salón", "cocina → solo personal", "baños → al fondo".

### 6.3 `frontend/Dockerfile.prod` — receta de tres etapas

```
deps      → instala dependencias exactas (npm ci)
build     → compila Next.js (npm run build)
runner    → copia solo lo necesario y corre como usuario sin privilegios
```

**Qué facilita:**

- **Imagen final pequeña:** no lleva el código fuente ni las herramientas de compilación, solo el resultado.
- **Reproducible:** `npm ci` instala exactamente lo que dice el lock.
- **Segura:** corre como `nextjs` (uid 1001), no como root.
- **Correcta:** `next start` sirve la app compilada, no `next dev` (que es lento, con recarga en caliente y no apto para producción).

> Nota real de este proyecto: con `next dev` y `NODE_ENV=production` el middleware fallaba con
> `EvalError: Code generation from strings disallowed`. El error no era del código: era usar el modo
> de desarrollo en producción. `next start` lo resolvió.

**Analogía:** no abres el restaurante con el obrador encendido y las cajas de ingredientes en el salón. `Dockerfile.prod` deja el obrador aparte y en el salón solo pone el plato terminado.

### 6.4 `backend` — uvicorn en modo servidor

```yaml
command: >
  alembic … upgrade head &&
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
    --workers 2 --proxy-headers --forwarded-allow-ips='*'
```

| Opción | Qué hace | Por qué |
|---|---|---|
| `alembic … upgrade head` | Aplica migraciones al arrancar | El contenedor queda operativo sin pasos manuales |
| `exec` | Sustituye el shell por uvicorn | Las señales (SIGTERM) llegan al proceso correcto: apagado limpio |
| `--workers 2` | Dos procesos atendiendo | Aprovecha dos núcleos y no se bloquea con una petición lenta |
| `--proxy-headers` | Confía en `X-Forwarded-*` | Los logs muestran la IP real del cliente, no la de Nginx |

### 6.5 `.env` — qué se queda en el servidor y qué no

**Regla:** el `.env` de producción **nunca** sale del servidor ni se copia al repo ni al entorno local.

| Variable | Producción | Local |
|---|---|---|
| `APP_ENV` | `production` | `local` |
| `DB_HOST` | RDS (`lixus-lab-db…`) | `postgres` (contenedor) |
| `PGSSLMODE` | `require` | **no debe ir** |
| `JWT_SECRET` | secreto real de 64 hex | valor de desarrollo |
| `PLATFORM_ADMIN_KEY` | clave real | clave de desarrollo |

**Analogía:** el `.env` es el llavero. El de casa no sirve para la oficina, y no se deja copia del llavero de la oficina en casa.

### 6.6 `git` en `/opt/lixus` — la receta versionada

Al principio `/opt/lixus` era una carpeta con archivos copiados a mano. Eso produjo el problema más caro del día: **el servidor tenía código del 13 de noviembre y el repo del 24**. Nadie sabía qué versión corría.

Ahora `/opt/lixus` es un **clon real** de la rama `develop`:

```bash
cd /opt/lixus
sudo git pull
```

**Qué facilita:**

- Sabes exactamente qué código corre (`git log -1`).
- Actualizar es `pull`, no "copiar cuatro archivos y rezar".
- Si algo se rompe, `git diff` te dice qué cambió.
- El despliegue deja de depender de la memoria de alguien.

**Analogía:** antes el servidor era un plato cocinado sin receta: rico hoy, imposible de repetir mañana. Ahora es la receta escrita.

---

## 7. Redes: `edge` vs `internal`

```yaml
networks:
  edge:        # público: nginx, frontend, backend
  internal:    # privado: backend, redis
    internal: true
```

| Red | Quién está | Puede salir a internet | Puede recibir de internet |
|---|---|---|---|
| `edge` | nginx, frontend, backend | Sí | Solo a través de nginx |
| `internal` | backend, redis | No | No |

`internal: true` significa que esa red **no tiene puerta a internet**. Redis solo puede hablar con el backend.

**Analogía:** `edge` es el vestíbulo; `internal` es el pasillo de servicio. Un cliente no puede entrar al pasillo, y el personal del pasillo no sale a la calle.

**Efecto secundario que nos mordió:** Docker da un nombre DNS a cada contenedor **mientras está corriendo**. Si el backend está en bucle de reinicio, desaparece del DNS y Nginx dice:

```
host not found in upstream "backend:8000"
```

No era un problema de red: era el síntoma de que el backend estaba caído. **Un contenedor que no vive, no existe para el DNS.**

---

## 8. El efecto dominó: los siete problemas del día

Cada error ocultaba el siguiente. Esta es la cronología real, con la causa y la lección.

| # | Síntoma | Causa real | Arreglo | Analogía |
|---|---|---|---|---|
| 1 | `502` y `host not found in upstream "backend:8000"` | Contenedores de **dos proyectos Compose distintos** (`lixus_default` de `docker-compose.lab.yml` y `lixus_edge` de prod) mezclados | `up -d --force-recreate --remove-orphans` con un solo compose | Dos edificios con el mismo número de puerta: el cartero no sabe dónde entregar |
| 2 | `host not found` aunque la red era correcta | Backend en `Restarting`: sin DNS mientras no está arriba | Arreglar el backend (era el problema de fondo) | El portero no encuentra el número si el inquilino está de viaje |
| 3 | `password authentication failed for user "lixus_admin"` | `DB_USER` no estaba en el `.env`; el valor venía de un `.env` horneado en la imagen | `DB_USER=lixus` en el `.env` (y explícito en el compose) | Usar la llave vieja del inquilino anterior |
| 4 | `no pg_hba.conf entry … no encryption` | RDS exige TLS (`rds.force_ssl=1`) | `PGSSLMODE=require` | La puerta exige hablar por el interfono cifrado, no a gritos |
| 5 | `schema "platform" does not exist` | El schema lo creaba `infra/docker/postgres/init/01-init.sql`, que **solo corre en el Postgres local** | `CREATE SCHEMA IF NOT EXISTS platform;` en RDS | La receta decía "precalienta el horno"; en la cocina nueva nadie lo hizo |
| 6 | `npm ci` fallaba con `Invalid: lock file's picomatch@2.3.2 does not satisfy picomatch@4.0.7` | `package-lock.json` desincronizado **y** conflicto de *peer dependency* (`fdir` pide `^3 \|\| ^4`, `micromatch` pide `^2.3.1`) | Regenerar el lock con **el mismo npm de la imagen** (`10.8.2`) usando `npm install` completo, y validar con `npm ci` real | La lista de compras no coincide con lo que hay en la despensa; y dos recetas piden marcas incompatibles del mismo ingrediente |
| 7 | El tar del certificado "no se creaba" | El **glob lo expandía el shell como `ec2-user`**, que no puede leer `/root` | `sudo sh -c 'ls …'` | Buscabas en el cajón cerrado con la llave equivocada |

### La lección más importante del día

**Un `--dry-run` no es una prueba.** El `npm ci --dry-run` dio "todo bien" porque se ejecutó dentro de una carpeta que ya tenía `node_modules`; el `npm ci` real falló igual. Desde entonces, la regla es: **valida con el comando real, en un directorio limpio, con la misma versión de herramienta que usa producción.**

Y su hermana: **cada capa oculta la siguiente.** Red → DNS → credenciales → TLS → schema → build. No se arregla "el 502"; se arregla el primer eslabón y se vuelve a mirar.

---

## 9. Comandos del día a día

### Desplegar cambios

```bash
cd /opt/lixus
sudo git pull

sudo docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
sudo docker exec lixus-nginx nginx -t && sudo docker exec lixus-nginx nginx -s reload

curl -s -o /dev/null -w "%{http_code}\n" https://lixus.coderhivex.com/
```

> Siempre con `-f docker-compose.prod.yml`: el `docker-compose.yml` del repo es el de **desarrollo**.
> Siempre `sudo git`: `.git` pertenece a `root`.

### Ver estado y logs

```bash
cd /opt/lixus
sudo docker compose -f docker-compose.prod.yml ps
sudo docker compose -f docker-compose.prod.yml logs --tail 50 backend
sudo docker compose -f docker-compose.prod.yml logs -f frontend
```

### Comprobar salud (sin abrir el navegador)

```bash
curl -s https://lixus.coderhivex.com/health; echo
curl -s -o /dev/null -w "%{http_code}\n" https://lixus.coderhivex.com/
curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" http://lixus.coderhivex.com/
```

### Si el build falla

Compose **aborta antes de tocar los contenedores que están corriendo**: el sitio no se cae. Para ver el error real:

```bash
sudo docker compose -f docker-compose.prod.yml build --progress=plain frontend 2>&1 | grep -A3 "npm error" | head -20
```

### Revertir un despliegue

```bash
cd /opt/lixus
sudo git log --oneline -5          # elegir el commit bueno
sudo git checkout <commit>
sudo docker compose -f docker-compose.prod.yml up -d --build
sudo docker exec lixus-nginx nginx -s reload
```

---

## 10. TLS: qué garantiza y cómo se renueva

| Concepto | Qué significa |
|---|---|
| **Let's Encrypt** | Autoridad certificadora gratuita y automática |
| **Certbot** | El programa que pide y renueva el certificado |
| **Reto ACME** | Let's Encrypt pide un archivo en `/.well-known/acme-challenge/…` para demostrar que controlas el dominio |
| **`fullchain.pem`** | Tu certificado + el de la cadena intermedia |
| **`privkey.pem`** | Tu clave privada (nunca sale del servidor) |
| **Renovación** | Cada 60–90 días; el timer lo intenta a diario y solo actúa cuando toca |

Estado actual: certificado emitido, válido hasta **2027-02-22**, respaldo en `/root/letsencrypt-2026-11-24.tar.gz`.

**Analogía:** el certificado es el carnet de identidad del restaurante. Si caduca, los clientes ven "sitio no seguro" y se van. El timer es el técnico que viene cada noche a mirar si hay que renovarlo.

**Límite a respetar:** Let's Encrypt permite **5 duplicados por semana**. Por eso se respalda `/etc/letsencrypt` y no se borra a la ligera.

---

## 11. Seguridad: qué protege qué

| Medida | Protege contra | Dónde está |
|---|---|---|
| HTTPS + HSTS | Interceptar o modificar el tráfico | `nginx.conf` |
| `301` de HTTP a HTTPS | Que alguien navegue en claro | `nginx.conf` |
| Cabeceras `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy` | Clickjacking, sniffing de tipos, fugas de referrer | `nginx.conf` |
| Red `internal` para Redis | Acceso directo a la caché desde internet | `docker-compose.prod.yml` |
| Solo `80`/`443` publicados | Exponer la app o la base por puertos internos | `docker-compose.prod.yml` |
| Contenedores sin privilegios / usuario `nextjs` | Escalada dentro del host | Dockerfiles |
| `X-Platform-Admin-Key` en `/platform/*` | Que cualquiera cree o liste restaurantes | `backend/app/core/dependencies.py` |
| `PGSSLMODE=require` | Tráfico sin cifrar hacia RDS | `.env` / compose |
| `.env` fuera de git | Filtrar secretos en el repo | `.gitignore` |
| Secretos obligatorios (`${VAR:?}`) | Arrancar con el secreto de ejemplo | `docker-compose.prod.yml` |

### Sobre `X-Platform-Admin-Key`

Antes del cambio, `/api/v1/platform/*` estaba **abierto**: cualquiera podía listar o provisionar restaurantes. El código nuevo lo protege con una clave compartida en la cabecera:

```bash
curl -H "X-Platform-Admin-Key: $PLATFORM_ADMIN_KEY" \
  https://lixus.coderhivex.com/api/v1/platform/tenants
```

Hoy: sin clave → `403`, con clave → `200`.

**Limitación honesta:** una clave compartida sirve para el MVP, pero no identifica *quién* llama. Lo correcto a futuro es un JWT de rol `lixus` con auditoría por usuario.

---

## 12. Qué facilita todo esto (resumen)

| Antes | Ahora |
|---|---|
| Copiar archivos a mano por SSM | `git pull` y tres comandos |
| "Creo que corre la versión de ayer" | `git log -1` lo dice |
| Instalar Nginx y Certbot en el sistema operativo | Imágenes versionadas, idénticas en cualquier servidor |
| Renovación del certificado manual | Timer diario automático |
| Redis accesible desde la red pública | Red `internal` aislada |
| Si algo se cae, te enteras por el cliente | Healthchecks + reinicio automático |
| `next dev` en producción | `next start` compilado y sin privilegios |
| Secretos de ejemplo por defecto | Arranque bloqueado si falta un secreto real |
| Logs infinitos llenando el disco | Rotación automática |
| Un build fallido podía dejar el sitio a medias | Compose aborta antes de tocar lo que corre |

---

## 13. Lo que queda pendiente (y por qué importa)

| Prioridad | Tema | Por qué |
|---|---|---|
| Media | `upstream` con `resolver 127.0.0.11 valid=10s` | Evita el `host not found` cuando un contenedor se recrea, y quita la necesidad del `reload` manual |
| Media | Script `ops.sh` (deploy + reload + verificación + backup) | Un solo comando, menos pasos que olvidar |
| Media | CI/CD (GitHub Actions) | Que el despliegue no dependa de pegar comandos por SSM |
| Media | Backups automáticos de RDS verificados | Un schema por tenant mal borrado no tiene vuelta atrás |
| Baja | Mover `DB_USER`, `DB_HOST`, `PGSSLMODE` al `environment` del compose | Hoy están en `.env`; el compose se lee mejor con ellos explícitos |
| Baja | `X-Platform-Admin-Key` → JWT de rol `lixus` | Identidad real y auditoría por usuario |
| Baja | Ampliar cobertura de logs y métricas | Saber qué pasó sin entrar por SSH |
| Baja | Documentar `CREATE SCHEMA platform` como paso 0 de cualquier RDS nueva | Ya nos costó un rato |

---

## 14. Glosario rápido de lo nuevo

| Término | Definición | Analogía |
|---|---|---|
| **Reverse proxy** | Servidor que recibe la petición y la pasa al servicio correcto | El portero que dirige a cada área |
| **TLS** | Cifrado del tráfico entre navegador y servidor | Hablar por el interfono privado, no a gritos |
| **Certificado** | Documento firmado que prueba que el dominio es tuyo | El carnet del restaurante |
| **ACME** | Protocolo para pedir y renovar certificados | El trámite del carnet, hecho solo |
| **Imagen** | Plantilla inmutable de un contenedor | La receta impresa |
| **Contenedor** | Instancia en ejecución de una imagen | El plato ya cocinado |
| **Volumen** | Almacenamiento que sobrevive al contenedor | La despensa, no el plato |
| **Healthcheck** | Prueba periódica de que el servicio responde | El jefe que pasa a ver si respira |
| **Red bridge / `internal`** | Red virtual entre contenedores | Pasillos internos del edificio |
| **DNS interno de Docker** | Nombre del servicio resuelto a su IP | La guía telefónica interna |
| **Multi-stage build** | Construir en etapas y copiar solo el resultado | Cocinar en el obrador y servir solo el plato |
| **`npm ci`** | Instala exactamente lo del lock, sin resolver nada nuevo | Comprar con la lista cerrada, sin improvisar |
| **Lockfile** | Árbol exacto de dependencias con versiones e integridad | La lista de la compra firmada |
| **Peer dependency** | Dependencia que una librería espera que aporte el proyecto | Dos recetas que exigen la misma marca de ingrediente |
| **Proxy headers** | Cabeceras que dicen quién llamó de verdad | La nota del portero: "viene de la mesa 4" |
| **Migración** | Cambio versionado del esquema de base de datos | Reforma del local, con planos y permisos |
| **Schema** | Espacio de nombres dentro de PostgreSQL | Un ala del edificio con su propio plano |

---

## 15. Cronología del día

1. Diagnóstico: `502` y `host not found in upstream`.
2. Descubrimiento de dos proyectos Compose mezclados → un solo compose prod y `--remove-orphans`.
3. Backend en bucle: usuario `lixus_admin` incorrecto → `DB_USER=lixus`.
4. RDS exigía TLS → `PGSSLMODE=require`.
5. Faltaba el schema `platform` en RDS → `CREATE SCHEMA IF NOT EXISTS platform`.
6. Frontend en `next dev` → `Dockerfile.prod` multi-stage con `next start`.
7. `npm ci` roto por lock desincronizado y conflicto de *peer dependency* → lock regenerado con npm 10.8.2 y validado con `npm ci` real.
8. `/opt/lixus` convertido en clon real de `develop`.
9. Backend nuevo desplegado: `/platform/*` ya exige `X-Platform-Admin-Key` (antes estaba abierto).
10. `next` actualizado `15.1.0 → 15.1.12` (CVE-2025-66478), build validado antes de subir.
11. Certificado respaldado en `/root/letsencrypt-2026-11-24.tar.gz`.
12. Verificación final: sitio `200`, health `ok`, HTTP `301`, platform `403/200`.

---

**Fin de `14-DESPLIEGUE-PRODUCCION.md`.**
