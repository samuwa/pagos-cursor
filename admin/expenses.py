import streamlit as st
from functions.f_read import get_all_expenses, get_expense_by_id, search_expenses
from functions.f_read import get_expenses_by_status, get_expenses_by_date_range, get_expenses_by_amount_range
from functions.f_cud import update_expense, delete_expense
from functions.f_read import get_user_by_id
from datetime import datetime, timedelta

st.subheader("Gestión de Gastos")

# Filters
st.subheader("🔍 Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox(
        "Estado",
        ["Todos", "pending", "approved", "rejected", "paid"]
    )

with col2:
    date_range = st.date_input(
        "Rango de fechas",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )

with col3:
    amount_range = st.slider(
        "Rango de monto",
        min_value=0.0,
        max_value=10000.0,
        value=(0.0, 10000.0),
        step=100.0
    )

# Search
search_query = st.text_input("Buscar gastos", placeholder="Descripción o categoría...")

# Get expenses based on filters
if status_filter == "Todos":
    expenses = get_all_expenses()
else:
    expenses = get_expenses_by_status(status_filter)

# Apply date filter
if len(date_range) == 2:
    start_date = date_range[0].strftime("%Y-%m-%d")
    end_date = date_range[1].strftime("%Y-%m-%d")
    expenses = [e for e in expenses if start_date <= e['created_at'][:10] <= end_date]

# Apply amount filter
expenses = [e for e in expenses if amount_range[0] <= e['amount'] <= amount_range[1]]

# Apply search filter
if search_query:
    expenses = [e for e in expenses if search_query.lower() in e['description'].lower() or search_query.lower() in e.get('category', '').lower()]

# Display expenses
st.subheader(f"Gastos ({len(expenses)})")

if expenses:
    # Summary metrics
    total_amount = sum(e['amount'] for e in expenses)
    avg_amount = total_amount / len(expenses) if expenses else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", f"${total_amount:,.2f}")
    with col2:
        st.metric("Promedio", f"${avg_amount:,.2f}")
    with col3:
        st.metric("Cantidad", len(expenses))
    
    st.markdown("---")
    
    # Display each expense
    for expense in expenses:
        with st.expander(f"${expense['amount']:.2f} - {expense['description']} ({expense['phase']})"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**ID:** {expense['id']}")
                st.write(f"**Descripción:** {expense['description']}")
                st.write(f"**Categoría:** {expense.get('category', 'N/A')}")
                st.write(f"**Fecha:** {expense['created_at'][:10]}")
            
            with col2:
                # Get user info
                user = get_user_by_id(expense['user_id'])
                st.write(f"**Usuario:** {user['name'] if user else 'N/A'}")
                st.write(f"**Estado:** {expense['phase']}")
                st.write(f"**Monto:** ${expense['amount']:.2f}")
                
                if expense.get('approved_by'):
                    approver = get_user_by_id(expense['approved_by'])
                    st.write(f"**Aprobado por:** {approver['name'] if approver else 'N/A'}")
                
                if expense.get('paid_by'):
                    payer = get_user_by_id(expense['paid_by'])
                    st.write(f"**Pagado por:** {payer['name'] if payer else 'N/A'}")
            
            with col3:
                # Action buttons
                if expense['phase'] == 'Creado':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✅ Aprobar", key=f"approve_{expense['id']}"):
                            if update_expense(expense['id'], {'phase': 'Aprobado'}):
                                st.success("✅ Gasto aprobado!")
                                st.rerun()
                    with col_b:
                        if st.button("❌ Rechazar", key=f"reject_{expense['id']}"):
                            if update_expense(expense['id'], {'phase': 'Rechazado'}):
                                st.success("❌ Gasto rechazado!")
                                st.rerun()
                
                elif expense['phase'] == 'Aprobado':
                    if st.button("💳 Marcar como Pagado", key=f"pay_{expense['id']}"):
                        if update_expense(expense['id'], {'phase': 'Pagado'}):
                            st.success("💳 Gasto marcado como pagado!")
                            st.rerun()
                
                # Edit button
                if st.button("✏️ Editar", key=f"edit_{expense['id']}"):
                    st.session_state.edit_expense = expense
                    st.rerun()
                
                # Delete button
                if st.button("🗑️ Eliminar", key=f"delete_{expense['id']}"):
                    if delete_expense(expense['id']):
                        st.success("🗑️ Gasto eliminado!")
                        st.rerun()
else:
    st.info("📝 No hay gastos que coincidan con los filtros aplicados.")

# Edit expense form
if 'edit_expense' in st.session_state:
    expense = st.session_state.edit_expense
    
    st.markdown("---")
    st.subheader("✏️ Editar Gasto")
    
    with st.form("edit_expense_form"):
        st.write(f"**Editando:** {expense['description']}")
        
        description = st.text_input("📝 Descripción", value=expense['description'])
        amount = st.number_input("💰 Monto", value=float(expense['amount']), min_value=0.0, step=0.01)
        category = st.text_input("📂 Categoría", value=expense.get('category', ''))
        status = st.selectbox("Estado", ["Creado", "Aprobado", "Rechazado", "Pagado"], index=["Creado", "Aprobado", "Rechazado", "Pagado"].index(expense['phase']))
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Guardar Cambios")
        with col2:
            if st.form_submit_button("❌ Cancelar"):
                del st.session_state.edit_expense
                st.rerun()
        
        if submitted:
            update_data = {
                "description": description,
                "amount": amount,
                "category": category,
                "phase": status
            }
            
            if update_expense(expense['id'], update_data):
                st.success("✅ Gasto actualizado exitosamente!")
                del st.session_state.edit_expense
                st.rerun() 