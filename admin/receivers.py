import streamlit as st
from functions.f_read import get_receivers, get_categories, get_accounts, get_receiver_by_id, get_receiver_categories, get_receiver_accounts, get_current_user_profile
from functions.f_cud import create_receiver, update_receiver, delete_receiver

st.subheader("👥 Gestión de Recibidores")

# Get all receivers
receivers = get_receivers()
categories = get_categories()
accounts = get_accounts()

# Receiver management tabs
tab1, tab2 = st.tabs(["Crear Recibidor", "Editar Recibidor"])

with tab1:
    st.subheader("➕ Crear Nuevo Recibidor")
    
    with st.form("create_receiver_form"):
        name = st.text_input("Nombre del recibidor")
        email = st.text_input("Email")
        phone = st.text_input("Teléfono")
        role = st.text_input("Rol/Cargo")
        
        # Category selection
        st.write("Categorías asociadas:")
        category_options = {cat['description']: cat['id'] for cat in categories}
        selected_categories = st.multiselect(
            "Selecciona las categorías:",
            options=list(category_options.keys())
        )
        category_ids = [category_options[cat] for cat in selected_categories]
        
        # Account selection
        st.write("Cuentas asociadas:")
        account_options = {f"{acc['description']} ({cat['description']})": acc['id'] for acc in accounts for cat in categories if cat['id'] == acc['category_id']}
        selected_accounts = st.multiselect(
            "Selecciona las cuentas:",
            options=list(account_options.keys())
        )
        account_ids = [account_options[acc] for acc in selected_accounts]
        
        submitted = st.form_submit_button("Crear Recibidor")
        
        if submitted:
            if name:
                # Get current user for created_by field
                current_user = get_current_user_profile(st.session_state.get('user_id'))
                created_by = current_user['id'] if current_user else None
                
                # Create receiver
                receiver_data = {
                    "name": name,
                    "email": email if email else None,
                    "phone": phone if phone else None,
                    "role": role if role else None,
                    "created_by": created_by
                }
                
                new_receiver = create_receiver(receiver_data, category_ids, account_ids)
                if new_receiver:
                    st.success(f"Recibidor {name} creado exitosamente!")
                    st.rerun()
                else:
                    st.error("Error al crear el recibidor")
            else:
                st.error("Por favor completa al menos el nombre del recibidor.")

with tab2:
    st.subheader("✏️ Editar Recibidor")
    
    # Receiver selection dropdown
    if receivers:
        # Create a list of receiver options for the dropdown
        receiver_options = {f"{receiver['name']} ({receiver['email'] or 'Sin email'})": receiver for receiver in receivers}
        
        # Add a "Select receiver" option at the beginning
        receiver_options = {"-- Seleccionar recibidor --": None} | receiver_options
        
        selected_receiver_key = st.selectbox(
            "Selecciona un recibidor para editar:",
            options=list(receiver_options.keys()),
            key="receiver_selection"
        )
        
        selected_receiver = receiver_options.get(selected_receiver_key)
        
        if selected_receiver:
            # Get receiver's current categories and accounts
            current_categories = get_receiver_categories(selected_receiver['id'])
            current_accounts = get_receiver_accounts(selected_receiver['id'])
            
            st.write(f"**Editando:** {selected_receiver['name']}")
            
            # Display name as read-only (cannot be edited)
            st.info(f"**Nombre:** {selected_receiver['name']} (no se puede editar)")
            
            # Basic information fields
            new_email = st.text_input("Email", value=selected_receiver['email'] or "", key="edit_email")
            new_phone = st.text_input("Teléfono", value=selected_receiver['phone'] or "", key="edit_phone")
            new_role = st.text_input("Rol/Cargo", value=selected_receiver['role'] or "", key="edit_role")
            
            # Category selection
            st.write("**Categorías asociadas:**")
            category_options = {cat['description']: cat['id'] for cat in categories}
            current_category_names = [cat['description'] for cat in current_categories]
            new_categories = st.multiselect(
                "Selecciona las categorías:",
                options=list(category_options.keys()),
                default=current_category_names,
                key="edit_categories"
            )
            new_category_ids = [category_options[cat] for cat in new_categories]
            
            # Dynamic account selection based on selected categories
            st.write("**Cuentas asociadas:**")
            if new_categories:
                # Get accounts for the selected categories
                available_accounts = []
                for category_name in new_categories:
                    category_id = category_options[category_name]
                    category_accounts = get_accounts_by_category(category_id)
                    available_accounts.extend(category_accounts)
                
                if available_accounts:
                    # Remove duplicates and create options
                    unique_accounts = {}
                    for acc in available_accounts:
                        # Find the category name for this account
                        category_name = next((cat['description'] for cat in categories if cat['id'] == acc['category_id']), 'Unknown')
                        unique_accounts[f"{acc['description']} ({category_name})"] = acc['id']
                    
                    # Get current account names that are still valid
                    current_account_names = []
                    for acc in current_accounts:
                        category_name = next((cat['description'] for cat in categories if cat['id'] == acc['category_id']), 'Unknown')
                        account_key = f"{acc['description']} ({category_name})"
                        if account_key in unique_accounts:
                            current_account_names.append(account_key)
                    
                    account_names = list(unique_accounts.keys())
                    new_accounts = st.multiselect(
                        "Selecciona las cuentas:",
                        options=account_names,
                        default=current_account_names,
                        key="edit_accounts"
                    )
                    new_account_ids = [unique_accounts[acc] for acc in new_accounts]
                else:
                    st.warning("No hay cuentas disponibles para las categorías seleccionadas.")
                    new_account_ids = []
            else:
                st.info("Selecciona al menos una categoría para ver las cuentas disponibles.")
                new_account_ids = []
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Guardar Cambios", type="primary", key="save_changes"):
                    # Update receiver (name cannot be changed)
                    update_data = {
                        "email": new_email if new_email else None,
                        "phone": new_phone if new_phone else None,
                        "role": new_role if new_role else None
                    }
                    
                    if update_receiver(selected_receiver['id'], update_data, new_category_ids, new_account_ids):
                        st.success("✅ Recibidor actualizado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error actualizando información del recibidor")
            
            with col2:
                if st.button("❌ Cancelar", key="cancel_edit"):
                    st.rerun()
        else:
            st.info("Selecciona un recibidor de la lista para editarlo.")
    else:
        st.warning("No hay recibidores disponibles para editar.")
