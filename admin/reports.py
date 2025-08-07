import streamlit as st
from functions.f_read import get_expense_statistics, get_all_expenses, get_expenses_by_status
from functions.f_read import get_expenses_by_date_range, get_users_by_role
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

st.title("📈 Reportes y Analytics")

# Get statistics
stats = get_expense_statistics()

# Date range selector
col1, col2 = st.columns(2)
with col1:
    report_period = st.selectbox(
        "📅 Período del reporte",
        ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días", "Este año", "Personalizado"]
    )

with col2:
    if report_period == "Personalizado":
        custom_dates = st.date_input(
            "📅 Seleccionar fechas",
            value=(datetime.now() - timedelta(days=30), datetime.now())
        )

# Calculate date range
if report_period == "Últimos 7 días":
    start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.now()
elif report_period == "Últimos 30 días":
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
elif report_period == "Últimos 90 días":
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()
elif report_period == "Este año":
    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()
else:  # Personalizado
    if len(custom_dates) == 2:
        start_date = custom_dates[0]
        end_date = custom_dates[1]
    else:
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()

# Get expenses for the period
period_expenses = get_expenses_by_date_range(
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)

# Summary metrics
st.subheader("📊 Métricas Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_amount = sum(e['amount'] for e in period_expenses)
    st.metric(
        label="💰 Total Gastos",
        value=f"${total_amount:,.2f}",
        delta=None
    )

with col2:
    avg_amount = total_amount / len(period_expenses) if period_expenses else 0
    st.metric(
        label="📊 Promedio",
        value=f"${avg_amount:,.2f}",
        delta=None
    )

with col3:
    st.metric(
        label="📋 Cantidad",
        value=len(period_expenses),
        delta=None
    )

with col4:
    pending_count = len([e for e in period_expenses if e['status'] == 'pending'])
    st.metric(
        label="⏳ Pendientes",
        value=pending_count,
        delta=None
    )

# Charts
st.markdown("---")
st.subheader("📈 Gráficos")

# Status distribution
if period_expenses:
    status_counts = {}
    for expense in period_expenses:
        status = expense['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    if status_counts:
        fig_pie = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Distribución por Estado"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# Monthly trend
if period_expenses:
    # Group by month
    monthly_data = {}
    for expense in period_expenses:
        month = expense['created_at'][:7]  # YYYY-MM
        if month not in monthly_data:
            monthly_data[month] = {'amount': 0, 'count': 0}
        monthly_data[month]['amount'] += expense['amount']
        monthly_data[month]['count'] += 1
    
    if monthly_data:
        months = sorted(monthly_data.keys())
        amounts = [monthly_data[m]['amount'] for m in months]
        counts = [monthly_data[m]['count'] for m in months]
        
        # Amount trend
        fig_amount = px.line(
            x=months,
            y=amounts,
            title="Tendencia de Montos por Mes",
            labels={'x': 'Mes', 'y': 'Monto ($)'}
        )
        st.plotly_chart(fig_amount, use_container_width=True)
        
        # Count trend
        fig_count = px.bar(
            x=months,
            y=counts,
            title="Cantidad de Gastos por Mes",
            labels={'x': 'Mes', 'y': 'Cantidad'}
        )
        st.plotly_chart(fig_count, use_container_width=True)

# Category analysis
if period_expenses:
    category_data = {}
    for expense in period_expenses:
        category = expense.get('category', 'Sin categoría')
        if category not in category_data:
            category_data[category] = {'amount': 0, 'count': 0}
        category_data[category]['amount'] += expense['amount']
        category_data[category]['count'] += 1
    
    if category_data:
        categories = list(category_data.keys())
        amounts = [category_data[c]['amount'] for c in categories]
        counts = [category_data[c]['count'] for c in categories]
        
        # Category amount chart
        fig_category_amount = px.bar(
            x=categories,
            y=amounts,
            title="Monto por Categoría",
            labels={'x': 'Categoría', 'y': 'Monto ($)'}
        )
        st.plotly_chart(fig_category_amount, use_container_width=True)

# User analysis
st.markdown("---")
st.subheader("👥 Análisis por Usuario")

# Get all users with expenses
user_expenses = {}
for expense in period_expenses:
    user_id = expense['user_id']
    if user_id not in user_expenses:
        user_expenses[user_id] = {'amount': 0, 'count': 0}
    user_expenses[user_id]['amount'] += expense['amount']
    user_expenses[user_id]['count'] += 1

if user_expenses:
    # Create user summary table
    user_summary = []
    for user_id, data in user_expenses.items():
        # Get user name (you'll need to implement this)
        user_name = f"Usuario {user_id}"  # Placeholder
        user_summary.append({
            'Usuario': user_name,
            'Total Gastos': data['count'],
            'Monto Total': f"${data['amount']:,.2f}",
            'Promedio': f"${data['amount']/data['count']:,.2f}" if data['count'] > 0 else "$0.00"
        })
    
    df = pd.DataFrame(user_summary)
    st.dataframe(df, use_container_width=True)

# Export functionality
st.markdown("---")
st.subheader("📤 Exportar Datos")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Exportar Reporte PDF"):
        st.info("📄 Funcionalidad de exportación PDF en desarrollo...")

with col2:
    if st.button("📋 Exportar a Excel"):
        if period_expenses:
            # Convert to DataFrame
            df_export = pd.DataFrame(period_expenses)
            st.download_button(
                label="💾 Descargar Excel",
                data=df_export.to_csv(index=False),
                file_name=f"reporte_gastos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("📝 No hay datos para exportar.") 