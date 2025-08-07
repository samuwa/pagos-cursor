import streamlit as st
from functions.f_read import get_all_users, get_user_roles, get_users_by_role, get_current_user_profile
from functions.f_cud import create_user, update_user, assign_role_to_user, remove_role_from_user
from functions.f_read import get_user_by_id

st.subheader("Gestión de Usuarios")

# Get all users
users = get_all_users()

# User management tabs
tab1, tab2 = st.tabs(["Crear Usuario", "Editar Usuario"])

with tab1:
    st.subheader("➕ Crear Nuevo Usuario")
    
    with st.form("create_user_form"):
        name = st.text_input("Nombre completo", placeholder="Juan Pérez")
        email = st.text_input("Email", placeholder="juan@empresa.com")
        
        # Role selection
        st.write("Asignar roles:")
        roles = st.multiselect(
            "Selecciona los roles:",
            ["admin", "requester", "approver", "payer", "viewer"],
            default=["requester"]
        )
        
        submitted = st.form_submit_button("Crear Usuario")
        
        if submitted:
            if name and email and roles:
                # Create user
                user_data = {
                    "name": name,
                    "email": email
                }
                
                new_user = create_user(user_data)
                if new_user:
                    # Assign roles
                    for role in roles:
                        assign_role_to_user(new_user['id'], role)
                    
                    st.success(f"Usuario {name} creado exitosamente!")
                    st.rerun()
            else:
                st.error("Por favor completa todos los campos y selecciona al menos un rol.")

with tab2:
    st.subheader("Editar Usuario")
    
    if 'edit_user' in st.session_state:
        user = st.session_state.edit_user
        
        with st.form("edit_user_form"):
            st.write(f"**Editando:** {user['name']} ({user['email']})")
            
            new_name = st.text_input("Nombre", value=user['name'])
            new_email = st.text_input("Email", value=user['email'])
            
            # Current roles
            current_roles = get_user_roles(user['id'])
            new_roles = st.multiselect(
                "Roles:",
                ["admin", "requester", "approver", "payer", "viewer"],
                default=current_roles
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Guardar Cambios")
            with col2:
                if st.form_submit_button("Cancelar"):
                    del st.session_state.edit_user
                    st.rerun()
            
            if submitted:
                # Update user
                update_data = {
                    "name": new_name,
                    "email": new_email
                }
                
                if update_user(user['id'], update_data):
                    # Update roles
                    # Remove roles not in new selection
                    for role in current_roles:
                        if role not in new_roles:
                            remove_role_from_user(user['id'], role)
                    
                    # Add new roles
                    for role in new_roles:
                        if role not in current_roles:
                            assign_role_to_user(user['id'], role)
                    
                    st.success("Usuario actualizado exitosamente!")
                    del st.session_state.edit_user
                    st.rerun()
    else:
        st.info("Selecciona un usuario de la lista para editarlo.") 