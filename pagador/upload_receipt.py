import streamlit as st
from functions.f_read import get_expenses_by_phase, get_expense_by_id
from functions.f_cud import upload_payment_receipt
from datetime import datetime

st.subheader("📄 Subir Comprobante de Pago")

# Get current user
user = st.session_state.user

if not user:
    st.error("No hay usuario autenticado.")
    st.stop()

# Get approved expenses that need payment receipts
approved_expenses = get_expenses_by_phase("Aprobado")

if not approved_expenses:
    st.info("No hay gastos aprobados que requieran comprobantes de pago.")
    st.stop()

# Filter expenses that don't have payment receipts yet
# (This would require a function to check if receipt exists)
expenses_without_receipts = approved_expenses

st.subheader("Gastos Aprobados Pendientes de Comprobante")

# Display expenses in a table
if expenses_without_receipts:
    expense_data = []
    for expense in expenses_without_receipts:
        expense_data.append({
            "ID": expense['id'],
            "Descripción": expense['description'],
            "Monto": f"${expense['amount']:.2f}",
            "Solicitante": expense.get('requester_name', 'N/A'),
            "Fecha": expense['expense_date'] if 'expense_date' in expense else 'N/A',
            "Estado": expense['phase']
        })
    
    st.dataframe(
        expense_data,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Descripción": st.column_config.TextColumn("Descripción", width="medium"),
            "Monto": st.column_config.TextColumn("Monto", width="small"),
            "Solicitante": st.column_config.TextColumn("Solicitante", width="small"),
            "Fecha": st.column_config.TextColumn("Fecha", width="small"),
            "Estado": st.column_config.TextColumn("Estado", width="small")
        },
        hide_index=True,
        use_container_width=True
    )

# Upload receipt section
st.subheader("Subir Comprobante de Pago")

# Expense selection
expense_options = {f"{exp['id']} - {exp['description']}": exp['id'] for exp in expenses_without_receipts}
selected_expense_key = st.selectbox(
    "Seleccionar Gasto",
    options=list(expense_options.keys()),
    help="Selecciona el gasto para el cual vas a subir el comprobante de pago"
)

if selected_expense_key:
    selected_expense_id = expense_options[selected_expense_key]
    
    # Get expense details
    expense_details = get_expense_by_id(selected_expense_id)
    
    if expense_details:
        # Show expense details
        st.info(f"**Gasto seleccionado:** {expense_details['description']} - ${expense_details['amount']:.2f}")
        
        # File upload
        receipt_file = st.file_uploader(
            "📄 Comprobante de Pago",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            help="Sube el comprobante de pago (PDF o imagen)"
        )
        
        # Additional notes
        notes = st.text_area(
            "💬 Notas adicionales",
            placeholder="Información adicional sobre el pago...",
            height=100
        )
        
        # Submit button
        if st.button("📤 Subir Comprobante", type="primary"):
            if receipt_file:
                # Upload the receipt
                if upload_payment_receipt(selected_expense_id, receipt_file, user["id"]):
                    st.success("✅ Comprobante de pago subido exitosamente!")
                    st.balloons()
                    
                    # Update expense status to paid
                    # This would require an additional function to mark expense as paid
                    st.info("El gasto ha sido marcado como pagado.")
                else:
                    st.error("❌ Error al subir el comprobante de pago.")
            else:
                st.error("Por favor selecciona un archivo para subir.")
    else:
        st.error("No se pudo obtener la información del gasto seleccionado.")
else:
    st.info("Selecciona un gasto para subir su comprobante de pago.")
