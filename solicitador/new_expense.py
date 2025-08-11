import streamlit as st
from functions.f_read import get_categories, get_accounts_by_category, get_receivers_by_categories, get_receivers
from functions.f_cud import create_expense, upload_file_to_supabase, create_reimbursement
from datetime import datetime
import uuid

# Get current user
user = st.session_state.user

if not user:
    st.error("No hay usuario autenticado.")
    st.stop()

st.subheader("Nuevo Gasto")

# Basic information
st.write("**Información Básica**")

col1, col2 = st.columns(2)

with col1:
    description = st.text_input(
        "📝 Descripción del gasto",
        placeholder="Descripción detallada del gasto"
    )
    
    amount = st.number_input(
        "💰 Monto",
        min_value=0.01,
        value=0.01,
        step=0.01,
        format="%.2f"
    )

with col2:
    # Removed expense_date field - expense will be created with current timestamp
    st.write("")  # Empty space for layout consistency

# Category and Account selection
st.write("**Categorización**")

# Get all categories
categories = get_categories()

if not categories:
    st.error("No se pudieron cargar las categorías.")
    st.stop()

# Create category options
category_options = {cat['description']: cat['id'] for cat in categories}
category_names = list(category_options.keys())

# Use columns for category and account selection
col1, col2 = st.columns(2)

with col1:
    # Multiple category selection
    selected_categories = st.multiselect(
        "📂 Categorías",
        options=category_names,
        help="Selecciona una o más categorías para este gasto"
    )

with col2:
    # Account selection based on selected categories
    selected_accounts = []
    if selected_categories:
        # Get all accounts for the selected categories
        all_accounts = []
        for category_name in selected_categories:
            category_id = category_options[category_name]
            accounts = get_accounts_by_category(category_id)
            all_accounts.extend(accounts)
        
        if all_accounts:
            # Remove duplicates and create options
            unique_accounts = {}
            for acc in all_accounts:
                unique_accounts[acc['description']] = acc['id']
            
            account_names = list(unique_accounts.keys())
            
            selected_account_names = st.multiselect(
                "💳 Cuentas",
                options=account_names,
                help="Selecciona una o más cuentas para este gasto"
            )
            
            # Convert selected account names to IDs
            selected_accounts = [unique_accounts[name] for name in selected_account_names]
        else:
            st.warning("No hay cuentas disponibles para las categorías seleccionadas.")
    else:
        st.info("Selecciona al menos una categoría para ver las cuentas disponibles.")

# Additional details
st.write("**Información Adicional**")

col1, col2 = st.columns(2)

with col1:
    # Provider selection based on selected categories
    selected_provider = None
    if selected_categories:
        # Get receivers for the selected categories
        category_ids = [category_options[cat] for cat in selected_categories]
        available_receivers = get_receivers_by_categories(category_ids)
        
        if available_receivers:
            # Create provider options
            provider_options = {f"{receiver['name']} ({receiver['email'] or 'Sin email'})": receiver['id'] for receiver in available_receivers}
            provider_names = list(provider_options.keys())
            
            # Add a "Select provider" option
            provider_names = ["-- Seleccionar proveedor --"] + provider_names
            provider_options = {"-- Seleccionar proveedor --": None} | provider_options
            
            selected_provider_name = st.selectbox(
                "🏢 Proveedor/Vendedor *",
                options=provider_names,
                help="Selecciona un proveedor de la lista (filtrado por las categorías seleccionadas)"
            )
            
            selected_provider = provider_options.get(selected_provider_name)
        else:
            st.error("❌ No hay proveedores disponibles para las categorías seleccionadas. Contacta al administrador para agregar proveedores.")
    else:
        st.info("Selecciona al menos una categoría para ver los proveedores disponibles.")
    
    # File upload for quotation
    quotation_file = st.file_uploader(
        "📄 Cotización",
        type=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'],
        help="Sube el archivo de la cotización (PDF, Word, o imagen)"
    )

with col2:
    # Removed payment_method and reimbursement_type fields as they are not needed for requesters
    st.write("")  # Empty space for layout consistency

