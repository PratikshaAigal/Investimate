
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

# # From GitHub (public CSV)
url = 'US_Stock_Data.csv'
df = pd.read_csv(url)


# 1. Clean numeric columns
for col in df.columns:
    if '_Price' in col or '_Vol.' in col:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '', regex=False), errors='coerce')

df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y', errors='coerce')
df = df.sort_values('Date')
df.dropna(how='all', subset=[col for col in df.columns if '_Price' in col], inplace=True)

# 2. Feature Engineering: Per Asset
assets = ['Natural_Gas', 'Crude_oil', 'Copper', 'Bitcoin', 'Platinum', 'Ethereum',
          'Apple', 'Tesla', 'Microsoft', 'Silver', 'Google', 'Nvidia', 'Berkshire',
          'Netflix', 'Amazon', 'Meta', 'Gold']

# ----------------------------------------
# 1. 📉 Market Risk (based on index volatility)
# ----------------------------------------
df['S&P_Return'] = df['S&P_500_Price'].pct_change()
df['Nasdaq_Return'] = df['Nasdaq_100_Price'].pct_change()
df['Market_Risk'] = df[['S&P_Return', 'Nasdaq_Return']].rolling(30, min_periods=1).std().mean(axis=1)
#
#
# # ----------------------------------------
# # 2. 🧱 Company-Specific Risk (per stock volatility)
# # ----------------------------------------
# companies=['Natural_Gas_Price', 'Crude_oil_Price', 'Copper_Price', 'Bitcoin_Price', 'Platinum_Price',
#            'Ethereum_Price', 'Apple_Price', 'Tesla_Price', 'Microsoft_Price', 'Silver_Price', 'Google_Price',
#            'Nvidia_Price', 'Berkshire_Price', 'Netflix_Price', 'Amazon_Price', 'Meta_Price', 'Gold_Price']
#
# # Loop through each asset and calculate volatility + flag
# for company in companies:
#     base_name = company.replace('_Price', '')  # e.g., "Apple"
#
#     # Step 1: Calculate returns
#     df[f'{base_name}_Return'] = df[company].pct_change()
#
#     # Step 2: Calculate 30-day rolling volatility
#     df[f'{base_name}_Volatility'] = df[f'{base_name}_Return'].rolling(window=30).std()
#
#     df['Return']=df[f'{base_name}_Return']
#     df['Volatility']=df[f'{base_name}_Volatility']
#     # Step 3: Get thresholds from percentiles
#     vol_clean = df[f'{base_name}_Volatility'].dropna()
#     low_thresh = vol_clean.quantile(0.33)
#     med_thresh = vol_clean.quantile(0.66)
#
#     # Step 4: Flag the risk level
#     def flag_risk(vol):
#         if pd.isna(vol):
#             return None
#         elif vol < low_thresh:
#             return 'Low'
#         elif vol < med_thresh:
#             return 'Medium'
#         else:
#             return 'High'
#
#     df[f'{base_name}_Risk_Level'] = df[f'{base_name}_Volatility'].apply(flag_risk)
#
# # Final columns to export
# result_cols = []
# for company in companies:
#     base_name = company.replace('_Price', '')
#     result_cols.extend([f'{base_name}_Volatility', f'{base_name}_Risk_Level'])
#
# # Drop rows with missing values
# df[result_cols] = df[result_cols].replace(['None', 'nan', 'NaN'], pd.NA)
# df_result = df[result_cols].dropna()
# # print(df_result)
#
#
# # ----------------------------------------
# # 3. 💸 Liquidity Risk (low average trading volume)
# # ----------------------------------------
#
# columns_list = ['Natural_Gas_Vol.', 'Crude_oil_Vol.', 'Copper_Vol.', 'Bitcoin_Vol.', 'Platinum_Vol.',
#                 'Ethereum_Vol.', 'Nasdaq_100_Vol.', 'Apple_Vol.', 'Tesla_Vol.', 'Microsoft_Vol.',
#                  'Silver_Vol.', 'Google_Vol.', 'Nvidia_Vol.', 'Berkshire_Vol.', 'Netflix_Vol.',
#                   'Amazon_Vol.', 'Meta_Vol.', 'Gold_Vol.' ]
# df['Avg_Liquidity'] = df[columns_list].rolling(window=30).mean().mean(axis=1)
#
# df= df.replace(['None', 'nan', 'NaN'], pd.NA)
# df= df.dropna()
# # print(df)
#
#
#
#
# # ----------------------------------------
# # 4. 🔁 Volatility Risk (total return volatility across all assets)
# # ----------------------------------------
# df['Volatility_Risk'] = df[[f'{base_name}_Return' for a in df]].rolling(window=30).std().mean(axis=1)
# # df= df.replace(['None', 'nan', 'NaN'], pd.NA)
# # df= df.dropna()
# # print(df)
#
#
# # ----------------------------------------
# # 5. ⏰ Timing Risk (drawdowns — peak-to-trough drop)
# # ----------------------------------------

