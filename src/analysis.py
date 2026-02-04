import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def aggregate_metrics(df):
    """
    Aggregates daily data to campaign level totals.
    """
    agg = df.groupby(['campaign_id', 'campaign_name']).agg({
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'conversion_value': 'sum'
    }).reset_index()
    
    # KPIs
    agg['ctr'] = agg['clicks'] / agg['impressions']
    agg['cpc'] = agg['spend'] / agg['clicks']
    agg['cpa'] = agg['spend'] / agg['conversions']
    agg['roas'] = agg['conversion_value'] / agg['spend']
    agg['conversion_rate'] = agg['conversions'] / agg['clicks']
    
    return agg.fillna(0)

def calculate_marginal_contribution(df):
    """
    Uses a simple Log-Linear regression to estimate marginal impact of spend on conversions.
    Conversions ~ Beta * ln(Spend)
    Marginal Change (Derivative) = Beta / Spend
    This helps identify where the 'next dollar' is most effective.
    """
    recommendations = []
    
    for campaign in df['campaign_id'].unique():
        subset = df[df['campaign_id'] == campaign].copy()
        
        # Avoid log(0)
        subset['log_spend'] = np.log1p(subset['spend'])
        
        X = subset[['log_spend']]
        y = subset['conversion_value'] # optimizing for Revenue/Value
        
        if len(subset) < 5:
            continue
            
        model = LinearRegression()
        model.fit(X, y)
        
        # Coefficient tells us: For a 1% increase in Spend, how much Value increases?
        # Beta approx change in Y for 1 unit change in log(X). 1 unit log(X) is approx 2.7x spend.
        # Direct derivative: dY/dSpend = Beta / (Spend + 1)
        
        beta = model.coef_[0]
        recent_spend = subset['spend'].mean() # Use average spend as baseline
        
        marginal_roas = beta / (recent_spend + 1)
        r_squared = model.score(X, y)
        
        recommendations.append({
            'campaign_id': campaign,
            'beta_coefficient': beta,
            'marginal_roas': marginal_roas,
            'model_confidence': r_squared
        })
        
    return pd.DataFrame(recommendations)

def generate_budget_recommendations(df, total_budget_shift_percentage=0.1):
    """
    Recommends shifting budget from Low Marginal ROAS to High Marginal ROAS campaigns.
    """
    metrics = aggregate_metrics(df)
    marginal = calculate_marginal_contribution(df)
    
    merged = pd.merge(metrics, marginal, on='campaign_id', how='left')
    
    # Sort by Marginal ROAS (Efficiency of next dollar)
    merged = merged.sort_values('marginal_roas', ascending=False)
    
    # Simple strategy: Take 10% from bottom half and give to top half
    n = len(merged)
    if n < 2:
        return merged
        
    top_half = merged.iloc[:n//2]
    bottom_half = merged.iloc[n//2:]
    
    # Calculate shift amounts
    recommendations = merged.copy()
    recommendations['recommended_action'] = 'Hold'
    recommendations['budget_modifier'] = 0.0
    
    # Identification
    high_performers = top_half['campaign_id'].tolist()
    low_performers = bottom_half['campaign_id'].tolist()
    
    recommendations.loc[recommendations['campaign_id'].isin(low_performers), 'recommended_action'] = 'Decrease Budget'
    recommendations.loc[recommendations['campaign_id'].isin(low_performers), 'budget_modifier'] = -total_budget_shift_percentage
    
    recommendations.loc[recommendations['campaign_id'].isin(high_performers), 'recommended_action'] = 'Increase Budget'
    recommendations.loc[recommendations['campaign_id'].isin(high_performers), 'budget_modifier'] = total_budget_shift_percentage

    return recommendations
