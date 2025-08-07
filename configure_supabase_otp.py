#!/usr/bin/env python3
"""
Configure Supabase Email Templates for OTP Authentication
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def configure_supabase_otp():
    """Configure Supabase email templates for OTP authentication"""
    
    # Get configuration from environment
    access_token = os.getenv("SUPABASE_ACCESS_TOKEN")
    project_ref = os.getenv("SUPABASE_PROJECT_REF")
    
    if not access_token:
        print("❌ SUPABASE_ACCESS_TOKEN not found in environment variables")
        print("📝 Please set your Supabase access token:")
        print("   export SUPABASE_ACCESS_TOKEN='your-access-token'")
        print("   Get it from: https://supabase.com/dashboard/account/tokens")
        return False
    
    if not project_ref:
        print("❌ SUPABASE_PROJECT_REF not found in environment variables")
        print("📝 Please set your Supabase project reference:")
        print("   export SUPABASE_PROJECT_REF='your-project-ref'")
        print("   Find it in your Supabase dashboard URL")
        return False
    
    # OTP Email Template Configuration
    otp_config = {
        "mailer_subjects_magic_link": "Your Login Code - Pagos",
        "mailer_templates_magic_link_content": """
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
        """,
        "mailer_subjects_confirmation": "Confirmar tu cuenta - Pagos",
        "mailer_templates_confirmation_content": """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
                <h2 style="color: #333; margin-bottom: 20px;">💰 Pagos - Sistema de Gastos</h2>
                <h3 style="color: #666; margin-bottom: 30px;">Confirmar tu cuenta</h3>
                
                <div style="background-color: #ffffff; padding: 30px; border-radius: 8px; border: 2px solid #e9ecef;">
                    <p style="color: #666; margin-bottom: 20px; font-size: 16px;">Haz clic en el siguiente enlace para confirmar tu cuenta:</p>
                    <a href="{{ .ConfirmationURL }}" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; font-weight: bold;">
                        ✅ Confirmar Cuenta
                    </a>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e9ecef;">
                    <p style="color: #999; font-size: 12px;">
                        Si no creaste esta cuenta, puedes ignorar este email.
                    </p>
                </div>
            </div>
        </div>
        """,
        "mailer_subjects_recovery": "Restablecer contraseña - Pagos",
        "mailer_templates_recovery_content": """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
                <h2 style="color: #333; margin-bottom: 20px;">💰 Pagos - Sistema de Gastos</h2>
                <h3 style="color: #666; margin-bottom: 30px;">Restablecer contraseña</h3>
                
                <div style="background-color: #ffffff; padding: 30px; border-radius: 8px; border: 2px solid #e9ecef;">
                    <p style="color: #666; margin-bottom: 20px; font-size: 16px;">Haz clic en el siguiente enlace para restablecer tu contraseña:</p>
                    <a href="{{ .ConfirmationURL }}" style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; font-weight: bold;">
                        🔑 Restablecer Contraseña
                    </a>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e9ecef;">
                    <p style="color: #999; font-size: 12px;">
                        Si no solicitaste restablecer tu contraseña, puedes ignorar este email.
                    </p>
                </div>
            </div>
        </div>
        """
    }
    
    # API endpoint
    url = f"https://api.supabase.com/v1/projects/{project_ref}/config/auth"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🔄 Configurando plantillas de email para OTP...")
        
        response = requests.patch(url, headers=headers, json=otp_config)
        
        if response.status_code == 200:
            print("✅ Plantillas de email configuradas exitosamente!")
            print("📧 Ahora Supabase enviará códigos OTP en lugar de Magic Links")
            print("\n📋 Configuración aplicada:")
            print("   • Magic Link → Email OTP")
            print("   • Confirmación de cuenta")
            print("   • Recuperación de contraseña")
            print("\n🚀 Tu aplicación ahora usará autenticación OTP por email!")
            return True
        else:
            print(f"❌ Error al configurar: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def get_current_config():
    """Get current Supabase auth configuration"""
    
    access_token = os.getenv("SUPABASE_ACCESS_TOKEN")
    project_ref = os.getenv("SUPABASE_PROJECT_REF")
    
    if not access_token or not project_ref:
        print("❌ Configuración incompleta")
        return None
    
    url = f"https://api.supabase.com/v1/projects/{project_ref}/config/auth"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error al obtener configuración: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return None

def main():
    """Main function"""
    print("💰 Configuración de Supabase para OTP - Pagos")
    print("=" * 50)
    
    # Check current configuration
    print("📋 Verificando configuración actual...")
    current_config = get_current_config()
    
    if current_config:
        print("✅ Conexión a Supabase establecida")
        
        # Check if OTP is already configured
        magic_link_template = current_config.get("mailer_templates_magic_link_content", "")
        if "{{ .Token }}" in magic_link_template:
            print("✅ OTP ya está configurado!")
            print("📧 Las plantillas de email están configuradas para OTP")
        else:
            print("⚠️  OTP no está configurado")
            print("📧 Configurando plantillas para OTP...")
            configure_supabase_otp()
    else:
        print("❌ No se pudo conectar a Supabase")
        print("📝 Verifica tu SUPABASE_ACCESS_TOKEN y SUPABASE_PROJECT_REF")

if __name__ == "__main__":
    main()
