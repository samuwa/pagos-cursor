import streamlit as st
import os
from dotenv import load_dotenv
from functions.f_cud import authenticate_user, get_user_roles
from functions.f_read import get_user_by_email

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Pagos - Sistema de Gastos",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_roles' not in st.session_state:
    st.session_state.user_roles = []

def login_page():
    """Login interface"""
    st.title("💰 Pagos - Sistema de Gastos")
    st.markdown("---")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Iniciar Sesión")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="tu@email.com")
            password = st.text_input("🔑 Contraseña", type="password", placeholder="Tu contraseña")
            
            submitted = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)
            
            if submitted:
                if email and password:
                    # Authenticate user
                    user = authenticate_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.user_roles = get_user_roles(user['id'])
                        st.rerun()
                    else:
                        st.error("❌ Credenciales inválidas. Por favor intenta de nuevo.")
                else:
                    st.warning("⚠️ Por favor completa todos los campos.")

def main_app():
    """Main application with role-based navigation"""
    user = st.session_state.user
    user_roles = st.session_state.user_roles
    
    # Header with user info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("💰 Pagos - Sistema de Gastos")
    with col2:
        st.markdown(f"**Usuario:** {user['name']}")
    with col3:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.user = None
            st.session_state.user_roles = []
            st.rerun()
    
    st.markdown("---")
    
    # Create navigation based on user roles
    pages = []
    
    # Admin pages
    if 'admin' in user_roles:
        pages.extend([
            st.Page("admin/dashboard.py", title="📊 Dashboard", icon=":material/dashboard:"),
            st.Page("admin/users.py", title="👥 Usuarios", icon=":material/people:"),
            st.Page("admin/expenses.py", title="📋 Todos los Gastos", icon=":material/receipt:"),
            st.Page("admin/reports.py", title="📈 Reportes", icon=":material/analytics:"),
        ])
    
    # Requester pages
    if 'requester' in user_roles:
        pages.extend([
            st.Page("solicitador/new_expense.py", title="➕ Nuevo Gasto", icon=":material/add:"),
            st.Page("solicitador/my_expenses.py", title="📝 Mis Gastos", icon=":material/list:"),
        ])
    
    # Approver pages
    if 'approver' in user_roles:
        pages.extend([
            st.Page("aprovador/pending.py", title="⏳ Pendientes", icon=":material/pending:"),
            st.Page("aprovador/approved.py", title="✅ Aprobados", icon=":material/check_circle:"),
            st.Page("aprovador/rejected.py", title="❌ Rechazados", icon=":material/cancel:"),
        ])
    
    # Payer pages
    if 'payer' in user_roles:
        pages.extend([
            st.Page("pagador/to_pay.py", title="💳 Por Pagar", icon=":material/payment:"),
            st.Page("pagador/paid.py", title="✅ Pagados", icon=":material/done:"),
        ])
    
    # Viewer pages (if any user has viewer role)
    if 'viewer' in user_roles or not pages:  # Show viewer pages if no other roles
        pages.extend([
            st.Page("vista/overview.py", title="👁️ Vista General", icon=":material/visibility:"),
            st.Page("vista/expenses.py", title="📋 Gastos", icon=":material/receipt:"),
        ])
    
    # Create navigation
    if pages:
        pg = st.navigation(pages, position="sidebar", expanded=True)
        pg.run()
    else:
        st.warning("⚠️ No tienes permisos para acceder a ninguna página. Contacta al administrador.")

# Main app logic
if st.session_state.user is None:
    login_page()
else:
    main_app() 