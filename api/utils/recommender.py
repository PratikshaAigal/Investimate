import pandas as pd
import joblib
# def recommend_assets(user_risk_level: str, top_n: int = 5):
#     df = pd.read_csv('api/asset_risk_profiles.csv')
#
#     # Match Investimate's 'Moderate' with 'Medium'
#     risk_map = {'Low': 'Low', 'Moderate': 'Medium', 'High': 'High'}
#     mapped_risk = risk_map.get(user_risk_level, 'Medium')
#
#     filtered = df[df['Risk_Level'] == mapped_risk]
#     recommended = filtered.sort_values(by='Avg_Return', ascending=False).head(top_n)
#
#     # Add explanation
#     recommended['Explanation'] = (
#             "It has an average return of " + (recommended['Avg_Return'] * 100).round(2).astype(str) +
#             "% and volatility of " + recommended['Volatility'].round(4).astype(str) +
#             ", matching your " + user_risk_level + " risk profile."
#     )
#
#     return recommended[['Asset', 'Avg_Return', 'Volatility', 'Risk_Level', 'Explanation']].to_dict('records')


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
            f"It has an average return of {(row['Avg_Return'] * 100):.2f}% and volatility of "
            f"{row['Volatility']:.4f}, matching your {user_level} risk profile."
        ),
        axis=1
    )
    return recommended[['Asset', 'Avg_Return', 'Volatility', 'Predicted_Risk_Label', 'Explanation']].rename(
        columns={'Predicted_Risk_Label': 'Risk_Level'}
    ).to_dict('records')
