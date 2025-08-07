import streamlit as st
from functions.f_cud import create_expense
from datetime import datetime
import uuid

st.title("➕ Nuevo Gasto")

# Get current user
user = st.session_state.user

if not user:
    st.error("❌ No hay usuario autenticado.")
    st.stop()

# Expense form
with st.form("new_expense_form"):
    st.subheader("📝 Detalles del Gasto")
    
    # Basic information
    description = st.text_area(
        "📝 Descripción del gasto",
        placeholder="Describe el gasto en detalle...",
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input(
            "💰 Monto ($)",
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
        
        priority = st.selectbox(
            "⚡ Prioridad",
            ["Baja", "Media", "Alta", "Urgente"]
        )
    
    # Additional details
    st.subheader("📋 Información Adicional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        vendor = st.text_input(
            "🏢 Proveedor/Vendedor",
            placeholder="Nombre del proveedor"
        )
        
        receipt_number = st.text_input(
            "🧾 Número de recibo",
            placeholder="Número de factura o recibo"
        )
    
    with col2:
        payment_method = st.selectbox(
            "💳 Método de pago",
            ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia", "Otro"]
        )
        
        reimbursement_type = st.selectbox(
            "🔄 Tipo de reembolso",
            ["Reembolso completo", "Reembolso parcial", "Sin reembolso"]
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
                "id": str(uuid.uuid4()),
                "user_id": user['id'],
                "description": description,
                "amount": amount,
                "category": category,
                "expense_date": expense_date.strftime("%Y-%m-%d"),
                "priority": priority,
                "vendor": vendor,
                "receipt_number": receipt_number,
                "payment_method": payment_method,
                "reimbursement_type": reimbursement_type,
                "comments": comments,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Create the expense
            new_expense = create_expense(expense_data)
            
            if new_expense:
                st.success("✅ Gasto enviado exitosamente!")
                st.balloons()
                
                # Show summary
                st.markdown("---")
                st.subheader("📋 Resumen del Gasto")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {new_expense['id']}")
                    st.write(f"**Descripción:** {new_expense['description']}")
                    st.write(f"**Monto:** ${new_expense['amount']:.2f}")
                    st.write(f"**Categoría:** {new_expense['category']}")
                
                with col2:
                    st.write(f"**Estado:** {new_expense['status']}")
                    st.write(f"**Fecha:** {new_expense['expense_date']}")
                    st.write(f"**Prioridad:** {new_expense['priority']}")
                    st.write(f"**Proveedor:** {new_expense.get('vendor', 'N/A')}")
                
                # Next steps
                st.info("📝 Tu gasto ha sido enviado para aprobación. Recibirás una notificación cuando sea revisado.")
                
                # Clear form
                st.rerun()
            else:
                st.error("❌ Error al crear el gasto. Por favor intenta de nuevo.")
        else:
            st.error("❌ Por favor completa la descripción y el monto del gasto.")

# Help section
with st.expander("❓ ¿Cómo funciona?"):
    st.markdown("""
    ### 📋 Proceso de Solicitud de Gastos
    
    1. **Completa el formulario** con todos los detalles del gasto
    2. **Adjunta el recibo** si está disponible
    3. **Envía la solicitud** para que sea revisada por un aprobador
    4. **Recibe notificaciones** sobre el estado de tu solicitud
    
    ### ⏱️ Tiempos de Respuesta
    
    - **Gastos urgentes:** 24-48 horas
    - **Gastos normales:** 3-5 días hábiles
    - **Gastos grandes:** 1-2 semanas
    
    ### 📞 Contacto
    
    Si tienes preguntas sobre tu solicitud, contacta al equipo de finanzas.
    """)

# Recent expenses preview
st.markdown("---")
st.subheader("🕒 Tus Gastos Recientes")

# This would show the user's recent expenses
# For now, just a placeholder
st.info("📝 Aquí verás tus gastos más recientes una vez que los crees.") 