# 💰 Pagos - Sistema de Gestión de Gastos

Un sistema completo de gestión de gastos empresariales construido con **Streamlit** y **Supabase**.

## 🚀 Características

### 👥 Gestión de Roles
- **Admin**: Control total del sistema, gestión de usuarios, reportes
- **Solicitador**: Crear y gestionar solicitudes de gastos
- **Aprobador**: Revisar y aprobar/rechazar gastos
- **Pagador**: Marcar gastos como pagados
- **Vista**: Consultar y visualizar gastos (solo lectura)

### 📋 Funcionalidades Principales
- ✅ **Autenticación segura** con Supabase Auth
- 📝 **Formularios inteligentes** para solicitudes de gastos
- 🔄 **Flujo de trabajo** completo: Solicitud → Aprobación → Pago
- 📊 **Dashboard y reportes** con gráficos interactivos
- 🔍 **Filtros avanzados** y búsqueda
- 📱 **Interfaz responsive** y moderna
- 🎨 **Diseño intuitivo** con emojis y colores

### 🛠️ Tecnologías

- **Frontend**: Streamlit (Python)
- **Backend**: Supabase (PostgreSQL + Auth)
- **Gráficos**: Plotly
- **Base de datos**: PostgreSQL
- **Autenticación**: Supabase Auth

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd Pagos
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto:
```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_ANON_KEY=tu_clave_anonima_de_supabase
```

### 4. Ejecutar la aplicación
```bash
streamlit run app.py
```

## 🗂️ Estructura del Proyecto

```
Pagos/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── .env                  # Variables de entorno
├── functions/            # Funciones de base de datos
│   ├── f_cud.py         # Create, Update, Delete
│   └── f_read.py        # Read operations
├── admin/               # Páginas de administrador
│   ├── dashboard.py     # Dashboard principal
│   ├── users.py         # Gestión de usuarios
│   ├── expenses.py      # Gestión de gastos
│   └── reports.py       # Reportes y analytics
├── solicitador/         # Páginas de solicitador
│   ├── new_expense.py   # Nuevo gasto
│   └── my_expenses.py   # Mis gastos
├── aprovador/           # Páginas de aprobador
│   ├── pending.py       # Gastos pendientes
│   ├── approved.py      # Gastos aprobados
│   └── rejected.py      # Gastos rechazados
├── pagador/             # Páginas de pagador
│   ├── to_pay.py        # Gastos por pagar
│   └── paid.py          # Gastos pagados
├── vista/               # Páginas de vista
│   ├── overview.py      # Vista general
│   └── expenses.py      # Vista de gastos
└── db_setup/           # Configuración de base de datos
    ├── database_schema.md
    ├── database_schema.sql
    └── streamlit_updates.txt
```

## 🔧 Configuración de Base de Datos

### Tablas Principales

1. **users**: Información de usuarios
2. **user_roles**: Roles asignados a usuarios
3. **expenses**: Gastos del sistema
4. **expense_attachments**: Archivos adjuntos (futuro)

### Scripts de Configuración

Los scripts de configuración se encuentran en `db_setup/`:
- `database_schema.sql`: Esquema completo de la base de datos
- `database_schema.md`: Documentación del esquema

## 🎯 Uso del Sistema

### 1. Login
- Acceder con email y contraseña
- El sistema detecta automáticamente los roles del usuario

### 2. Navegación
- **Sidebar dinámico**: Se adapta según los roles del usuario
- **Navegación fluida**: Entre páginas sin recargar

### 3. Roles y Permisos

#### 👑 Admin
- Dashboard con métricas completas
- Gestión de usuarios y roles
- Reportes y analytics
- Control total de gastos

#### 📝 Solicitador
- Crear nuevos gastos
- Ver historial de solicitudes
- Editar gastos pendientes

#### ✅ Aprobador
- Revisar gastos pendientes
- Aprobar/rechazar con comentarios
- Ver historial de decisiones

#### 💳 Pagador
- Ver gastos aprobados por pagar
- Marcar como pagados
- Registrar detalles de pago

#### 👁️ Vista
- Consultar todos los gastos
- Ver métricas generales
- Sin permisos de edición

## 🚀 Características Avanzadas

### 📊 Dashboard Interactivo
- Métricas en tiempo real
- Gráficos con Plotly
- Filtros dinámicos

### 🔍 Búsqueda y Filtros
- Búsqueda por texto
- Filtros por estado, categoría, fecha
- Rango de montos

### 📈 Reportes
- Exportación a Excel
- Gráficos de tendencias
- Análisis por período

### 🎨 UI/UX Moderna
- Emojis para mejor UX
- Colores por estado
- Diseño responsive
- Navegación intuitiva

## 🔒 Seguridad

- **Autenticación**: Supabase Auth
- **Autorización**: Roles basados en base de datos
- **Validación**: Formularios con validación
- **Auditoría**: Logs de todas las acciones

## 🛠️ Desarrollo

### Nuevas Funcionalidades
1. Crear página en el directorio correspondiente
2. Agregar función en `functions/` si es necesario
3. Actualizar navegación en `app.py`

### Estructura de Datos
- Todas las funciones de DB están en `functions/`
- Separación clara entre CUD y Read operations
- Manejo de errores consistente

## 📞 Soporte

Para soporte técnico o preguntas:
- Revisar la documentación en `db_setup/`
- Consultar los comentarios en el código
- Verificar la configuración de Supabase

## 🎉 ¡Listo para Usar!

El sistema está completamente funcional y listo para ser desplegado en producción. Solo necesitas:

1. ✅ Configurar Supabase
2. ✅ Ejecutar los scripts de base de datos
3. ✅ Configurar las variables de entorno
4. ✅ ¡Ejecutar `streamlit run app.py`!

---

**Desarrollado con ❤️ usando Streamlit y Supabase**
