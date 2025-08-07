import streamlit as st
from functions.f_read import get_paid_expenses, get_user_by_id
from datetime import datetime, timedelta

st.subheader("Gastos Pagados")

# Get current user
user = st.session_state.user

if not user:
    st.error("❌ No hay usuario autenticado.")
    st.stop()

# Get paid expenses
paid_expenses = get_paid_expenses()

# Filters
st.subheader("🔍 Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    category_filter = st.selectbox(
        "📂 Categoría",
        ["Todas", "Alimentación", "Transporte", "Hospedaje", "Materiales", "Equipamiento", "Servicios", "Otros"]
    )

with col2:
    date_range = st.date_input(
        "📅 Rango de fechas",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
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
filtered_expenses = paid_expenses

if category_filter != "Todas":
    filtered_expenses = [e for e in filtered_expenses if e.get('category') == category_filter]

if len(date_range) == 2:
    start_date = date_range[0].strftime("%Y-%m-%d")
    end_date = date_range[1].strftime("%Y-%m-%d")
    filtered_expenses = [e for e in filtered_expenses if start_date <= e['paid_at'][:10] <= end_date]

filtered_expenses = [e for e in filtered_expenses if amount_range[0] <= e['amount'] <= amount_range[1]]

# Summary metrics
if filtered_expenses:
    total_amount = sum(e['amount'] for e in filtered_expenses)
    avg_amount = total_amount / len(filtered_expenses)
    recent_count = len([e for e in filtered_expenses if e['paid_at'][:10] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Total Pagados", len(filtered_expenses))
    
    with col2:
        st.metric("💰 Monto Total", f"${total_amount:,.2f}")
    
    with col3:
        st.metric("📊 Promedio", f"${avg_amount:,.2f}")
    
    with col4:
        st.metric("🕒 Últimos 7 días", recent_count)

# Display expenses
st.subheader(f"📋 Gastos Pagados ({len(filtered_expenses)})")

if filtered_expenses:
    # Sort by payment date (newest first)
    filtered_expenses.sort(key=lambda x: x['paid_at'], reverse=True)
    
    for expense in filtered_expenses:
        # Get user info
        requester = get_user_by_id(expense['user_id'])
        approver = get_user_by_id(expense['approved_by'])
        payer = get_user_by_id(expense['paid_by'])
        
        requester_name = requester['name'] if requester else 'Usuario Desconocido'
        approver_name = approver['name'] if approver else 'Aprobador Desconocido'
        payer_name = payer['name'] if payer else 'Pagador Desconocido'
        
        with st.expander(f"✅ ${expense['amount']:.2f} - {expense['description']} (por {requester_name})"):
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
                st.write(f"**Pagado por:** {payer_name}")
                st.write(f"**Fecha de pago:** {expense['paid_at'][:10]}")
                st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
            
            with col3:
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
    
    # View expense details
    if 'view_expense' in st.session_state:
        expense = st.session_state.view_expense
        requester = get_user_by_id(expense['user_id'])
        approver = get_user_by_id(expense['approved_by'])
        payer = get_user_by_id(expense['paid_by'])
        
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
            st.write(f"**Pagado por:** {payer['name'] if payer else 'N/A'}")
            st.write(f"**Fecha de pago:** {expense['paid_at'][:10]}")
            st.write(f"**Fecha de gasto:** {expense.get('expense_date', expense['created_at'][:10])}")
            st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
            st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
        
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
    st.info("📝 No hay gastos pagados para mostrar.")

# Quick actions
st.markdown("---")
st.subheader("⚡ Acciones Rápidas")

col1, col2 = st.columns(2)

with col1:
    if st.button("💳 Ver Por Pagar", use_container_width=True):
        st.switch_page("pagador/to_pay.py")

with col2:
    if st.button("📊 Ver Estadísticas", use_container_width=True):
        st.info("📈 Funcionalidad de estadísticas en desarrollo...") 