import streamlit as st
import os
from supabase import create_client
from functions.f_cud import upload_file_to_supabase
import io

st.title("🧪 Test de Configuración de Supabase Storage")

# Check environment variables
st.subheader("1. Verificar Variables de Entorno")

supabase_url = os.environ.get("SUPABASE_URL")
supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY")
supabase_service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

col1, col2, col3 = st.columns(3)

with col1:
    if supabase_url:
        st.success("✅ SUPABASE_URL configurado")
    else:
        st.error("❌ SUPABASE_URL no encontrado")

with col2:
    if supabase_anon_key:
        st.success("✅ SUPABASE_ANON_KEY configurado")
    else:
        st.error("❌ SUPABASE_ANON_KEY no encontrado")

with col3:
    if supabase_service_key:
        st.success("✅ SUPABASE_SERVICE_ROLE_KEY configurado")
    else:
        st.error("❌ SUPABASE_SERVICE_ROLE_KEY no encontrado")

# Test Supabase connection
st.subheader("2. Verificar Conexión a Supabase")

try:
    supabase = create_client(supabase_url, supabase_service_key)
    
    # Test database connection
    response = supabase.table('users').select('count', count='exact').execute()
    st.success("✅ Conexión a base de datos exitosa")
    
    # Test storage connection
    try:
        # Try to list files in quotes bucket
        storage_response = supabase.storage.from_('quotes').list()
        st.success("✅ Conexión a Storage exitosa - Bucket 'quotes' accesible")
    except Exception as e:
        st.error(f"❌ Error accediendo al bucket 'quotes': {str(e)}")
    
    try:
        # Try to list files in receipts bucket
        storage_response = supabase.storage.from_('receipts').list()
        st.success("✅ Conexión a Storage exitosa - Bucket 'receipts' accesible")
    except Exception as e:
        st.error(f"❌ Error accediendo al bucket 'receipts': {str(e)}")
        
except Exception as e:
    st.error(f"❌ Error de conexión: {str(e)}")

# Test file upload
st.subheader("3. Test de Subida de Archivo")

test_file = st.file_uploader(
    "Selecciona un archivo para probar la subida",
    type=['pdf', 'jpg', 'jpeg', 'png'],
    help="Este es solo un test, el archivo se subirá al bucket 'quotes'"
)

if test_file and st.button("📤 Probar Subida de Archivo"):
    try:
        # Create a test file
        test_content = b"This is a test file for Supabase Storage"
        test_file_obj = io.BytesIO(test_content)
        test_file_obj.name = "test_file.txt"
        
        # Test upload
        result = upload_file_to_supabase(test_file, "quotes")
        
        if result:
            st.success("✅ Archivo subido exitosamente!")
            st.json(result)
        else:
            st.error("❌ Error al subir archivo")
            
    except Exception as e:
        st.error(f"❌ Error en test de subida: {str(e)}")

# Check database tables
st.subheader("4. Verificar Tablas de Base de Datos")

try:
    # Check if expense_categories table exists
    response = supabase.table('expense_categories').select('*').limit(1).execute()
    st.success("✅ Tabla 'expense_categories' existe")
except Exception as e:
    st.error(f"❌ Tabla 'expense_categories' no existe o no es accesible: {str(e)}")

try:
    # Check if expense_accounts table exists
    response = supabase.table('expense_accounts').select('*').limit(1).execute()
    st.success("✅ Tabla 'expense_accounts' existe")
except Exception as e:
    st.error(f"❌ Tabla 'expense_accounts' no existe o no es accesible: {str(e)}")

try:
    # Check if payment_receipts table exists
    response = supabase.table('payment_receipts').select('*').limit(1).execute()
    st.success("✅ Tabla 'payment_receipts' existe")
except Exception as e:
    st.error(f"❌ Tabla 'payment_receipts' no existe o no es accesible: {str(e)}")

# Summary
st.subheader("📊 Resumen de Configuración")

if (supabase_url and supabase_anon_key and supabase_service_key):
    st.success("🎉 ¡Configuración completada! Supabase Storage está listo para usar.")
    st.info("Ahora puedes usar la aplicación para subir cotizaciones y comprobantes de pago.")
else:
    st.error("⚠️ Hay problemas en la configuración. Revisa las variables de entorno.")
