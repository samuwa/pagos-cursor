# Configuración de Supabase para Email OTP

## Opción 1: Configuración Automática (Recomendada)

### 1. Obtener Access Token
1. Ve a [Supabase Dashboard](https://supabase.com/dashboard/account/tokens)
2. Crea un nuevo access token
3. Copia el token

### 2. Obtener Project Reference
1. Ve a tu proyecto en Supabase Dashboard
2. El Project Reference está en la URL: `https://supabase.com/dashboard/project/[PROJECT_REF]`
3. Copia el PROJECT_REF

### 3. Configurar Variables de Entorno
```bash
export SUPABASE_ACCESS_TOKEN="tu-access-token"
export SUPABASE_PROJECT_REF="tu-project-ref"
```

### 4. Ejecutar Script de Configuración
```bash
python configure_supabase_otp.py
```

## Opción 2: Configuración Manual

### 1. Ir a Supabase Dashboard
1. Ve a tu proyecto en [Supabase Dashboard](https://supabase.com/dashboard)
2. Navega a **Authentication** → **Email Templates**

### 2. Modificar Magic Link Template
1. Encuentra la plantilla **"Magic Link"**
2. Reemplaza el contenido con:

```html
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
        <h2 style="color: #333; margin-bottom: 20px;">💰 Pagos - Sistema de Gastos</h2>
        <h3 style="color: #666; margin-bottom: 30px;">Tu código de acceso</h3>
        
        <div style="background-color: #ffffff; padding: 30px; border-radius: 8px; border: 2px solid #e9ecef;">
            <p style="color: #666; margin-bottom: 15px; font-size: 16px;">Ingresa este código de 6 dígitos para acceder:</p>
            <div style="background-color: #007bff; color: white; padding: 15px; border-radius: 6px; font-size: 24px; font-weight: bold; letter-spacing: 3px; margin: 20px 0;">
                {{ .Token }}
            </div>
            <p style="color: #999; font-size: 14px; margin-top: 20px;">
                ⏰ Este código expira en 5 minutos por seguridad.
            </p>
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e9ecef;">
            <p style="color: #999; font-size: 12px;">
                Si no solicitaste este código, puedes ignorar este email.
            </p>
        </div>
    </div>
</div>
```

### 3. Cambiar el Asunto
Cambia el asunto del email a: **"Tu código de acceso - Pagos"**

### 4. Guardar Cambios
Haz clic en **"Save"** para aplicar los cambios.

## Verificación

Después de la configuración:

1. **Prueba el login** en tu aplicación
2. **Verifica que recibes un código OTP** en lugar de un Magic Link
3. **Confirma que el código funciona** en la aplicación

## Diferencias Clave

### Antes (Magic Link):
- Email contiene un enlace clickeable
- Usuario hace clic para autenticarse
- Usa `{{ .ConfirmationURL }}`

### Después (OTP):
- Email contiene un código de 6 dígitos
- Usuario ingresa el código manualmente
- Usa `{{ .Token }}`

## Solución de Problemas

### Si no recibes emails:
1. Verifica que el email esté autorizado en Supabase
2. Revisa la configuración SMTP
3. Verifica los logs de Supabase

### Si el código no funciona:
1. Verifica que el template use `{{ .Token }}`
2. Confirma que el código no haya expirado (5 minutos)
3. Revisa los logs de la aplicación

### Si necesitas ayuda:
1. Revisa los logs de Supabase Dashboard
2. Verifica la configuración de email templates
3. Contacta soporte de Supabase si es necesario
