import streamlit as st
from functions.f_read import get_all_users, get_user_roles, get_users_by_role, get_current_user_profile
from functions.f_cud import create_user, update_user, assign_role_to_user, remove_role_from_user
from functions.f_read import get_user_by_id

st.subheader("Gestión de Usuarios")

# Get all users
users = get_all_users()

# User management tabs
tab1, tab2, tab3, tab4 = st.tabs(["Lista de Usuarios", "Crear Usuario", "Editar Usuario", "Mi Perfil"])

with tab1:
    st.subheader("Lista de Usuarios")
    
    if users:
        # Search and filter
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("Buscar usuario", placeholder="Nombre o email...")
        with col2:
            role_filter = st.selectbox("Filtrar por rol", ["Todos", "admin", "requester", "approver", "payer", "viewer"])
        
        # Filter users
        filtered_users = users
        if search_term:
            filtered_users = [u for u in users if search_term.lower() in u['name'].lower() or search_term.lower() in u['email'].lower()]
        
        if role_filter != "Todos":
            filtered_users = [u for u in filtered_users if role_filter in get_user_roles(u['id'])]
        
        # Display users
        for user in filtered_users:
            with st.expander(f"{user['name']} ({user['email']})"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**ID:** {user['id']}")
                    st.write(f"**Email:** {user['email']}")
                    st.write(f"**Creado:** {user['created_at'][:10]}")
                
                with col2:
                    roles = get_user_roles(user['id'])
                    st.write(f"**Roles:** {', '.join(roles) if roles else 'Sin roles'}")
                
                with col3:
                    if st.button("Editar", key=f"edit_{user['id']}"):
                        st.session_state.edit_user = user
                        st.rerun()
    else:
        st.info("No hay usuarios registrados.")

with tab2:
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

with tab3:
    st.subheader("🔧 Editar Usuario")
    
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

with tab4:
    st.subheader("Mi Perfil")
    
    # Get current user
    if 'user' in st.session_state:
        current_user = st.session_state.user
        user_profile = get_current_user_profile(current_user['id'])
        
        if user_profile:
            st.write(f"**Editando tu perfil:** {user_profile['name']} ({user_profile['email']})")
            
            with st.form("my_profile_form"):
                new_name = st.text_input("Nombre", value=user_profile['name'])
                new_email = st.text_input("Email", value=user_profile['email'])
                
                # Show current roles (read-only for own profile)
                current_roles = get_user_roles(user_profile['id'])
                st.write(f"**Roles actuales:** {', '.join(current_roles) if current_roles else 'Sin roles'}")
                st.info("Los roles solo pueden ser modificados por un administrador.")
                
                submitted = st.form_submit_button("Guardar Cambios")
                
                if submitted:
                    if new_name and new_email:
                        update_data = {
                            "name": new_name,
                            "email": new_email
                        }
                        
                        if update_user(user_profile['id'], update_data):
                            st.success("Perfil actualizado exitosamente!")
                            # Update session state
                            st.session_state.user['name'] = new_name
                            st.session_state.user['email'] = new_email
                            st.rerun()
                        else:
                            st.error("Error al actualizar el perfil.")
                    else:
                        st.error("Por favor completa todos los campos.")
        else:
            st.error("No se pudo cargar tu perfil.")
    else:
        st.error("No hay usuario autenticado.") 