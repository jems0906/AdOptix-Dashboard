import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from simulation import simulate_campaign_data
from analysis import aggregate_metrics, generate_budget_recommendations

st.set_page_config(page_title="AdOptix Dashboard", layout="wide")

st.title("AdOptix: Intelligent Budget Optimization")
st.markdown("""
This dashboard simulates ad campaign performance and uses a regression-based model to estimate 
**Marginal ROAS** (Return on Ad Spend). It recommends budget shifts to maximize total return.
""")

# --- Data Loading ---
@st.cache_data
def load_data():
    return simulate_campaign_data(n_days=45, n_campaigns=8)

if st.button("Regenerate Simulation Data"):
    st.cache_data.clear()

df = load_data()

# --- Sidebar Controls ---
st.sidebar.header("Configuration")
budget_shift_pct = st.sidebar.slider("Aggressiveness of Shift (%)", 5, 30, 10) / 100

# --- High Level KPIs ---
metrics = aggregate_metrics(df)
total_spend = metrics['spend'].sum()
total_conv_value = metrics['conversion_value'].sum()
global_roas = total_conv_value / total_spend
total_conversions = metrics['conversions'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spend", f"${total_spend:,.2f}")
col2.metric("Total Revenue", f"${total_conv_value:,.2f}")
col3.metric("Global ROAS", f"{global_roas:.2f}x")
col4.metric("Conversions", f"{total_conversions:,}")

# --- Campaign Performance Overview ---
st.subheader("Campaign Performance Overview")
st.dataframe(metrics.style.format({
    'spend': '${:,.2f}',
    'conversion_value': '${:,.2f}',
    'roas': '{:.2f}x',
    'ctr': '{:.2%}',
    'cpa': '${:,.2f}'
}))

# --- Visualizations ---
st.subheader("Deep Dive Analytics")
tab1, tab2 = st.tabs(["Time Series", "Spend vs Return"])

with tab1:
    fig_time = px.line(df, x='date', y='conversion_value', color='campaign_name', title='Daily Revenue by Campaign')
    st.plotly_chart(fig_time, width='stretch')

with tab2:
    fig_scatter = px.scatter(metrics, x='spend', y='conversion_value', 
                             size='roas', color='campaign_name',
                             hover_data=['roas', 'cpa'],
                             title='Spend Efficiency (Size = ROAS)')
    st.plotly_chart(fig_scatter, width='stretch')

# --- ML Recommendations ---
st.divider()
st.subheader("💰 AI Budget Recommendations")
st.markdown("The system analyzes the *marginal* return of each campaign. Campaigns where the next dollar spent yields high returns are recommended for budget increases.")

recs = generate_budget_recommendations(df, total_budget_shift_percentage=budget_shift_pct)

# Visualization of recommendations
fig_recs = go.Figure()

for action, color in [('Increase Budget', 'green'), ('Decrease Budget', 'red'), ('Hold', 'grey')]:
    subset = recs[recs['recommended_action'] == action]
    if not subset.empty:
        fig_recs.add_trace(go.Bar(
            x=subset['campaign_name'],
            y=subset['marginal_roas'],
            name=action,
            marker_color=color
        ))

fig_recs.update_layout(title="Marginal ROAS by Campaign (Higher is Better)", yaxis_title="Marginal Revenue per $1 Spend", xaxis_title="Campaign")
st.plotly_chart(fig_recs, width='stretch')

st.write("Detailed Recommendations:")
st.dataframe(recs[['campaign_name', 'marginal_roas', 'model_confidence', 'recommended_action', 'budget_modifier']].sort_values('marginal_roas', ascending=False).style.format({
    'marginal_roas': '{:.2f}',
    'model_confidence': '{:.2f}',
    'budget_modifier': '{:.0%}'
}))
