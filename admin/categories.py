import streamlit as st
from functions.f_read import get_categories, get_accounts, get_accounts_by_category
from functions.f_cud import create_category, create_account
import uuid

st.subheader("Gestión de Categorías y Cuentas")

# Get current data
categories = get_categories()
accounts = get_accounts()

# Create tabs for different operations
tab1, tab2, tab3 = st.tabs(["📊 Ver Categorías y Cuentas", "➕ Crear Categoría", "💳 Crear Cuenta"])

with tab1:
    st.subheader("📊 Categorías y Cuentas Existentes")
    
    if not categories:
        st.info("No hay categorías creadas aún.")
    else:
        # Display categories with their accounts
        for category in categories:
            with st.expander(f"📂 {category['description']}", expanded=True):
                # Get accounts for this category
                category_accounts = get_accounts_by_category(category['id'])
                
                if category_accounts:
                    # Create a table for accounts
                    account_data = []
                    for account in category_accounts:
                        account_data.append({
                            "ID": account['id'],
                            "Descripción": account['description'],
                            "Fecha de Creación": account['created_at'][:10] if account['created_at'] else "N/A"
                        })
                    
                    st.dataframe(
                        account_data,
                        column_config={
                            "ID": st.column_config.NumberColumn("ID", width="small"),
                            "Descripción": st.column_config.TextColumn("Descripción", width="medium"),
                            "Fecha de Creación": st.column_config.TextColumn("Fecha de Creación", width="small")
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info("No hay cuentas asociadas a esta categoría.")
                
                # Show category details
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID de Categoría:** {category['id']}")
                with col2:
                    st.write(f"**Fecha de Creación:** {category['created_at'][:10] if category['created_at'] else 'N/A'}")

with tab2:
    st.subheader("➕ Crear Nueva Categoría")
    
    with st.form("create_category_form"):
        category_description = st.text_input(
            "Descripción de la Categoría",
            placeholder="Ej: Office Supplies, Travel, Equipment, etc.",
            help="Nombre descriptivo de la categoría"
        )
        
        submitted = st.form_submit_button("Crear Categoría", type="primary")
        
        if submitted:
            if category_description:
                category_data = {
                    "description": category_description
                }
                
                if create_category(category_data):
                    st.success("✅ Categoría creada exitosamente!")
                    st.rerun()
                else:
                    st.error("❌ Error al crear la categoría.")
            else:
                st.error("Por favor ingresa una descripción para la categoría.")

with tab3:
    st.subheader("💳 Crear Nueva Cuenta")
    
    # Get categories for selection
    if not categories:
        st.warning("Primero debes crear al menos una categoría.")
    else:
        with st.form("create_account_form"):
            # Category selection
            category_options = {cat['description']: cat['id'] for cat in categories}
            selected_category = st.selectbox(
                "Categoría",
                options=list(category_options.keys()),
                help="Selecciona la categoría a la que pertenecerá esta cuenta"
            )
            
            account_description = st.text_input(
                "Descripción de la Cuenta",
                placeholder="Ej: Office Supplies Account, Travel Expenses Account, etc.",
                help="Nombre descriptivo de la cuenta"
            )
            
            submitted = st.form_submit_button("Crear Cuenta", type="primary")
            
            if submitted:
                if account_description and selected_category:
                    account_data = {
                        "category_id": category_options[selected_category],
                        "description": account_description
                    }
                    
                    if create_account(account_data):
                        st.success("✅ Cuenta creada exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al crear la cuenta.")
                else:
                    st.error("Por favor completa todos los campos.")
