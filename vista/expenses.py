import streamlit as st
from functions.f_read import get_all_expenses, get_expenses_by_phase, get_user_by_id
from functions.f_read import search_expenses, get_expenses_by_date_range, get_expenses_by_amount_range
from datetime import datetime, timedelta

st.title("Vista de Gastos")

# Get current user
user = st.session_state.user

if not user:
    st.error("No hay usuario autenticado.")
    st.stop()

# Filters
st.subheader("Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox(
        "Estado",
        ["Todos", "Creado", "Aprobado", "Rechazado", "Pagado"]
    )

with col2:
    category_filter = st.selectbox(
        "Categoría",
        ["Todas", "Alimentación", "Transporte", "Hospedaje", "Materiales", "Equipamiento", "Servicios", "Otros"]
    )

with col3:
    priority_filter = st.selectbox(
        "Prioridad",
        ["Todas", "Baja", "Media", "Alta", "Urgente"]
    )

# Additional filters
col1, col2 = st.columns(2)

with col1:
    date_range = st.date_input(
        "Rango de fechas",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )

with col2:
    amount_range = st.slider(
        "Rango de monto",
        min_value=0.0,
        max_value=10000.0,
        value=(0.0, 10000.0),
        step=100.0
    )

# Search
search_query = st.text_input(
    "Buscar gastos",
    placeholder="Buscar en descripción o categoría..."
)

# Get expenses based on filters
if status_filter == "Todos":
    expenses = get_all_expenses()
else:
    expenses = get_expenses_by_phase(status_filter)

# Apply additional filters
if category_filter != "Todas":
    expenses = [e for e in expenses if e.get('category') == category_filter]

if priority_filter != "Todas":
    expenses = [e for e in expenses if e.get('priority') == priority_filter]

if len(date_range) == 2:
    start_date = date_range[0].strftime("%Y-%m-%d")
    end_date = date_range[1].strftime("%Y-%m-%d")
    expenses = [e for e in expenses if start_date <= e['created_at'][:10] <= end_date]

expenses = [e for e in expenses if amount_range[0] <= e['amount'] <= amount_range[1]]

if search_query:
    expenses = [e for e in expenses if search_query.lower() in e['description'].lower() or search_query.lower() in e.get('category', '').lower()]

# Summary metrics
if expenses:
    total_amount = sum(e['amount'] for e in expenses)
    avg_amount = total_amount / len(expenses)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Gastos", len(expenses))
    
    with col2:
        st.metric("Monto Total", f"${total_amount:,.2f}")
    
    with col3:
        st.metric("Promedio", f"${avg_amount:,.2f}")
    
    with col4:
        # Count by status
        status_counts = {}
        for expense in expenses:
            status = expense['phase']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        most_common_status = max(status_counts.items(), key=lambda x: x[1])[0] if status_counts else 'N/A'
        st.metric("Estado más común", most_common_status)

# Display expenses
st.subheader(f"Gastos ({len(expenses)})")

if expenses:
    # Sort by creation date (newest first)
    expenses.sort(key=lambda x: x['created_at'], reverse=True)
    
    for expense in expenses:
        # Get user info
        requester = get_user_by_id(expense['user_id'])
        requester_name = requester['name'] if requester else 'Usuario Desconocido'
        
        # Status color
        status_colors = {
            'Creado': '🟡',
            'Aprobado': '🟢',
            'Rechazado': '🔴',
            'Pagado': '🟦'
        }
        
        status_icon = status_colors.get(expense['phase'], '⚪')
        
        with st.expander(f"{status_icon} ${expense['amount']:.2f} - {expense['description']} (por {requester_name})"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**ID:** {expense['id']}")
                st.write(f"**Solicitante:** {requester_name}")
                st.write(f"**Descripción:** {expense['description']}")
                st.write(f"**Categoría:** {expense.get('category', 'N/A')}")
                st.write(f"**Fecha de gasto:** {expense.get('expense_date', expense['created_at'][:10])}")
            
            with col2:
                st.write(f"**Monto:** ${expense['amount']:.2f}")
                st.write(f"**Estado:** {expense['status']}")
                st.write(f"**Prioridad:** {expense.get('priority', 'N/A')}")
                st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
                st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
            
            with col3:
                if st.button("Ver Detalles", key=f"view_{expense['id']}"):
                    st.session_state.view_expense = expense
                    st.rerun()
            
            # Show comments if any
            if expense.get('comments'):
                st.markdown("---")
                st.write("**Comentarios del solicitante:**")
                st.write(expense['comments'])
            
            if expense.get('approver_comments'):
                st.markdown("---")
                st.write("**Comentarios del aprobador:**")
                st.write(expense['approver_comments'])
    
    # View expense details
    if 'view_expense' in st.session_state:
        expense = st.session_state.view_expense
        requester = get_user_by_id(expense['user_id'])
        approver = get_user_by_id(expense['approved_by']) if expense.get('approved_by') else None
        payer = get_user_by_id(expense['paid_by']) if expense.get('paid_by') else None
        
        st.markdown("---")
        st.subheader("Detalles del Gasto")
        
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
            st.write(f"**Fecha de gasto:** {expense.get('expense_date', expense['created_at'][:10])}")
            st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
            st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
            st.write(f"**Tipo de reembolso:** {expense.get('reimbursement_type', 'N/A')}")
            
            if approver:
                st.write(f"**Aprobado por:** {approver['name']}")
                if expense.get('approved_at'):
                    st.write(f"**Fecha de aprobación:** {expense['approved_at'][:10]}")
            
            if payer:
                st.write(f"**Pagado por:** {payer['name']}")
                if expense.get('paid_at'):
                    st.write(f"**Fecha de pago:** {expense['paid_at'][:10]}")
        
        if expense.get('comments'):
            st.markdown("---")
            st.write("**Comentarios del solicitante:**")
            st.write(expense['comments'])
        
        if expense.get('approver_comments'):
            st.markdown("---")
            st.write("**Comentarios del aprobador:**")
            st.write(expense['approver_comments'])
        
        if st.button("Cerrar"):
            del st.session_state.view_expense
            st.rerun()

else:
    st.info("No hay gastos que coincidan con los filtros aplicados.")

# Quick actions
st.markdown("---")
st.subheader("Acciones Rápidas")

col1, col2 = st.columns(2)

with col1:
    if st.button("Ver Vista General", use_container_width=True):
        st.switch_page("vista/overview.py")

with col2:
    if st.button("Ver Estadísticas", use_container_width=True):
        st.info("Funcionalidad de estadísticas en desarrollo...") 