def calculate_drawdown(series):
    peak = series.expanding(min_periods=1).max()
    drawdown = (series - peak) / peak
    return drawdown

df['Timing_Risk'] = calculate_drawdown(df['S&P_500_Price'])

df= df.replace(['None', 'nan', 'NaN'], pd.NA)
df= df.dropna()
# print(df)
# 3. Per-Asset Feature Computation
assets = ['Natural_Gas', 'Crude_oil', 'Copper', 'Bitcoin', 'Platinum', 'Ethereum',
          'Apple', 'Tesla', 'Microsoft', 'Silver', 'Google', 'Nvidia', 'Berkshire',
          'Netflix', 'Amazon', 'Meta', 'Gold']

asset_data = []

for asset in assets:
    price_col = f'{asset}_Price'
    vol_col = f'{asset}_Vol.'

    if price_col not in df.columns or vol_col not in df.columns:
        continue

    temp = pd.DataFrame({
        'Price': df[price_col],
        'Volume': df[vol_col],
        'Market_Risk': df['Market_Risk'],
        'Timing_Risk': df['Timing_Risk']
    }).dropna()

    temp['Return'] = temp['Price'].pct_change()
    temp['Volatility'] = temp['Return'].rolling(30).std()

    temp['Liquidity'] = temp['Volume'].pct_change()
    temp['Liquidity'] = temp['Volume'].rolling(30).mean()

    avg_return = temp['Return'].mean()
    avg_volatility = temp['Volatility'].mean()
    avg_liquidity = temp['Liquidity'].mean()
    avg_market_risk = temp['Market_Risk'].mean()
    avg_timing_risk = temp['Timing_Risk'].mean()

    composite_score = np.mean([
        avg_market_risk,
        avg_volatility,
        1 / (avg_liquidity + 1e-9),
        abs(avg_return),
        abs(avg_timing_risk)
    ])

    if np.isnan(composite_score):
        continue

    asset_data.append({
        'Asset': asset,
        'Avg_Return': avg_return,
        'Volatility': avg_volatility,
        'Liquidity': avg_liquidity,
        'Market_Risk': avg_market_risk,
        'Timing_Risk': avg_timing_risk,
        'Composite_Risk_Score': composite_score,
    })

# 4. Create final asset DataFrame
asset_df = pd.DataFrame(asset_data).dropna()

# 5. Dynamic quantile-based risk classification
low_q = asset_df['Composite_Risk_Score'].quantile(0.33)
med_q = asset_df['Composite_Risk_Score'].quantile(0.66)

def classify_risk(score):
    if score < low_q:
        return 'Low'
    elif score < med_q:
        return 'Medium'
    else:
        return 'High'

asset_df['Risk_Level'] = asset_df['Composite_Risk_Score'].apply(classify_risk)

asset_df.to_csv("asset_features.csv", index=False)
print("✅ Saved asset_features.csv")

# 5. Train ML Model
X = asset_df[[ 'Volatility', 'Liquidity', 'Market_Risk', 'Timing_Risk, 'Avg_Return' ]]
y = asset_df['Risk_Level']

X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.8, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

print("✅ Accuracy:", model.score(X_test, y_test))
joblib.dump(model, "risk_model.pkl")
print("✅ Model saved as 'risk_model.pkl'")

