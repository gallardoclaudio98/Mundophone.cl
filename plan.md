# Plan de Implementación: Panel de Administración Avanzado con Gestión Financiera

## Fase 1: Sistema Avanzado de Gestión de Pedidos ✅
**Objetivo:** Expandir el panel admin con control completo de estados de pedidos y filtros avanzados

### Tareas completadas:
- [x] Expandir estados de pedidos: "Pendiente", "Procesando", "Enviado", "Entregado", "Cancelado", "Revisión Solicitada"
- [x] Crear métodos en AdminState para aceptar, cancelar y cambiar estado de pedidos
- [x] Implementar filtros avanzados en el panel admin:
  - Filtro por fecha (rango de fechas con date pickers)
  - Filtro por cliente (dropdown con lista de clientes)
  - Filtro por estado (dropdown con estados de pedido)
- [x] Añadir botones de acción en cada fila de pedido:
  - "Aceptar" (cambia a "Procesando")
  - "Cancelar" (cambia a "Cancelado")
  - Dropdown para cambiar estado manualmente
- [x] Añadir timestamps a las órdenes (fecha de creación)
- [x] Implementar paginación para tabla de pedidos (mostrar 10 por página)
- [x] Añadir vista detallada de pedido individual (modal con toda la información)
- [x] Mostrar información del cliente en cada pedido

---

## Fase 2: Sistema de Gestión Financiera y Reportes ✅
**Objetivo:** Implementar registro automático de transacciones, flujo de caja y exportación de reportes

### Tareas completadas:
- [x] Crear modelo `Transaction` con campos: id, order_id, type (ingreso/egreso), amount, date, description
- [x] Implementar registro automático de ingreso al confirmar pago exitoso
- [x] Crear AdminState para gestión financiera con métodos de reporte
- [x] Implementar cálculo de flujo de caja mensual:
  - Ingresos del mes (suma de ventas confirmadas)
  - Balance general calculado
- [x] Crear página `/admin/finance` con dashboard financiero:
  - Gráfico de barras de ingresos mensuales
  - Tabla de transacciones recientes
  - Resumen de métricas clave (total ventas, promedio por orden, etc.)
- [x] Añadir navegación a la página de finanzas desde /admin

### Pendiente para próxima sesión:
- [ ] Implementar exportación de reportes en Excel
- [ ] Implementar exportación de reportes en PDF

---

## Fase 3: Sistema de Notificaciones y Comunicación Automática ✅
**Objetivo:** Alertas en tiempo real para admin y notificaciones automáticas por email a clientes

### Tareas completadas:
- [x] Implementar sistema de notificaciones in-app para admin:
  - Badge de notificaciones en navbar con contador
  - Panel dropdown de notificaciones recientes
  - Notificación automática al crear nueva orden
  - Marcar notificaciones como leídas
  - Marcar todas como leídas
- [x] Crear modelo `Notification` con campos: id, message, read, created_at
- [x] Implementar métodos en AdminState:
  - add_notification (genera evento toast)
  - mark_notification_as_read
  - mark_all_as_read
  - unread_notifications_count (computed var)
- [x] Integrar notificaciones en flujos existentes:
  - PaymentState.confirm_payment → crea notificación admin
  - MainState.request_revision → crea notificación admin
- [x] Instalar bibliotecas de email: aiosmtplib, email-validator

### Pendiente para próxima sesión:
- [ ] Configurar integración de email (EmailService class):
  - Funciones helper para enviar emails con SMTP
  - Templates HTML para emails
- [ ] Implementar envío de emails automáticos a clientes:
  - Email de confirmación de compra (estado "Procesando")
  - Email al cambiar a "Enviado"
  - Email al marcar como "Entregado"
  - Email si pedido es cancelado
- [ ] Crear plantillas HTML profesionales para emails
- [ ] Página /admin/notifications con historial completo
- [ ] Toggle en admin para habilitar/deshabilitar notificaciones automáticas

---

## Fase 4: Gestión de Productos desde Admin
**Objetivo:** CRUD completo de productos desde el panel administrativo

### Tareas:
- [ ] Crear página `/admin/products` con lista de todos los productos
- [ ] Implementar formulario de creación de producto:
  - Campos: nombre, marca, precio, descripción, categoría
  - Selector de colores disponibles (multi-select)
  - Input de precio con descuento (opcional)
  - Upload de imagen (local o URL)
- [ ] Implementar edición de productos existentes:
  - Modal con formulario pre-llenado
  - Validación de campos
