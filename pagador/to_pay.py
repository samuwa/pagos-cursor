import streamlit as st
from functions.f_read import get_approved_expenses, get_user_by_id
from functions.f_cud import mark_expense_as_paid
from datetime import datetime, timedelta

st.subheader("Gastos Por Pagar")

# Get current user
user = st.session_state.user

if not user:
    st.error("❌ No hay usuario autenticado.")
    st.stop()

# Get approved expenses (these are ready to be paid)
approved_expenses = get_approved_expenses()

# Filter out expenses that are already paid
to_pay_expenses = [e for e in approved_expenses if e['status'] == 'approved']

# Filters
st.subheader("🔍 Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    category_filter = st.selectbox(
        "📂 Categoría",
        ["Todas", "Alimentación", "Transporte", "Hospedaje", "Materiales", "Equipamiento", "Servicios", "Otros"]
    )

with col2:
    priority_filter = st.selectbox(
        "⚡ Prioridad",
        ["Todas", "Baja", "Media", "Alta", "Urgente"]
    )

with col3:
    amount_range = st.slider(
        "💰 Rango de monto",
        min_value=0.0,
        max_value=10000.0,
        value=(0.0, 10000.0),
        step=100.0
    )

# Filter expenses
filtered_expenses = to_pay_expenses

if category_filter != "Todas":
    filtered_expenses = [e for e in filtered_expenses if e.get('category') == category_filter]

if priority_filter != "Todas":
    filtered_expenses = [e for e in filtered_expenses if e.get('priority') == priority_filter]

filtered_expenses = [e for e in filtered_expenses if amount_range[0] <= e['amount'] <= amount_range[1]]

