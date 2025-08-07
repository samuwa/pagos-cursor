import streamlit as st
import os
from dotenv import load_dotenv
from functions.f_cud import send_otp_email, verify_otp, get_user_roles
from functions.f_read import get_user_by_email
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Pagos - Sistema de Gastos",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_roles' not in st.session_state:
    st.session_state.user_roles = []
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'otp_email' not in st.session_state:
    st.session_state.otp_email = ""
if 'otp_sent_time' not in st.session_state:
    st.session_state.otp_sent_time = 0

def login_page():
    """Login interface with email OTP"""
    st.title("Pagos - Sistema de Gastos")
    st.markdown("---")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Iniciar Sesión")
        st.markdown("Ingresa tu email para recibir un código de verificación")
        
        if not st.session_state.otp_sent:
            # Step 1: Email input
            with st.form("email_form"):
                email = st.text_input("Email", placeholder="tu@email.com")
                
                submitted = st.form_submit_button("Enviar Código", use_container_width=True)
                
                if submitted:
                    if email and "@" in email:
                        # Send OTP
                        if send_otp_email(email):
                            st.session_state.otp_sent = True
                            st.session_state.otp_email = email
                            st.session_state.otp_sent_time = time.time()
                            st.success("Código enviado a tu email. Revisa tu bandeja de entrada.")
                            st.rerun()
                        else:
                            st.error("Error al enviar el código. Verifica tu email.")
                    else:
                        st.warning("Por favor ingresa un email válido.")
        
        else:
            # Step 2: OTP verification
            st.markdown(f"**Código enviado a:** {st.session_state.otp_email}")
            
            # Check if OTP has expired (5 minutes)
            if time.time() - st.session_state.otp_sent_time > 300:  # 5 minutes
                st.warning("El código ha expirado. Solicita uno nuevo.")
                st.session_state.otp_sent = False
                st.session_state.otp_email = ""
                st.rerun()
            
            with st.form("otp_form"):
                otp = st.text_input("Código de Verificación", placeholder="123456", max_chars=6)
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Verificar", use_container_width=True)
                with col2:
                    if st.form_submit_button("Nuevo Código", use_container_width=True):
                        if send_otp_email(st.session_state.otp_email):
                            st.session_state.otp_sent_time = time.time()
                            st.success("Nuevo código enviado.")
                            st.rerun()
                        else:
                            st.error("Error al enviar nuevo código.")
                
                if submitted:
                    if otp and len(otp) == 6:
                        # Verify OTP
                        user = verify_otp(st.session_state.otp_email, otp)
                        if user:
                            st.session_state.user = user
                            st.session_state.user_roles = get_user_roles(user['id'])
                            st.session_state.otp_sent = False
                            st.session_state.otp_email = ""
                            st.success("¡Inicio de sesión exitoso!")
                            st.rerun()
                        else:
                            st.error("Código inválido. Por favor intenta de nuevo.")
                    else:
                        st.warning("Por favor ingresa el código de 6 dígitos.")
            
            # Show remaining time
            remaining_time = int(300 - (time.time() - st.session_state.otp_sent_time))
            if remaining_time > 0:
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                st.info(f"Tiempo restante: {minutes}:{seconds:02d}")

def main_app():
    """Main application with role-based navigation"""
    user = st.session_state.user
    user_roles = st.session_state.user_roles
    
    # Header with user info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("Pagos - Sistema de Gastos")
    with col2:
        st.markdown(f"**Usuario:** {user['name']}")
    with col3:
        if st.button("Cerrar Sesión"):
            st.session_state.user = None
            st.session_state.user_roles = []
            st.session_state.otp_sent = False
            st.session_state.otp_email = ""
            st.session_state.otp_sent_time = 0
            st.rerun()
    
    st.markdown("---")
    
    # Create navigation based on user roles
    pages = {}
    
    # Debug: Show user roles
    st.sidebar.write(f"**User ID:** {user['id']}")
    st.sidebar.write(f"**Roles del usuario:** {user_roles}")
    st.sidebar.write(f"**Tipo de roles:** {type(user_roles)}")
    st.sidebar.write(f"**Longitud de roles:** {len(user_roles) if user_roles else 0}")
    
    # Debug: Check if admin role exists
    if user_roles:
        st.sidebar.write(f"**¿Contiene 'admin'?:** {'admin' in user_roles}")
        st.sidebar.write(f"**Roles exactos:** {[repr(role) for role in user_roles]}")
    else:
        st.sidebar.write("**No hay roles asignados**")
    
    # Admin pages
    if 'admin' in user_roles:
        pages["Administración"] = [
            st.Page("admin/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
            st.Page("admin/users.py", title="Usuarios", icon=":material/people:"),
            st.Page("admin/expenses.py", title="Todos los Gastos", icon=":material/receipt:"),
            st.Page("admin/reports.py", title="Reportes", icon=":material/analytics:"),
        ]
    
    # Requester pages
    if 'requester' in user_roles:
        pages["Solicitudes"] = [
            st.Page("solicitador/new_expense.py", title="Nuevo Gasto", icon=":material/add:"),
            st.Page("solicitador/my_expenses.py", title="Mis Gastos", icon=":material/list:"),
        ]
    
    # Approver pages
    if 'approver' in user_roles:
        pages["Aprobaciones"] = [
            st.Page("aprovador/pending.py", title="Pendientes", icon=":material/pending:"),
            st.Page("aprovador/approved.py", title="Aprobados", icon=":material/check_circle:"),
            st.Page("aprovador/rejected.py", title="Rechazados", icon=":material/cancel:"),
        ]
    
    # Payer pages
    if 'payer' in user_roles:
        pages["Pagos"] = [
            st.Page("pagador/to_pay.py", title="Por Pagar", icon=":material/payment:"),
            st.Page("pagador/paid.py", title="Pagados", icon=":material/done:"),
        ]
    
    # Viewer pages (only if user has viewer role)
    if 'viewer' in user_roles:
        pages["Vista General"] = [
            st.Page("vista/overview.py", title="Vista General", icon=":material/visibility:"),
            st.Page("vista/expenses.py", title="Gastos", icon=":material/receipt:"),
        ]
    
    # Create navigation
    if pages:
        pg = st.navigation(pages, position="top", expanded=True)
        pg.run()
    else:
        # Fallback: If no pages are assigned but user exists, show admin pages
        st.warning("No tienes permisos para acceder a ninguna página. Contacta al administrador.")
        st.sidebar.write("**DEBUG: Mostrando páginas de admin como fallback**")
        
        # Force show admin pages as fallback
        fallback_pages = {
            "Administración": [
                st.Page("admin/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
                st.Page("admin/users.py", title="Usuarios", icon=":material/people:"),
                st.Page("admin/expenses.py", title="Todos los Gastos", icon=":material/receipt:"),
                st.Page("admin/reports.py", title="Reportes", icon=":material/analytics:"),
            ]
        }
        
        pg_fallback = st.navigation(fallback_pages, position="top", expanded=True)
        pg_fallback.run()

# Main app logic
if st.session_state.user is None:
    login_page()
else:
    main_app() 