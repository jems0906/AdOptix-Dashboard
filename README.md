# AdOptix Dashboard 📊

An intelligent ad campaign budget optimization system that uses machine learning to recommend budget shifts for maximum ROI. Built to demonstrate data modeling, analytics, and visualization skills relevant to Meta's advertising business.

## 🎯 Overview

AdOptix simulates realistic ad campaign performance across multiple channels (Facebook, Instagram, Audience Network) and uses regression-based analytics to identify where marketing budgets should be allocated for optimal returns.

### Key Features

- **Campaign Simulation**: Generates realistic ad data with diminishing returns modeling
- **ML-Driven Recommendations**: Log-linear regression to calculate Marginal ROAS
- **Interactive Dashboard**: Real-time visualizations using Streamlit and Plotly
- **Budget Optimization**: Data-driven recommendations for budget reallocation
- **Full Funnel Modeling**: Impressions → Clicks → Conversions → Revenue

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone or navigate to the project directory:
```bash
cd "C:\project\AdOptix Dashboard"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
python -m streamlit run src/app.py
```

The dashboard will open at `http://localhost:8501`

## 📁 Project Structure

```
AdOptix Dashboard/
├── src/
│   ├── simulation.py     # Campaign data generator
│   ├── analysis.py       # ML models and analytics
│   └── app.py           # Streamlit dashboard
├── data/
│   └── marketing_data.csv  # Generated campaign data
├── requirements.txt      # Python dependencies
└── README.md
```

## 🧠 How It Works

### 1. Data Simulation (`simulation.py`)

Generates realistic campaign data with:
- **Diminishing Returns**: Conversions follow saturation curves (spend efficiency decreases at high budgets)
- **Campaign Types**: Awareness, Retargeting, Prospecting, Competitor, Loyalty
- **Channels**: Facebook, Instagram, Audience Network
- **Metrics**: Spend, Impressions, Clicks, Conversions, Revenue

### 2. Analytics & ML (`analysis.py`)

**Data Modeling:**
- Aggregates daily data to campaign-level totals
- Calculates KPIs: CTR, CPC, CPA, ROAS, Conversion Rate

**Machine Learning:**
- Fits log-linear regression: `Revenue ~ β * ln(Spend)`
- Calculates **Marginal ROAS**: The expected revenue from the next dollar spent
- Formula: `dRevenue/dSpend = β / Spend`

**Recommendation Logic:**
- Ranks campaigns by Marginal ROAS (efficiency of next dollar)
- Recommends shifting budget FROM low-marginal campaigns TO high-marginal campaigns

### 3. Visualization (`app.py`)

**Interactive Dashboard Features:**
- Global KPIs (Total Spend, Revenue, ROAS, Conversions)
- Campaign performance table with formatting
- Time series chart showing daily revenue trends
- Spend efficiency scatter plot (bubble size = ROAS)
- Marginal ROAS bar chart with color-coded recommendations
- Configurable budget shift aggressiveness slider

## 📊 Key Metrics Explained

| Metric | Definition | Business Value |
|--------|------------|----------------|
| **CTR** | Click-Through Rate | Measures ad relevance/engagement |
| **CPC** | Cost Per Click | Auction efficiency |
| **CPA** | Cost Per Acquisition | Customer acquisition cost |
| **ROAS** | Return on Ad Spend | Revenue generated per dollar spent |
| **Marginal ROAS** | Next dollar efficiency | Where to allocate incremental budget |

## 🎓 Technical Highlights

### Data Modeling
- Pandas DataFrame aggregations with groupby operations
- Multi-level joins between metrics and ML outputs
- Proper handling of edge cases (division by zero, log of zero)

### Machine Learning
- Scikit-learn LinearRegression for predictive modeling
- Log transformation for diminishing returns modeling
- Model confidence scoring (R²)
- Marginal analysis via calculus (derivative of fitted function)

### Visualization
- Plotly for interactive charts with hover data
- Color-coded recommendations (green/red/grey)
- Responsive layout with Streamlit columns
- Dynamic data regeneration for testing scenarios

## 🔧 Customization

### Adjust Simulation Parameters

Edit `src/simulation.py`:
```python
df = simulate_campaign_data(
    n_days=45,      # Number of days to simulate
    n_campaigns=8,  # Number of campaigns
    seed=42         # Random seed for reproducibility
)
```

### Modify Budget Shift Strategy

Edit `src/analysis.py`:
```python
def generate_budget_recommendations(df, total_budget_shift_percentage=0.1):
    # Adjust the shift percentage or ranking logic
```

## 📈 Sample Insights

The dashboard might show:
- "Retargeting - Instagram" has a Marginal ROAS of 2.5x → **Increase Budget**
- "Awareness - Facebook" has a Marginal ROAS of 0.3x → **Decrease Budget**
- Shifting 10% budget could increase total revenue by 15-20%

## 🎯 Meta Ads Business Relevance

This project demonstrates:
1. **Campaign Management**: Multi-channel, multi-objective optimization
2. **Attribution Modeling**: Full funnel tracking from impression to conversion
3. **Budget Pacing**: Understanding diminishing returns and saturation
4. **Data-Driven Decisions**: ML recommendations vs. intuition
5. **ROI Analysis**: Clear visualization of lift and efficiency gains

## 🛠️ Dependencies

- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `plotly`: Interactive visualizations
- `streamlit`: Web dashboard framework
- `scikit-learn`: Machine learning models

## 📝 Future Enhancements

Potential additions:
- [ ] A/B test simulation and statistical significance testing
- [ ] Multi-touch attribution modeling
- [ ] Time series forecasting (ARIMA/Prophet)
- [ ] Constraint-based optimization (budget caps, minimum spend)
- [ ] Export recommendations to CSV/Excel
- [ ] Integration with real ad platform APIs

## 📄 License

This project is for educational and demonstration purposes.

---

**Built with ❤️ for data-driven marketing optimization**
