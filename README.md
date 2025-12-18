# Forecast Simulator 🎯

A web-based forecasting tool that calculates adjusted forecasts based on driver changes and elasticities.

## Formula
```
Final Forecast = Baseline × (1 + Σ(Driver Change × Elasticity))
```

## Features
- Interactive dashboard with real-time calculations
- Visual charts (waterfall chart, pie chart)
- Metric cards showing key results
- Data export to CSV
- Easy driver management (add/remove)

## Quick Start
1. Set your baseline forecast
2. Add drivers with change percentages and elasticities
3. View calculated results and visualizations
4. Export data if needed

## Local Installation
```bash
pip install -r requirements.txt
streamlit run forecast_app.py
```

## Live Demo
🔗 [Access the app here](your-deployment-url-here)

## Example Usage
- **Baseline**: 1,000,000
- **Price increase**: +5% (elasticity: -0.8) = -40,000 impact
- **Marketing spend**: +15% (elasticity: 0.3) = +45,000 impact
- **Economic decline**: -2% (elasticity: 0.5) = -10,000 impact
- **Result**: 995,000 (-0.5% change)

## Technology Stack
- Streamlit
- Pandas
- Plotly
- Python 3.7+