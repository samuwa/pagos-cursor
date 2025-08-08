import streamlit as st
from functions.f_read import get_expense_statistics, get_recent_expenses, get_all_expenses
from functions.f_read import get_pending_expenses, get_approved_expenses, get_paid_expenses
import plotly.express as px
from datetime import datetime, timedelta

st.subheader("Vista General")

# Get current user
user = st.session_state.user

if not user:
    st.error("No hay usuario autenticado.")
    st.stop()

# Get statistics
stats = get_expense_statistics()

# Summary metrics
st.subheader("Resumen General")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Gastos",
        value=stats.get('total_expenses', 0),
        delta=None
    )

with col2:
    st.metric(
        label="Monto Total",
        value=f"${stats.get('total_amount', 0):,.2f}",
        delta=None
    )

with col3:
    st.metric(
        label="Pendientes",
        value=stats.get('creado_count', 0),
        delta=None
    )

with col4:
    st.metric(
        label="Aprobados",
        value=stats.get('aprobado_count', 0),
        delta=None
    )

# Additional metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Rechazados",
        value=stats.get('rechazado_count', 0),
        delta=None
    )

with col2:
    st.metric(
        label="Pagados",
        value=stats.get('pagado_count', 0),
        delta=None
    )

with col3:
    avg_amount = stats.get('total_amount', 0) / stats.get('total_expenses', 1) if stats.get('total_expenses', 0) > 0 else 0
    st.metric(
        label="Promedio",
        value=f"${avg_amount:,.2f}",
        delta=None
    )

with col4:
    # Calculate completion rate
    total_processed = stats.get('aprobado_count', 0) + stats.get('rechazado_count', 0) + stats.get('pagado_count', 0)
    total_submitted = stats.get('total_expenses', 0)
    completion_rate = (total_processed / total_submitted * 100) if total_submitted > 0 else 0
    st.metric(
        label="Tasa de Completitud",
        value=f"{completion_rate:.1f}%",
        delta=None
    )

# Charts
st.markdown("---")
st.subheader("Gráficos")

# Status distribution pie chart
status_data = {
    'Pendientes': stats.get('creado_count', 0),
    'Aprobados': stats.get('aprobado_count', 0),
    'Rechazados': stats.get('rechazado_count', 0),
    'Pagados': stats.get('pagado_count', 0)
}

if sum(status_data.values()) > 0:
    fig_pie = px.pie(
        values=list(status_data.values()),
        names=list(status_data.keys()),
        title="Distribución de Gastos por Estado"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Recent expenses
st.markdown("---")
st.subheader("Gastos Recientes")

recent_expenses = get_recent_expenses(10)
if recent_expenses:
    for expense in recent_expenses:
        # Status color
        status_colors = {
            'Creado': '🟡',
            'Aprobado': '🟢',
            'Rechazado': '🔴',
            'Pagado': '🟦'
        }
        
        status_icon = status_colors.get(expense['phase'], '⚪')
        
        with st.expander(f"{status_icon} ${expense['amount']:.2f} - {expense['description']} ({expense['phase']})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**ID:** {expense['id']}")
                st.write(f"**Descripción:** {expense['description']}")
                st.write(f"**Categoría:** {expense.get('category', 'N/A')}")
            
            with col2:
                st.write(f"**Monto:** ${expense['amount']:.2f}")
                st.write(f"**Estado:** {expense['status']}")
                st.write(f"**Fecha:** {expense['created_at'][:10]}")
            
            with col3:
                st.write(f"**Prioridad:** {expense.get('priority', 'N/A')}")
                st.write(f"**Proveedor:** {expense.get('vendor', 'N/A')}")
                st.write(f"**Método de pago:** {expense.get('payment_method', 'N/A')}")
else:
    st.info("No hay gastos recientes para mostrar.") 