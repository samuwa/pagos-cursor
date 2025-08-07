import streamlit as st
from functions.f_read import get_expense_statistics, get_recent_expenses, get_all_users
from functions.f_read import get_pending_expenses, get_approved_expenses, get_paid_expenses
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.title("📊 Dashboard Administrativo")

# Get statistics
stats = get_expense_statistics()

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📋 Total Gastos",
        value=stats.get('total_expenses', 0),
        delta=None
    )

with col2:
    st.metric(
        label="💰 Total Monto",
        value=f"${stats.get('total_amount', 0):,.2f}",
        delta=None
    )

with col3:
    st.metric(
        label="⏳ Pendientes",
        value=stats.get('pending_count', 0),
        delta=None
    )

with col4:
    st.metric(
        label="✅ Aprobados",
        value=stats.get('approved_count', 0),
        delta=None
    )

# Charts section
st.markdown("---")
st.subheader("📈 Gráficos")

# Status distribution pie chart
status_data = {
    'Pendientes': stats.get('pending_count', 0),
    'Aprobados': stats.get('approved_count', 0),
    'Rechazados': stats.get('rejected_count', 0),
    'Pagados': stats.get('paid_count', 0)
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
st.subheader("🕒 Gastos Recientes")

recent_expenses = get_recent_expenses(10)
if recent_expenses:
    for expense in recent_expenses:
        with st.expander(f"${expense['amount']:.2f} - {expense['description']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Usuario:** {expense.get('user_name', 'N/A')}")
            with col2:
                st.write(f"**Estado:** {expense['status']}")
            with col3:
                st.write(f"**Fecha:** {expense['created_at'][:10]}")
else:
    st.info("📝 No hay gastos recientes para mostrar.")

# Quick actions
st.markdown("---")
st.subheader("⚡ Acciones Rápidas")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👥 Ver Usuarios", use_container_width=True):
        st.switch_page("admin/users.py")

with col2:
    if st.button("📋 Ver Todos los Gastos", use_container_width=True):
        st.switch_page("admin/expenses.py")

with col3:
    if st.button("📈 Ver Reportes", use_container_width=True):
        st.switch_page("admin/reports.py") 