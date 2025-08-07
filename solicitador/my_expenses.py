import streamlit as st
from functions.f_read import get_expenses_by_user, get_expense_by_id
from functions.f_cud import update_expense, delete_expense
from datetime import datetime

st.title("📝 Mis Gastos")

# Get current user
user = st.session_state.user

if not user:
    st.error("❌ No hay usuario autenticado.")
    st.stop()

# Get user's expenses
expenses = get_expenses_by_user(user['id'])

# Filters
st.subheader("🔍 Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox(
        "📊 Estado",
        ["Todos", "pending", "approved", "rejected", "paid"]
    )

with col2:
    category_filter = st.selectbox(
        "📂 Categoría",
        ["Todas", "Alimentación", "Transporte", "Hospedaje", "Materiales", "Equipamiento", "Servicios", "Otros"]
    )

with col3:
    search_query = st.text_input(
        "🔍 Buscar",
        placeholder="Buscar en descripción..."
    )

# Filter expenses
filtered_expenses = expenses

if status_filter != "Todos":
    filtered_expenses = [e for e in filtered_expenses if e['status'] == status_filter]

if category_filter != "Todas":
    filtered_expenses = [e for e in filtered_expenses if e.get('category') == category_filter]

if search_query:
    filtered_expenses = [e for e in filtered_expenses if search_query.lower() in e['description'].lower()]

# Summary metrics
if filtered_expenses:
    total_amount = sum(e['amount'] for e in filtered_expenses)
    pending_amount = sum(e['amount'] for e in filtered_expenses if e['status'] == 'pending')
    approved_amount = sum(e['amount'] for e in filtered_expenses if e['status'] == 'approved')
    paid_amount = sum(e['amount'] for e in filtered_expenses if e['status'] == 'paid')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total", f"${total_amount:,.2f}")
    
    with col2:
        st.metric("⏳ Pendientes", f"${pending_amount:,.2f}")
    
    with col3:
        st.metric("✅ Aprobados", f"${approved_amount:,.2f}")
    
    with col4:
        st.metric("💳 Pagados", f"${paid_amount:,.2f}")

# Display expenses
st.subheader(f"📋 Mis Gastos ({len(filtered_expenses)})")

if filtered_expenses:
    # Sort by creation date (newest first)
    filtered_expenses.sort(key=lambda x: x['created_at'], reverse=True)
    
    for expense in filtered_expenses:
        # Status color mapping
        status_colors = {
            'pending': '🟡',
            'approved': '🟢',
            'rejected': '🔴',
            'paid': '🟦'
        }
        
        status_icon = status_colors.get(expense['status'], '⚪')
        
        with st.expander(f"{status_icon} ${expense['amount']:.2f} - {expense['description']} ({expense['status']})"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**ID:** {expense['id']}")
                st.write(f"**Descripción:** {expense['description']}")
                st.write(f"**Categoría:** {expense.get('category', 'N/A')}")
                st.write(f"**Fecha de gasto:** {expense.get('expense_date', expense['created_at'][:10])}")
                st.write(f"**Prioridad:** {expense.get('priority', 'N/A')}")
            
            with col2:
                st.write(f"**Estado:** {expense['status']}")
                st.write(f"**Monto:** ${expense['amount']:.2f}")
                st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
                st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
                st.write(f"**Creado:** {expense['created_at'][:10]}")
                
                if expense.get('approved_at'):
                    st.write(f"**Aprobado:** {expense['approved_at'][:10]}")
                
                if expense.get('paid_at'):
                    st.write(f"**Pagado:** {expense['paid_at'][:10]}")
            
            with col3:
                # Status-specific actions
                if expense['status'] == 'pending':
                    if st.button("✏️ Editar", key=f"edit_{expense['id']}"):
                        st.session_state.edit_expense = expense
                        st.rerun()
                    
                    if st.button("🗑️ Cancelar", key=f"cancel_{expense['id']}"):
                        if delete_expense(expense['id']):
                            st.success("🗑️ Gasto cancelado!")
                            st.rerun()
                
                elif expense['status'] == 'rejected':
                    if expense.get('approver_comments'):
                        st.info(f"💬 Comentario: {expense['approver_comments']}")
                
                # View details button
                if st.button("👁️ Ver Detalles", key=f"view_{expense['id']}"):
                    st.session_state.view_expense = expense
                    st.rerun()
    
    # Edit expense form
    if 'edit_expense' in st.session_state:
        expense = st.session_state.edit_expense
        
        st.markdown("---")
        st.subheader("✏️ Editar Gasto")
        
        with st.form("edit_expense_form"):
            st.write(f"**Editando:** {expense['description']}")
            
            description = st.text_area("📝 Descripción", value=expense['description'])
            amount = st.number_input("💰 Monto", value=float(expense['amount']), min_value=0.01, step=0.01)
            category = st.selectbox("📂 Categoría", ["Alimentación", "Transporte", "Hospedaje", "Materiales", "Equipamiento", "Servicios", "Otros"], index=["Alimentación", "Transporte", "Hospedaje", "Materiales", "Equipamiento", "Servicios", "Otros"].index(expense.get('category', 'Otros')))
            priority = st.selectbox("⚡ Prioridad", ["Baja", "Media", "Alta", "Urgente"], index=["Baja", "Media", "Alta", "Urgente"].index(expense.get('priority', 'Media')))
            comments = st.text_area("💬 Comentarios", value=expense.get('comments', ''))
            
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
                    "priority": priority,
                    "comments": comments
                }
                
                if update_expense(expense['id'], update_data):
                    st.success("✅ Gasto actualizado exitosamente!")
                    del st.session_state.edit_expense
                    st.rerun()
    
    # View expense details
    if 'view_expense' in st.session_state:
        expense = st.session_state.view_expense
        
        st.markdown("---")
        st.subheader("👁️ Detalles del Gasto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**ID:** {expense['id']}")
            st.write(f"**Descripción:** {expense['description']}")
            st.write(f"**Categoría:** {expense.get('category', 'N/A')}")
            st.write(f"**Monto:** ${expense['amount']:.2f}")
            st.write(f"**Estado:** {expense['status']}")
            st.write(f"**Prioridad:** {expense.get('priority', 'N/A')}")
        
        with col2:
            st.write(f"**Fecha de gasto:** {expense.get('expense_date', expense['created_at'][:10])}")
            st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
            st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
            st.write(f"**Tipo de reembolso:** {expense.get('reimbursement_type', 'N/A')}")
            st.write(f"**Número de recibo:** {expense.get('receipt_number', 'N/A')}")
            st.write(f"**Creado:** {expense['created_at'][:10]}")
        
        if expense.get('comments'):
            st.markdown("---")
            st.write("**💬 Comentarios:**")
            st.write(expense['comments'])
        
        if expense.get('approver_comments'):
            st.markdown("---")
            st.write("**💬 Comentarios del aprobador:**")
            st.write(expense['approver_comments'])
        
        if st.button("❌ Cerrar"):
            del st.session_state.view_expense
            st.rerun()

else:
    st.info("📝 No tienes gastos registrados. ¡Crea tu primer gasto!")

# Quick actions
st.markdown("---")
st.subheader("⚡ Acciones Rápidas")

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Nuevo Gasto", use_container_width=True):
        st.switch_page("solicitador/new_expense.py")

with col2:
    if st.button("📊 Ver Estadísticas", use_container_width=True):
        st.info("📈 Funcionalidad de estadísticas en desarrollo...") 