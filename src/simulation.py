import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def simulate_campaign_data(n_days=30, n_campaigns=5, seed=42):
    """
    Simulates ad campaign data with diminishing returns to allow for budget optimization validation.
    """
    np.random.seed(seed)
    
    campaign_types = ['Awareness', 'Retargeting', 'Prospecting', 'Competitor', 'Loyalty']
    channels = ['Facebook', 'Instagram', 'Audience Network']
    
    data = []
    
    start_date = datetime.now() - timedelta(days=n_days)
    
    campaign_configs = []
    for i in range(n_campaigns):
        c_type = np.random.choice(campaign_types)
        c_channel = np.random.choice(channels)
        # Each campaign has different efficiency (alpha) and cost-per-impression dynamics
        efficiency = np.random.uniform(0.5, 2.0) 
        saturation_point = np.random.uniform(1000, 5000)
        campaign_configs.append({
            'campaign_id': f"CMP_{i+1:03d}",
            'campaign_name': f"{c_type} - {c_channel} - {i+1}",
            'efficiency': efficiency,
            'saturation': saturation_point
        })

    for day in range(n_days):
        current_date = start_date + timedelta(days=day)
        
        for config in campaign_configs:
            # Random daily budget fluctuation
            spend = np.random.uniform(100, 1000)
            
            # Impressions correlate with Spend usually linearly but with CPM noise
            cpm = np.random.uniform(5, 15) # Cost per mille
            impressions = (spend / cpm) * 1000
            
            # CTR varies by campaign efficiency
            ctr = np.random.uniform(0.005, 0.02) * config['efficiency']
            clicks = impressions * ctr
            
            # Conversions follow a dimishing return curve based on spend/saturation
            # Model: Beta * log(Spend) * Efficiency
            # Ideally conversion rate drops as volume increases (saturation)
            
            base_conv_rate = np.random.uniform(0.02, 0.10)
            
            # Simple saturation: conversions grow with spend but sub-linearly
            # Conversions = K * (Spend ** 0.8) for example
            conversions = (clicks * base_conv_rate) * (1 / (1 + (spend/config['saturation'])))
            conversions = max(0, int(conversions))
            
            # Conversion Value
            aov = np.random.normal(50, 10) # Average Order Value
            conversion_value = conversions * aov
            
            data.append({
                'date': current_date.date(),
                'campaign_id': config['campaign_id'],
                'campaign_name': config['campaign_name'],
                'spend': round(spend, 2),
                'impressions': int(impressions),
                'clicks': int(clicks),
                'conversions': int(conversions),
                'conversion_value': round(conversion_value, 2)
            })
            
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = simulate_campaign_data()
    print(df.head())
    df.to_csv('data/marketing_data.csv', index=False)