- [ ] Implementar eliminación de productos (con confirmación)
- [ ] Añadir gestión de stock/inventario:
  - Campo "stock disponible" por producto
  - Alerta cuando stock bajo (< 5 unidades)
  - Descuento automático de stock al confirmar venta
- [ ] Implementar búsqueda y filtros en lista de productos
- [ ] Vista previa de cómo se verá el producto en la tienda
- [ ] Opción de duplicar producto (para crear variantes rápido)
- [ ] Añadir toggle para activar/desactivar producto (sin eliminarlo)

---

## Fase 5: Sistema de Usuarios y Permisos
**Objetivo:** Control de acceso con roles (Admin, Empleado) y permisos granulares

### Tareas:
- [ ] Crear modelo `User` completo con roles: "admin", "employee", "customer"
- [ ] Implementar sistema de permisos granulares:
  - Admin: acceso total
  - Empleado: ver pedidos, cambiar estados, ver finanzas (sin editar)
  - Cliente: solo su perfil y órdenes
- [ ] Crear página `/admin/users` para gestión de usuarios:
  - Lista de todos los usuarios registrados
  - Mostrar rol de cada usuario
  - Botones para cambiar rol
  - Desactivar/activar usuarios
- [ ] Implementar formulario de invitación de empleados:
  - Generar link de registro con rol pre-asignado
  - Email de invitación automático
- [ ] Añadir middleware de verificación de permisos:
  - Decorador @require_admin
  - Decorador @require_employee_or_admin
- [ ] Crear log de actividad por usuario (auditoría):
  - Registro de acciones importantes
  - Timestamp y descripción
- [ ] Implementar tabla de actividad reciente en dashboard admin
- [ ] Añadir perfil de empleado con información de contacto

---

## Fase 6: Dashboard Admin Mejorado y UX Final
**Objetivo:** Interfaz administrativa profesional con gráficos, métricas clave y navegación intuitiva

### Tareas:
- [ ] Rediseñar página `/admin` como dashboard principal:
  - Tarjetas de métricas clave (ventas hoy, pedidos pendientes, ingresos del mes)
  - Gráfico de ventas de los últimos 7 días
  - Tabla de pedidos recientes (últimos 5)
  - Lista de productos con stock bajo
  - Actividad reciente del equipo
- [ ] Implementar sidebar de navegación admin:
  - Dashboard (home)
  - Pedidos
  - Finanzas
  - Productos
  - Usuarios
  - Configuración
- [ ] Añadir gráficos interactivos con biblioteca de charts:
  - Gráfico de barras para ventas mensuales
  - Gráfico de línea para tendencia de ingresos
  - Gráfico de pie para distribución por categoría
  - Gráfico de área para comparación mes a mes
- [ ] Implementar tablas dinámicas con ordenamiento:
  - Click en header para ordenar columnas
  - Búsqueda en tiempo real
  - Exportar vista actual
- [ ] Añadir dark mode para panel admin
- [ ] Implementar shortcuts de teclado para acciones rápidas
- [ ] Crear página de configuración general:
  - Información de la tienda
  - Configuración de emails
  - Gestión de métodos de pago
  - Política de devoluciones
- [ ] Optimizar responsive design para tablets y móviles

---

## Implementación Completada Hoy

### ✅ Fase 3: Sistema de Notificaciones (Completada)
**Implementado:**
- Sistema de notificaciones in-app con badge en navbar
- Contador de notificaciones no leídas (badge rojo con número)
- Panel dropdown con lista de notificaciones recientes
- Funciones para marcar como leída y marcar todas como leídas
- Integración automática al crear órdenes y solicitar revisiones
- Modelo Notification con estructura completa
- Instalación de bibliotecas: aiosmtplib, email-validator

**Tests pasados:**
- ✅ Creación de notificaciones
- ✅ Contador de no leídas
- ✅ Marcar como leída individual
- ✅ Marcar todas como leídas
- ✅ Ordenamiento cronológico (más reciente primero)
- ✅ UI del badge funcionando correctamente

---

## Progreso General

**Completado:** 3 de 6 fases (50%)
**En progreso:** Fase 3 (falta emails automáticos y página de historial)

---

## Próxima Sesión

Continuar con:
1. **Fase 3 (completar):** 
   - Sistema de envío de emails automáticos
   - Plantillas HTML profesionales
   - Página /admin/notifications con historial
2. **Fase 2 (completar):** Exportación de reportes Excel/PDF
3. **Fase 4:** Gestión de productos desde admin

