import pandas as pd

def recommend_assets(user_risk_level: str, top_n: int = 5):
    df = pd.read_csv('api/asset_risk_profiles.csv')

    # Match Investimate's 'Moderate' with 'Medium'
    risk_map = {'Low': 'Low', 'Moderate': 'Medium', 'High': 'High'}
    mapped_risk = risk_map.get(user_risk_level, 'Medium')

    filtered = df[df['Risk_Level'] == mapped_risk]
    recommended = filtered.sort_values(by='Avg_Return', ascending=False).head(top_n)

    # Add explanation
    recommended['Explanation'] = (
            "It has an average return of " + (recommended['Avg_Return'] * 100).round(2).astype(str) +
            "% and volatility of " + recommended['Volatility'].round(4).astype(str) +
            ", matching your " + user_risk_level + " risk profile."
    )

    return recommended[['Asset', 'Avg_Return', 'Volatility', 'Risk_Level', 'Explanation']].to_dict('records')
