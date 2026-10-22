## 1. Sectores del proyecto

### 1.1 Arquitectura del proyecto

**Estado:** APROBADA  
**Área:** arquitectura general, SaaS multitenant  
**Decisión:**  
El proyecto se construye como un solo backend multitenant y un solo frontend organizado en áreas claras. Hay tres caras aparentes distintas: la web pública del restaurante, el panel privado del CEO del restaurante y el sitio y panel privado de Lixus para el flujo de nuevos tenants.

El backend es único y es la fuente de autoridad. El frontend puede presentar, pero no decide quién puede entrar, qué tenant puede ver, qué puede hacer un CEO o si un tenant está activo.

**Motivo:**  
Un solo backend evita dividir el núcleo del SaaS en varios sistemas cuando no hace falta. Un solo frontend organizado en áreas evita crear tres repositorios para lo que puede vivir como un proyecto bien separado por responsabilidades. La seguridad queda en el backend, la sesión, la resolución de tenant y los permisos, no en el riesgo de que algo esté “oculto” en el frontend.

**Consecuencias técnicas:**

- Backend único con separación entre lo global de Lixus, lo del tenant y lo público del restaurante.
- Fronteras claras entre:
  - web pública del restaurante
  - panel privado del CEO
  - sitio de solicitud de Lixus
  - panel privado de Lixus
- El tenant se resuelve desde el servidor, no desde lo que el cliente dice.
- La sesión y los permisos protegen el panel del CEO y el panel de Lixus.
- La web pública muestra solo lo que el tenant publica, sin exponer datos internos del SaaS ni datos de otros restaurantes.

### 1.2 Web pública del restaurante

**Estado:** APROBADA  
**Área:** frontend público del tenant  
**Decisión:**  
Cada restaurante tiene su web pública en subdominio propio, con una plantilla común y datos distintos por tenant. Los datos que puede personalizar el CEO son: nombre, logo, colores, teléfono, horarios, texto de presentación, fotos del menú y datos similares. No es un constructor visual libre. La estructura de la web es común, la personalización viene de la configuración del tenant.

**Motivo:**  
El subdominio hace más limpia la presencia del restaurante y reduce la mezcla entre tenants. La plantilla común ayuda a mantener el proyecto ent Ernable sin construir un sitio a medida por restaurante.

**Consecuencias técnicas:**

- La web pública se resuelve por subdominio y por tenant.
- Se carga la configuración pública del tenant correcto.
- No se expone lo que no debe ser público del SaaS ni de otros tenants.
- El panel del CEO puede editar lo público sin tocar la estructura de la plantilla.

### 1.3 Panel del CEO del restaurante

**Estado:** APROBADA  
**Área:** frontend privado del tenant  
**Decisión:**  
El panel del CEO vive en una ruta privada dentro del mismo subdominio del restaurante, por ejemplo `restaurante1.tudominio.com/app` o `restaurante1.tudominio.com/admin`. Solo el CEO del tenant puede acceder. No entra personal. No es un panel de personal.

**Motivo:**  
Mantener el panel dentro del mismo subdominio simplifica el mantenimiento y sigue siendo claramente privado. La seguridad proviene de la sesión y de la verificación del tenant, no de la ruta.

**Consecuencias técnicas:**

- El panel es privado y requiere sesión.
- La sesión identifica al usuario y al tenant.
- Solo el CEO puede entrar a este panel.
- El backend valida el acceso en cada petición.

### 1.4 Sitio de solicitud de Lixus

**Estado:** APROBADA  
**Área:** onboarding SaaS, captación de nuevos tenants  
**Decisión:**  
La solicitud de nuevo restaurante va en un sitio pequeño y separado, por ejemplo un subdominio propio como `solicita.tudominio.com`. Solo recoge el formulario de solicitud. No es el panel del restaurante y no es la web pública del restaurante.

**Motivo:**  
El sitio de solicitud tiene un propósito distinto: entrar al SaaS, no atender clientes del restaurante. Mantenerlo aparte reduce la confusión y acota la superficie del flujo de onboarding.

**Consecuencias técnicas:**

- El formulario genera una solicitud pendiente.
- La solicitud queda registrada para que Lixus la gestione.
- El sitio no crea tenant directamente ni asigna acceso.
- El flujo posterior lo controla Lixus.

### 1.5 Panel de Lixus

**Estado:** APROBADA  
**Área:** gestión SaaS, administración global  
**Decisión:**  
El panel de Lixus es privado para Lixus y se usa para gestionar solicitudes, tenants, membresías, pagos de membresía, creación de tenant, contraseña inicial y notificaciones al futuro CEO.

**Motivo:**  
Aquí es donde Lixus controla el flujo completo de entrada al SaaS. No debe mezclarse con la web pública ni con el panel del restaurante.

**Consecuencias técnicas:**

- La gestión de nuevos restaurantes vive en el lado de Lixus.
- La creación del tenant es un proceso gestionado, no automático desde el formulario.
- La contraseña inicial es parte del flujo de onboarding.
- El panel de Lixus puede ser otra área privada o otro subdominio según convenga.

### 1.6 Separación de responsabilidades de seguridad

**Estado:** APROBADA  
**Área:** seguridad, multitenant, sesión, permisos  
**Decisión:**  
La seguridad se basa en que el backend es la fuente de autoridad, el tenant se resuelve desde el servidor, la sesión protege las áreas privadas y los permisos definen qué puede hacer cada actor. El frontend solo presenta y facilita el uso. No se confía en la ocultación, las rutas ni las validaciones del cliente para proteger nada importante.

**Motivo:**  
Es la forma más robusta de mantener un SaaS multitenant sin dejar fugas por suposiciones del frontend. La separación entre público, privado del restaurante y privado del SaaS es más fácil de mantener cuando el backend decide.

**Consecuencias técnicas:**

- El backend valida la sesión y el tenant en cada acceso privado.
- El panel del CEO solo sirve al CEO del tenant.
- El panel de Lixus solo sirve a Lixus.
- Lo público solo muestra lo que el tenant publica.
- El formulario de solicitud es entrada, no estado de tenant activo.
- La contraseña inicial es parte del proceso gestionado por Lixus.

**Qué incluye esta decisión**

- Un solo backend multitenant.
- Un solo frontend organizado en áreas.
- Web pública del restaurante en subdominio.
- Panel privado del CEO en ruta aparte dentro del mismo subdominio.
- Sitio separado para la solicitud de Lixus.
- Panel privado de Lixus para gestión SaaS.
- Separación de responsabilidades y fronteras claras.

**Qué está fuera de esta decisión**

- Tecnologías internas concretas de auth, rate limiting, archivos e IA.
- Modelo de datos detallado.
- Decisión de subdominios o DNS de producción.
- Plan de despliegue más allá del MVP.