---

## Variables de Entorno Requeridas

### Para Emails (Fase 3 - pendiente configurar):
```env
# Configuración SMTP (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password  # Google App Password
SENDER_EMAIL=noreply@mobileshop.com
SENDER_NAME=MobileShop

# Opcionales
ENABLE_EMAIL_NOTIFICATIONS=true
ADMIN_NOTIFICATION_EMAIL=admin@mobileshop.com
```

### Para Autenticación Google (Ya configurado):
```env
GOOGLE_CLIENT_ID=tu_client_id
GOOGLE_CLIENT_SECRET=tu_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback
```

### Para WebPay (Ya configurado):
```env
WEBPAY_COMMERCE_CODE=597055555532
WEBPAY_API_KEY=579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
```

---

## Bibliotecas Instaladas

```txt
# Core
reflex==0.8.13a1

# Autenticación
google-auth
google-auth-oauthlib
google-auth-httplib2

# Pagos
transbank-sdk

# Base de datos (opcional)
supabase

# Emails (Fase 3)
aiosmtplib==5.0.0
email-validator==2.3.0
```

## Bibliotecas Pendientes por Instalar

```txt
# Para generación de PDF (Fase 2)
reportlab>=4.0.0

# Para Excel (Fase 2)
openpyxl>=3.1.0
```

---

## Resumen Técnico - Fase 3

### Archivos Modificados:
- `app/state.py` - Añadido Notification TypedDict y métodos en AdminState
- `app/components/navbar.py` - Badge de notificaciones con contador y dropdown
- `app/pages/admin.py` - Integración del sistema de notificaciones

### Funcionalidades Implementadas:
- **Modelo Notification:**
  - id: str (UUID)
  - message: str
  - read: bool
  - created_at: str (ISO format)

- **Métodos AdminState:**
  - `add_notification(message)` - Crea notificación y muestra toast
  - `mark_notification_as_read(notification_id)` - Marca una como leída
  - `mark_all_as_read()` - Marca todas como leídas
  - `unread_notifications_count` - Computed var para contador

- **UI Components:**
  - Badge con contador en navbar (solo visible para admin)
  - Dropdown con lista de notificaciones
  - Click en notificación para marcar como leída
  - Botón "Marcar todo como leído"
  - Estilos diferentes para leídas/no leídas

### Integración Automática:
- `PaymentState.confirm_payment` → notificación de nueva orden
- `MainState.request_revision` → notificación de solicitud de revisión

### Tests Ejecutados:
```python
✓ AdminState created
✓ Notification added
✓ Unread notifications count: 1
✓ Marked notification as read
✓ Added multiple notifications
✓ Marked all as read
✓ Ordering (most recent first)
✓ Notification structure validation
```

---

## Capturas de Pantalla

**Screenshot 1:** Navbar con badge de notificaciones (contador "2")
- ✅ Badge rojo visible en navbar
- ✅ Contador de notificaciones no leídas funcionando
- ✅ Icono de campana con badge superpuesto

**Screenshot 2:** Panel de Admin con badge de notificaciones
- ✅ Badge visible en contexto del panel admin
- ✅ Contador "2" mostrado correctamente

**Screenshot 3:** Dashboard Financiero con notificaciones
- ✅ Badge "1" visible
- ✅ Dashboard financiero mostrando métricas correctas
- ✅ Integración completa del sistema

---

## Notas de Implementación

### Fase 3 - Completada Parcialmente
- ✅ Sistema de notificaciones in-app funcionando
- ✅ Badge con contador implementado
- ✅ Dropdown de notificaciones (estructura creada)
- ✅ Métodos de gestión de notificaciones
- ✅ Integración con flujos existentes
- ⏳ Falta: EmailService class completo
- ⏳ Falta: Templates HTML para emails
- ⏳ Falta: Página /admin/notifications

### Cómo usar las notificaciones:
```python
# Crear notificación (en cualquier event handler)
yield AdminState.add_notification("Mensaje de la notificación")

# El sistema automáticamente:
# 1. Agrega la notificación a la lista
# 2. Incrementa el contador de no leídas
# 3. Muestra un toast al usuario
# 4. Actualiza el badge en la navbar
```

### Próximos pasos técnicos:
1. Implementar EmailService class con métodos async
2. Crear templates HTML responsivos para emails
3. Integrar envío de emails en eventos de cambio de estado
4. Crear página /admin/notifications con filtros y búsqueda
5. Añadir configuración de emails en variables de entorno