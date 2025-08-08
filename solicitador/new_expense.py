import streamlit as st
from functions.f_read import get_categories, get_accounts_by_category
from functions.f_cud import create_expense
from datetime import datetime
import uuid

# Get current user
user = st.session_state.user

if not user:
    st.error("No hay usuario autenticado.")
    st.stop()

st.subheader("Nuevo Gasto")

# Basic information
st.subheader("Información Básica")

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
    expense_date = st.date_input(
        "📅 Fecha del gasto",
        value=datetime.now().date()
    )

# Category and Account selection
st.subheader("Categorización")

# Get all categories
categories = get_categories()

if not categories:
    st.error("No se pudieron cargar las categorías.")
    st.stop()

# Create category options
category_options = {cat['description']: cat['id'] for cat in categories}
category_names = list(category_options.keys())

# Multiple category selection
selected_categories = st.multiselect(
    "📂 Categorías",
    options=category_names,
    help="Selecciona una o más categorías para este gasto"
)

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
    st.subheader("Información Adicional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        vendor = st.text_input(
            "🏢 Proveedor/Vendedor",
            placeholder="Nombre del proveedor"
        )
        
        # File upload for quotation
        quotation_file = st.file_uploader(
            "📄 Cotización",
            type=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'],
            help="Sube el archivo de la cotización (PDF, Word, o imagen)"
        )
    
    with col2:
        payment_method = st.selectbox(
            "Método de pago",
            ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia", "Otro"]
        )
        
        reimbursement_type = st.selectbox(
            "Tipo de reembolso",
            ["Reembolso directo", "Compra corporativa", "Otro"]
        )
    
    # Reimbursement section
    st.subheader("Información de Reembolso")
    
    is_reimbursement = st.checkbox(
        "💰 Es un reembolso",
        help="Marca esta casilla si este gasto es un reembolso que necesitas recuperar"
    )
    
    if is_reimbursement:
        col1, col2 = st.columns(2)
        
        with col1:
            reimbursement_recipient = st.text_input(
                "👤 Recibidor del reembolso",
                placeholder="Nombre de la persona que recibirá el reembolso",
                help="Persona a quien se le hará el reembolso"
            )
        
        with col2:
            reimbursement_method = st.selectbox(
                "Método de reembolso",
                ["Transferencia bancaria", "Efectivo", "Cheque", "Otro"]
            )
    
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
        else:
            # Create expense data
            expense_data = {
                "user_id": user["id"],
                "description": description,
                "amount": amount,
                "category_ids": [category_options[cat] for cat in selected_categories],
                "account_ids": selected_accounts,
                "expense_date": expense_date.strftime("%Y-%m-%d"),
                "vendor": vendor,
                "quotation_file": quotation_file.name if quotation_file else None,
                "payment_method": payment_method,
                "reimbursement_type": reimbursement_type,
                "notes": comments,
                "status": "pending",
                "is_reimbursement": is_reimbursement
            }
            
            # Add reimbursement fields if it's a reimbursement
            if is_reimbursement:
                expense_data.update({
                    "reimbursement_recipient": reimbursement_recipient,
                    "reimbursement_method": reimbursement_method
                })
            
            # Create the expense
            if create_expense(expense_data):
                st.success("✅ Gasto creado exitosamente!")
                st.balloons()
            else:
                st.error("❌ Error al crear el gasto. Por favor intenta de nuevo.") 