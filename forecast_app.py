import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Forecast Simulator",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'drivers' not in st.session_state:
    st.session_state.drivers = []

def calculate_forecast(baseline, drivers_data):
    """Calculate the adjusted forecast"""
    total_impact = 0
    driver_impacts = []
    
    for driver in drivers_data:
        impact = (driver['change'] / 100) * driver['elasticity']
        driver_impacts.append({
            'name': driver['name'],
            'change': driver['change'],
            'elasticity': driver['elasticity'],
            'impact': impact,
            'impact_percent': impact * 100,
            'impact_absolute': impact * baseline
        })
        total_impact += impact
    
    final_forecast = baseline * (1 + total_impact)
    absolute_change = final_forecast - baseline
    percent_change = (absolute_change / baseline) * 100
    
    return {
        'baseline': baseline,
        'total_impact': total_impact,
        'final_forecast': final_forecast,
        'absolute_change': absolute_change,
        'percent_change': percent_change,
        'driver_impacts': driver_impacts
    }

# Main app
st.title("🎯 Forecast Simulator")
st.markdown("Calculate adjusted forecasts based on driver changes and elasticities")

# Sidebar for inputs
st.sidebar.header("📊 Input Parameters")

# Baseline forecast
baseline_forecast = st.sidebar.number_input(
    "Baseline Forecast",
    value=1000000.0,
    step=10000.0,
    format="%.0f"
)

st.sidebar.subheader("Drivers")

# Add new driver
with st.sidebar.expander("➕ Add New Driver"):
    driver_name = st.text_input("Driver Name", key="new_driver_name")
    driver_change = st.number_input("Change (%)", value=0.0, step=0.1, key="new_driver_change")
    driver_elasticity = st.number_input("Elasticity", value=0.0, step=0.1, key="new_driver_elasticity")
    
    if st.button("Add Driver"):
        if driver_name:
            st.session_state.drivers.append({
                'name': driver_name,
                'change': driver_change,
                'elasticity': driver_elasticity
            })
            st.success(f"Added driver: {driver_name}")
            st.rerun()

# Display current drivers
if st.session_state.drivers:
    st.sidebar.subheader("Current Drivers")
    for i, driver in enumerate(st.session_state.drivers):
        with st.sidebar.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{driver['name']}**")
                st.write(f"Change: {driver['change']:+.1f}%")
                st.write(f"Elasticity: {driver['elasticity']:.2f}")
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.drivers.pop(i)
                    st.rerun()
            st.divider()

# Clear all drivers
if st.sidebar.button("🗑️ Clear All Drivers"):
    st.session_state.drivers = []
    st.rerun()

