import pandas as pd
import joblib
def recommend_assets(user_risk_level: str, top_n: int = 5):


    df = pd.read_csv('asset_features.csv')
    model = joblib.load('risk_model.pkl')

    # Predict using model (raw values, no scaling)
    X = df[['Avg_Return', 'Volatility', 'Liquidity', 'Market_Risk', 'Timing_Risk']]
    df['Predicted_Risk_Label'] = model.predict(X)

    # Match risk label
    risk_map = {'Low': 'Low', 'Moderate': 'Medium', 'High': 'High'}
    user_level = risk_map.get(user_risk_level, 'Medium')

    filtered = df[df['Predicted_Risk_Label'] == user_level]
    recommended = filtered.sort_values(by='Avg_Return', ascending=False).head(top_n)

    # Add explanation column row-wise
    recommended['Explanation'] = recommended.apply(
        lambda row: (
            f"It offers an average return of {(row['Avg_Return'] * 100):.2f}% with a volatility of {row['Volatility']:.4f}. "
            f"Liquidity is {row['Liquidity']}, Market Risk is {row['Market_Risk']}, and Timing Risk is {row['Timing_Risk']}, "
            f"aligning with your {user_level} risk preference."
        ),
        axis=1
    )

    for col in ['Liquidity', 'Market_Risk', 'Timing_Risk']:
        recommended[col] = recommended[col].apply(format_large_number)
    return recommended[['Asset',
        'Avg_Return',
        'Volatility',
        'Liquidity',
        'Market_Risk',
        'Timing_Risk',
        'Predicted_Risk_Label',
        'Explanation']].rename(
        columns={'Predicted_Risk_Label': 'Risk_Level'}
    ).to_dict('records')


def format_large_number(value):
    abs_val = abs(value)
    if abs_val >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif abs_val >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif abs_val >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return f"{value:.2f}"
