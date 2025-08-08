import streamlit as st
from functions.f_cud import create_expense
from datetime import datetime
import uuid

st.subheader("Nuevo Gasto")

# Get current user
user = st.session_state.user

if not user:
    st.error("No hay usuario autenticado.")
    st.stop()

# Expense form
with st.form("new_expense_form"):
    st.subheader("Detalles del Gasto")
    
    # Basic information
    description = st.text_area(
        "Descripción del gasto",
        placeholder="Describe el gasto en detalle...",
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input(
            "Monto ($)",
            min_value=0.01,
            max_value=100000.00,
            step=0.01,
            format="%.2f"
        )
        
        category = st.selectbox(
            "📂 Categoría",
            [
                "Alimentación",
                "Transporte",
                "Hospedaje",
                "Materiales",
                "Equipamiento",
                "Servicios",
                "Otros"
            ]
        )
    
    with col2:
        expense_date = st.date_input(
            "📅 Fecha del gasto",
            value=datetime.now().date()
        )
    
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
        placeholder="Información adicional que consideres relevante...",
        height=80
    )
    
    # File upload (for receipts)
    uploaded_file = st.file_uploader(
        "📎 Adjuntar recibo/factura",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        help="Sube una imagen o PDF del recibo o factura"
    )
    
    # Submit button
    submitted = st.form_submit_button("🚀 Enviar Gasto", use_container_width=True)
    
    if submitted:
        if description and amount > 0:
            # Create expense data
            expense_data = {
                "user_id": user["id"],
                "description": description,
                "amount": amount,
                "category": category,
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
            new_expense = create_expense(expense_data)
            
            if new_expense:
                st.success("Gasto enviado exitosamente!")
                st.balloons()
                
                # Show summary
                st.markdown("---")
                st.subheader("Resumen del Gasto")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {new_expense['id']}")
                    st.write(f"**Descripción:** {new_expense['description']}")
                    st.write(f"**Monto:** ${new_expense['amount']:.2f}")
                    st.write(f"**Categoría:** {new_expense['category']}")
                
                with col2:
                    st.write(f"**Estado:** {new_expense['status']}")
                    st.write(f"**Fecha:** {new_expense['expense_date']}")
                    st.write(f"**Proveedor:** {new_expense.get('vendor', 'N/A')}")
                
                # Next steps
                st.info("Tu gasto ha sido enviado para aprobación. Recibirás una notificación cuando sea revisado.")
                
                # Clear form
                st.rerun()
            else:
                st.error("Error al crear el gasto. Por favor intenta de nuevo.")
        else:
            st.error("Por favor completa la descripción y el monto del gasto.") 