# Main content
if st.session_state.drivers:
    # Calculate results
    results = calculate_forecast(baseline_forecast, st.session_state.drivers)
    
    # Display results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Baseline Forecast",
            f"{results['baseline']:,.0f}"
        )
    
    with col2:
        st.metric(
            "Total Impact",
            f"{results['total_impact']*100:+.2f}%"
        )
    
    with col3:
        st.metric(
            "Final Forecast",
            f"{results['final_forecast']:,.0f}",
            f"{results['absolute_change']:+,.0f}"
        )
    
    with col4:
        st.metric(
            "Change",
            f"{results['percent_change']:+.2f}%"
        )
    
    # Detailed breakdown
    st.subheader("📋 Driver Impact Breakdown")
    
    # Create dataframe for display
    df_impacts = pd.DataFrame([
        {
            'Driver': impact['name'],
            'Change (%)': f"{impact['change']:+.1f}%",
            'Elasticity': impact['elasticity'],
            'Impact (%)': f"{impact['impact_percent']:+.2f}%",
            'Impact (Absolute)': f"{impact['impact_absolute']:+,.0f}"
        }
        for impact in results['driver_impacts']
    ])
    
    st.dataframe(df_impacts, use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Waterfall chart simulation
        fig = go.Figure()
        
        x_values = ['Baseline'] + [impact['name'] for impact in results['driver_impacts']] + ['Final']
        y_values = [results['baseline']] + [impact['impact_absolute'] for impact in results['driver_impacts']] + [results['final_forecast']]
        
        # Baseline bar
        fig.add_trace(go.Bar(
            x=['Baseline'],
            y=[results['baseline']],
            name='Baseline',
            marker_color='blue'
        ))
        
        # Driver impact bars
        colors = px.colors.qualitative.Set3
        for i, impact in enumerate(results['driver_impacts']):
            color = 'green' if impact['impact_absolute'] > 0 else 'red'
            fig.add_trace(go.Bar(
                x=[impact['name']],
                y=[impact['impact_absolute']],
                name=impact['name'],
                marker_color=color
            ))
        
        # Final bar
        fig.add_trace(go.Bar(
            x=['Final'],
            y=[results['final_forecast']],
            name='Final Forecast',
            marker_color='navy'
        ))
        
        fig.update_layout(
            title="Forecast Impact by Driver",
            xaxis_title="Components",
            yaxis_title="Value",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart of impacts
        impact_data = []
        impact_labels = []
        impact_values = []
        
        for impact in results['driver_impacts']:
            if abs(impact['impact_absolute']) > 0:
                impact_labels.append(f"{impact['name']}<br>({impact['impact_percent']:+.1f}%)")
                impact_values.append(abs(impact['impact_absolute']))
        
        if impact_values:
            fig_pie = go.Figure(data=[go.Pie(
                labels=impact_labels,
                values=impact_values,
                hole=0.3
            )])
            
            fig_pie.update_layout(
                title="Driver Impact Distribution (Absolute Values)"
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Export results
    st.subheader("📤 Export Results")
    
    # Prepare export data
    export_data = {
        'calculation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'baseline_forecast': results['baseline'],
        'final_forecast': results['final_forecast'],
        'total_impact_percent': results['percent_change'],
        'drivers': st.session_state.drivers,
        'driver_impacts': results['driver_impacts']
    }
    
    # Convert to CSV for download
    export_df = pd.DataFrame([
        {
            'Metric': 'Baseline Forecast',
            'Value': results['baseline']
        },
        {
            'Metric': 'Final Forecast',
            'Value': results['final_forecast']
        },
        {
            'Metric': 'Total Change (%)',
            'Value': results['percent_change']
        }
    ] + [
        {
            'Metric': f"{impact['name']} Impact",
            'Value': impact['impact_absolute']
        }
        for impact in results['driver_impacts']
    ])
    
    csv = export_df.to_csv(index=False)
    st.download_button(
        label="📁 Download Results (CSV)",
        data=csv,
        file_name=f"forecast_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.info("👈 Add drivers using the sidebar to start calculating forecasts")
    
    # Example section
    st.subheader("📖 Example Usage")
    st.markdown("""
    **Formula:** `Final Forecast = Baseline × (1 + Σ(Driver Change × Elasticity))`
    
    **Example:**
    - Baseline Forecast: 1,000,000
    - Price Increase: +5% with elasticity -0.8
    - Marketing Spend: +15% with elasticity 0.3
    - Economic Index: -2% with elasticity 0.5
    
    **Calculation:**
    - Price Impact: 5% × (-0.8) = -4.0% = -40,000
    - Marketing Impact: 15% × 0.3 = +4.5% = +45,000
    - Economic Impact: -2% × 0.5 = -1.0% = -10,000
    - **Final Forecast:** 1,000,000 × (1 + (-0.005)) = 995,000
    """)

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ How to Use")
st.sidebar.markdown("""
1. Set your baseline forecast
2. Add drivers with their:
   - Change percentage
   - Elasticity coefficient
3. View calculated results
4. Export data if needed
""")

st.sidebar.markdown("### 📚 Formula")
st.sidebar.code("Final = Baseline × (1 + Σ(Change × Elasticity))")