# Summary metrics
if filtered_expenses:
    total_amount = sum(e['amount'] for e in filtered_expenses)
    urgent_count = len([e for e in filtered_expenses if e.get('priority') == 'Urgente'])
    high_count = len([e for e in filtered_expenses if e.get('priority') == 'Alta'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💳 Por Pagar", len(filtered_expenses))
    
    with col2:
        st.metric("💰 Monto Total", f"${total_amount:,.2f}")
    
    with col3:
        st.metric("🚨 Urgentes", urgent_count)
    
    with col4:
        st.metric("⚡ Alta Prioridad", high_count)

# Display expenses
st.subheader(f"📋 Gastos Por Pagar ({len(filtered_expenses)})")

if filtered_expenses:
    # Sort by priority and approval date
    priority_order = {"Urgente": 4, "Alta": 3, "Media": 2, "Baja": 1}
    filtered_expenses.sort(key=lambda x: (priority_order.get(x.get('priority', 'Media'), 0), x['approved_at']), reverse=True)
    
    for expense in filtered_expenses:
        # Get user info
        requester = get_user_by_id(expense['user_id'])
        approver = get_user_by_id(expense['approved_by'])
        
        requester_name = requester['name'] if requester else 'Usuario Desconocido'
        approver_name = approver['name'] if approver else 'Aprobador Desconocido'
        
        # Priority color
        priority_colors = {
            'Urgente': '🔴',
            'Alta': '🟠',
            'Media': '🟡',
            'Baja': '🟢'
        }
        
        priority_icon = priority_colors.get(expense.get('priority', 'Media'), '⚪')
        
        with st.expander(f"{priority_icon} ${expense['amount']:.2f} - {expense['description']} (por {requester_name})"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**ID:** {expense['id']}")
                st.write(f"**Solicitante:** {requester_name}")
                st.write(f"**Descripción:** {expense['description']}")
                st.write(f"**Categoría:** {expense.get('category', 'N/A')}")
                st.write(f"**Fecha de gasto:** {expense.get('expense_date', expense['created_at'][:10])}")
            
            with col2:
                st.write(f"**Monto:** ${expense['amount']:.2f}")
                st.write(f"**Aprobado por:** {approver_name}")
                st.write(f"**Fecha de aprobación:** {expense['approved_at'][:10]}")
                st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
                st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
            
            with col3:
                # Payment actions
                if st.button("💳 Marcar como Pagado", key=f"pay_{expense['id']}"):
                    st.session_state.pay_expense = expense
                    st.rerun()
                
                if st.button("👁️ Ver Detalles", key=f"view_{expense['id']}"):
                    st.session_state.view_expense = expense
                    st.rerun()
            
            # Show comments if any
            if expense.get('comments'):
                st.markdown("---")
                st.write("**💬 Comentarios del solicitante:**")
                st.write(expense['comments'])
            
            if expense.get('approver_comments'):
                st.markdown("---")
                st.write("**💬 Comentarios del aprobador:**")
                st.write(expense['approver_comments'])
    
    # Payment form
    if 'pay_expense' in st.session_state:
        expense = st.session_state.pay_expense
        requester = get_user_by_id(expense['user_id'])
        
        st.markdown("---")
        st.subheader("💳 Marcar como Pagado")
        
        with st.form("pay_expense_form"):
            st.write(f"**Marcando como pagado:** {expense['description']} por ${expense['amount']:.2f}")
            st.write(f"**Solicitante:** {requester['name'] if requester else 'N/A'}")
            
            payment_date = st.date_input(
                "📅 Fecha de pago",
                value=datetime.now().date()
            )
            
            payment_method = st.selectbox(
                "💳 Método de pago utilizado",
                ["Transferencia bancaria", "Cheque", "Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Otro"]
            )
            
            payment_reference = st.text_input(
                "🔢 Número de referencia",
                placeholder="Número de cheque, transferencia, etc."
            )
            
            payment_notes = st.text_area(
                "📝 Notas de pago",
                placeholder="Notas adicionales sobre el pago..."
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("💳 Confirmar Pago")
            with col2:
                if st.form_submit_button("❌ Cancelar"):
                    del st.session_state.pay_expense
                    st.rerun()
            
            if submitted:
                # Mark as paid
                if mark_expense_as_paid(expense['id'], user['id'], payment_date.strftime("%Y-%m-%d")):
                    st.success("💳 Gasto marcado como pagado exitosamente!")
                    del st.session_state.pay_expense
                    st.rerun()
    
    # View expense details
    if 'view_expense' in st.session_state:
        expense = st.session_state.view_expense
        requester = get_user_by_id(expense['user_id'])
        approver = get_user_by_id(expense['approved_by'])
        
        st.markdown("---")
        st.subheader("👁️ Detalles del Gasto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**ID:** {expense['id']}")
            st.write(f"**Solicitante:** {requester['name'] if requester else 'N/A'}")
            st.write(f"**Email del solicitante:** {requester['email'] if requester else 'N/A'}")
            st.write(f"**Descripción:** {expense['description']}")
            st.write(f"**Categoría:** {expense.get('category', 'N/A')}")
            st.write(f"**Monto:** ${expense['amount']:.2f}")
            st.write(f"**Prioridad:** {expense.get('priority', 'N/A')}")
        
        with col2:
            st.write(f"**Estado:** {expense['status']}")
            st.write(f"**Aprobado por:** {approver['name'] if approver else 'N/A'}")
            st.write(f"**Fecha de aprobación:** {expense['approved_at'][:10]}")
            st.write(f"**Fecha de gasto:** {expense.get('expense_date', expense['created_at'][:10])}")
            st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
            st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
            st.write(f"**Tipo de reembolso:** {expense.get('reimbursement_type', 'N/A')}")
        
        if expense.get('comments'):
            st.markdown("---")
            st.write("**💬 Comentarios del solicitante:**")
            st.write(expense['comments'])
        
        if expense.get('approver_comments'):
            st.markdown("---")
            st.write("**💬 Comentarios del aprobador:**")
            st.write(expense['approver_comments'])
        
        if st.button("❌ Cerrar"):
            del st.session_state.view_expense
            st.rerun()

else:
    st.success("🎉 ¡No hay gastos pendientes de pago!")

# Quick actions
st.markdown("---")
st.subheader("⚡ Acciones Rápidas")

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Ver Pagados", use_container_width=True):
        st.switch_page("pagador/paid.py")

with col2:
    if st.button("📊 Ver Estadísticas", use_container_width=True):
        st.info("📈 Funcionalidad de estadísticas en desarrollo...") 