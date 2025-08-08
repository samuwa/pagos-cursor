import streamlit as st
from functions.f_read import get_pending_expenses, get_user_by_id
from functions.f_cud import approve_expense, reject_expense
from datetime import datetime

st.subheader("Gastos Pendientes")

# Get current user
user = st.session_state.user

if not user:
    st.error("❌ No hay usuario autenticado.")
    st.stop()

# Get pending expenses
pending_expenses = get_pending_expenses()

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
filtered_expenses = pending_expenses

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
        st.metric("📋 Total Pendientes", len(filtered_expenses))
    
    with col2:
        st.metric("💰 Monto Total", f"${total_amount:,.2f}")
    
    with col3:
        st.metric("🚨 Urgentes", urgent_count)
    
    with col4:
        st.metric("⚡ Alta Prioridad", high_count)

# Display expenses
st.subheader(f"📋 Gastos Pendientes ({len(filtered_expenses)})")

if filtered_expenses:
    # Sort by priority and creation date
    priority_order = {"Urgente": 4, "Alta": 3, "Media": 2, "Baja": 1}
    filtered_expenses.sort(key=lambda x: (priority_order.get(x.get('priority', 'Media'), 0), x['created_at']), reverse=True)
    
    for expense in filtered_expenses:
        # Get requester info
        requester = get_user_by_id(expense['user_id'])
        requester_name = requester['name'] if requester else 'Usuario Desconocido'
        
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
                st.write(f"**Prioridad:** {expense.get('priority', 'N/A')}")
                st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
                st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
                st.write(f"**Solicitado:** {expense['created_at'][:10]}")
            
            with col3:
                # Approval actions
                if st.button("✅ Aprobar", key=f"approve_{expense['id']}"):
                    st.session_state.approve_expense = expense
                    st.rerun()
                
                if st.button("❌ Rechazar", key=f"reject_{expense['id']}"):
                    st.session_state.reject_expense = expense
                    st.rerun()
                
                if st.button("👁️ Ver Detalles", key=f"view_{expense['id']}"):
                    st.session_state.view_expense = expense
                    st.rerun()
            
            # Show comments if any
            if expense.get('comments'):
                st.markdown("---")
                st.write("**💬 Comentarios del solicitante:**")
                st.write(expense['comments'])
    
    # Approval form
    if 'approve_expense' in st.session_state:
        expense = st.session_state.approve_expense
        
        st.markdown("---")
        st.subheader("✅ Aprobar Gasto")
        
        with st.form("approve_expense_form"):
            st.write(f"**Aprobando:** {expense['description']} por ${expense['amount']:.2f}")
            
            comments = st.text_area(
                "💬 Comentarios de aprobación (opcional)",
                placeholder="Comentarios adicionales..."
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("✅ Confirmar Aprobación")
            with col2:
                if st.form_submit_button("❌ Cancelar"):
                    del st.session_state.approve_expense
                    st.rerun()
            
            if submitted:
                if approve_expense(expense['id'], user['id'], comments):
                    st.success("✅ Gasto aprobado exitosamente!")
                    del st.session_state.approve_expense
                    st.rerun()
    
    # Rejection form
    if 'reject_expense' in st.session_state:
        expense = st.session_state.reject_expense
        
        st.markdown("---")
        st.subheader("❌ Rechazar Gasto")
        
        with st.form("reject_expense_form"):
            st.write(f"**Rechazando:** {expense['description']} por ${expense['amount']:.2f}")
            
            comments = st.text_area(
                "💬 Motivo del rechazo",
                placeholder="Explica por qué se rechaza este gasto...",
                required=True
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("❌ Confirmar Rechazo")
            with col2:
                if st.form_submit_button("❌ Cancelar"):
                    del st.session_state.reject_expense
                    st.rerun()
            
            if submitted:
                if comments.strip():
                    if reject_expense(expense['id'], user['id'], comments):
                        st.success("❌ Gasto rechazado exitosamente!")
                        del st.session_state.reject_expense
                        st.rerun()
                else:
                    st.error("❌ Por favor proporciona un motivo para el rechazo.")
    
    # View expense details
    if 'view_expense' in st.session_state:
        expense = st.session_state.view_expense
        requester = get_user_by_id(expense['user_id'])
        
        st.markdown("---")
        st.subheader("👁️ Detalles del Gasto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**ID:** {expense['id']}")
            st.write(f"**Solicitante:** {requester['name'] if requester else 'N/A'}")
            st.write(f"**Email:** {requester['email'] if requester else 'N/A'}")
            st.write(f"**Descripción:** {expense['description']}")
            st.write(f"**Categoría:** {expense.get('category', 'N/A')}")
            st.write(f"**Monto:** ${expense['amount']:.2f}")
        
        with col2:
            st.write(f"**Estado:** {expense['status']}")
            st.write(f"**Prioridad:** {expense.get('priority', 'N/A')}")
            st.write(f"**Fecha de gasto:** {expense.get('expense_date', expense['created_at'][:10])}")
            st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
            st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
            st.write(f"**Tipo de reembolso:** {expense.get('reimbursement_type', 'N/A')}")
        
        if expense.get('comments'):
            st.markdown("---")
            st.write("**💬 Comentarios del solicitante:**")
            st.write(expense['comments'])
        
        if st.button("❌ Cerrar"):
            del st.session_state.view_expense
            st.rerun()

else:
    st.success("🎉 ¡No hay gastos pendientes para revisar!") 