# Reimbursement section
st.write("**Información de Reembolso**")

is_reimbursement = st.checkbox(
    "💰 Es un reembolso",
    help="Marca esta casilla si este gasto es un reembolso que necesitas recuperar"
)

if is_reimbursement:
    # Get all receivers for reimbursement selection
    all_receivers = get_receivers()
    
    if all_receivers:
        # Create receiver options for reimbursement
        receiver_options = {f"{receiver['name']} ({receiver['email'] or 'Sin email'})": receiver['id'] for receiver in all_receivers}
        receiver_names = list(receiver_options.keys())
        
        # Add a "Select receiver" option
        receiver_names = ["-- Seleccionar recibidor --"] + receiver_names
        receiver_options = {"-- Seleccionar recibidor --": None} | receiver_options
        
        reimbursement_receiver_name = st.selectbox(
            "👤 Recibidor del reembolso *",
            options=receiver_names,
            help="Selecciona el recibidor que recibirá el reembolso"
        )
        
        reimbursement_receiver_id = receiver_options.get(reimbursement_receiver_name)
    else:
        st.error("❌ No hay recibidores disponibles. Contacta al administrador para agregar recibidores.")
        reimbursement_receiver_id = None

# Comments
comments = st.text_area(
    "💬 Comentarios adicionales",
    placeholder="Comentarios adicionales sobre el gasto...",
    height=100
)

# Submit button
if st.button("💾 Crear Gasto", type="primary"):
    # Validation
    if not description or not amount or not selected_categories or not selected_accounts:
        st.error("Por favor completa todos los campos obligatorios: descripción, monto, categorías y cuentas.")
    elif selected_categories and not selected_provider:
        st.error("❌ Por favor selecciona un proveedor de la lista. Es obligatorio seleccionar un proveedor.")
    elif is_reimbursement and not reimbursement_receiver_id:
        st.error("❌ Por favor selecciona un recibidor para el reembolso.")
    else:
        # Upload quotation file if provided
        quotation_info = None
        if quotation_file:
            quotation_info = upload_file_to_supabase(quotation_file, "quotes")
            if not quotation_info:
                st.error("Error al subir el archivo de cotización.")
                st.stop()
        
        # Get vendor name from selected provider
        category_ids = [category_options[cat] for cat in selected_categories]
        available_receivers = get_receivers_by_categories(category_ids)
        selected_receiver = next((r for r in available_receivers if r['id'] == selected_provider), None)
        vendor_name = selected_receiver['name'] if selected_receiver else "Proveedor no encontrado"
        
        # Create expense data
        expense_data = {
            "user_id": user["id"],
            "description": description,
            "amount": amount,
            "category_ids": [category_options[cat] for cat in selected_categories],
            "account_ids": selected_accounts,
            "vendor": vendor_name,
            "receiver_id": selected_provider,  # Add receiver_id to link to the receivers table
            "notes": comments,
            "status": "pending",
            "is_reembolso": is_reimbursement
        }
        
        # Add quotation info if uploaded
        if quotation_info:
            expense_data.update({
                "quotation_file_url": quotation_info["file_url"],
                "quotation_file_name": quotation_info["file_name"],
                "quotation_file_size": quotation_info["file_size"]
            })
        
        # Create the expense
        new_expense = create_expense(expense_data)
        if new_expense:
            # If it's a reimbursement, create the reimbursement record
            if is_reimbursement and reimbursement_receiver_id:
                reimbursement_created = create_reimbursement(
                    expense_id=new_expense['id'],
                    receiver_id=reimbursement_receiver_id,
                    created_by=user["id"]
                )
                if reimbursement_created:
                    st.success("✅ Gasto y reembolso creados exitosamente!")
                else:
                    st.warning("⚠️ Gasto creado pero hubo un error al crear el registro de reembolso.")
            else:
                st.success("✅ Gasto creado exitosamente!")
            st.balloons()
        else:
            st.error("❌ Error al crear el gasto. Por favor intenta de nuevo.") 