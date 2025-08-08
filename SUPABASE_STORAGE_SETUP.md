# Configuración de Supabase Storage para Archivos

## 📋 Requisitos Previos

1. Tener un proyecto Supabase configurado
2. Tener las variables de entorno configuradas:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`

## 🗂️ Configuración de Buckets

### 1. Crear Buckets en Supabase Dashboard

Ve a tu proyecto Supabase → Storage → Create a new bucket

#### Bucket: `quotes`
- **Propósito**: Almacenar cotizaciones y documentos de gastos
- **Configuración**:
  - Public bucket: ✅ (para acceso público a archivos)
  - File size limit: 10MB
  - Allowed MIME types: `application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png`

#### Bucket: `receipts`
- **Propósito**: Almacenar comprobantes de pago
- **Configuración**:
  - Public bucket: ✅ (para acceso público a archivos)
  - File size limit: 10MB
  - Allowed MIME types: `application/pdf, image/jpeg, image/png`

### 2. Configurar Políticas de Seguridad (RLS)

#### Para el bucket `quotes`:
```sql
-- Permitir lectura pública de cotizaciones
CREATE POLICY "Public read access for quotes" ON storage.objects
FOR SELECT USING (bucket_id = 'quotes');

-- Permitir inserción solo a usuarios autenticados
CREATE POLICY "Authenticated users can upload quotes" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'quotes' AND auth.role() = 'authenticated');
```

#### Para el bucket `receipts`:
```sql
-- Permitir lectura pública de comprobantes
CREATE POLICY "Public read access for receipts" ON storage.objects
FOR SELECT USING (bucket_id = 'receipts');

-- Permitir inserción solo a usuarios autenticados
CREATE POLICY "Authenticated users can upload receipts" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'receipts' AND auth.role() = 'authenticated');
```

## 🗄️ Configuración de Base de Datos

### 1. Ejecutar Migraciones

Ejecuta los siguientes archivos SQL en tu base de datos Supabase:

1. `db_setup/multiple_categories_accounts.sql` - Para múltiples categorías y cuentas
2. `db_setup/payment_receipts_table.sql` - Para la tabla de comprobantes de pago

### 2. Verificar Tablas

Asegúrate de que las siguientes tablas existan:
- `expense_categories` - Relación muchos a muchos entre gastos y categorías
- `expense_accounts` - Relación muchos a muchos entre gastos y cuentas
- `payment_receipts` - Almacenar información de comprobantes de pago

## 🔧 Configuración de Variables de Entorno

Asegúrate de que las siguientes variables estén configuradas en Heroku:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## 📁 Estructura de Archivos

### Cotizaciones
- **Ubicación**: `quotes/` bucket
- **Formato**: `{uuid}.{extension}`
- **Tipos permitidos**: PDF, DOC, DOCX, JPG, JPEG, PNG
- **Tamaño máximo**: 10MB

### Comprobantes de Pago
- **Ubicación**: `receipts/` bucket
- **Formato**: `{uuid}.{extension}`
- **Tipos permitidos**: PDF, JPG, JPEG, PNG
- **Tamaño máximo**: 10MB

## 🔍 Verificación

### 1. Probar Subida de Archivos
1. Ve a "Nuevo Gasto" en la aplicación
2. Sube un archivo de cotización
3. Verifica que aparezca en el bucket `quotes` en Supabase Dashboard

### 2. Probar Comprobantes de Pago
1. Ve a "Subir Comprobante" como pagador
2. Sube un comprobante de pago
3. Verifica que aparezca en el bucket `receipts` en Supabase Dashboard

## 🚨 Solución de Problemas

### Error: "Missing Supabase service role key"
- Verifica que `SUPABASE_SERVICE_ROLE_KEY` esté configurada en Heroku
- Asegúrate de que la clave sea correcta

### Error: "Bucket not found"
- Verifica que los buckets `quotes` y `receipts` existan en Supabase
- Asegúrate de que estén configurados como públicos

### Error: "Permission denied"
- Verifica las políticas RLS en los buckets
- Asegúrate de que los usuarios autenticados puedan subir archivos

### Archivos no se suben
- Verifica el tamaño del archivo (máximo 10MB)
- Verifica el tipo de archivo (solo PDF, DOC, DOCX, JPG, PNG)
- Revisa los logs de la aplicación para errores específicos

## 📊 Monitoreo

### Verificar Uso de Storage
1. Ve a Supabase Dashboard → Storage
2. Revisa el uso de cada bucket
3. Monitorea el crecimiento de archivos

### Logs de Aplicación
```bash
# Ver logs de Heroku
heroku logs --tail -a pagos-cursor
```

## 🔄 Mantenimiento

### Limpieza de Archivos
- Los archivos se eliminan automáticamente cuando se elimina el gasto asociado
- Considera implementar una política de retención para archivos antiguos

### Backup
- Los archivos en Supabase Storage se respaldan automáticamente
- Considera configurar backups adicionales si es necesario
