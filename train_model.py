
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from sklearn.metrics import accuracy_score

# # From GitHub (public CSV)
url = 'https://raw.githubusercontent.com/PratikshaAigal/Investimate/main/US_Stock_Data.csv'
df = pd.read_csv(url)

# # Basic cleaning
df.dropna(inplace=True)


df['S&P_500_Price'] = df['S&P_500_Price'].str.replace(',', '', regex=False).astype(float)
df['Nasdaq_100_Price'] = df['Nasdaq_100_Price'].str.replace(',', '', regex=False).astype(float)
df['Bitcoin_Price'] = df['Bitcoin_Price'].str.replace(',', '', regex=False).astype(float)
df['Platinum_Price'] = df['Platinum_Price'].str.replace(',', '', regex=False).astype(float)
df['Ethereum_Price'] = df['Ethereum_Price'].str.replace(',', '', regex=False).astype(float)
df['Berkshire_Price'] = df['Berkshire_Price'].str.replace(',', '', regex=False).astype(float)
df['Gold_Price'] = df['Gold_Price'].str.replace(',', '', regex=False).astype(float)
# print(df.dtypes)

# ----------------------------------------
# 1. 📉 Market Risk (based on index volatility)
# ----------------------------------------
df['S&P_Return'] = df['S&P_500_Price'].pct_change()
df['Nasdaq_Return'] = df['Nasdaq_100_Price'].pct_change()
df['Market_Risk'] = df[['S&P_Return', 'Nasdaq_Return']].rolling(30, min_periods=1).std().mean(axis=1)
df.dropna(inplace=True)
# print(df)

# ----------------------------------------
# 2. 🧱 Company-Specific Risk (per stock volatility)
# ----------------------------------------
companies=['Natural_Gas_Price', 'Crude_oil_Price', 'Copper_Price', 'Bitcoin_Price', 'Platinum_Price',
           'Ethereum_Price', 'Apple_Price', 'Tesla_Price', 'Microsoft_Price', 'Silver_Price', 'Google_Price',
           'Nvidia_Price', 'Berkshire_Price', 'Netflix_Price', 'Amazon_Price', 'Meta_Price', 'Gold_Price']

# Loop through each asset and calculate volatility + flag
for company in companies:
    base_name = company.replace('_Price', '')  # e.g., "Apple"

    # Step 1: Calculate returns
    df[f'{base_name}_Return'] = df[company].pct_change()

    # Step 2: Calculate 30-day rolling volatility
    df[f'{base_name}_Volatility'] = df[f'{base_name}_Return'].rolling(window=30).std()

    df['Return']=df[f'{base_name}_Return']
    df['Volatility']=df[f'{base_name}_Volatility']
    # Step 3: Get thresholds from percentiles
    vol_clean = df[f'{base_name}_Volatility'].dropna()
    low_thresh = vol_clean.quantile(0.33)
    med_thresh = vol_clean.quantile(0.66)

    # Step 4: Flag the risk level
    def flag_risk(vol):
        if pd.isna(vol):
            return None
        elif vol < low_thresh:
            return 'Low'
        elif vol < med_thresh:
            return 'Medium'
        else:
            return 'High'

    df[f'{base_name}_Risk_Level'] = df[f'{base_name}_Volatility'].apply(flag_risk)

# Final columns to export
result_cols = []
for company in companies:
    base_name = company.replace('_Price', '')
    result_cols.extend([f'{base_name}_Volatility', f'{base_name}_Risk_Level'])

# Drop rows with missing values
df[result_cols] = df[result_cols].replace(['None', 'nan', 'NaN'], pd.NA)
df_result = df[result_cols].dropna()
# print(df_result)


# ----------------------------------------
# 3. 💸 Liquidity Risk (low average trading volume)
# ----------------------------------------

columns_list = ['Natural_Gas_Vol.', 'Crude_oil_Vol.', 'Copper_Vol.', 'Bitcoin_Vol.', 'Platinum_Vol.',
                'Ethereum_Vol.', 'Nasdaq_100_Vol.', 'Apple_Vol.', 'Tesla_Vol.', 'Microsoft_Vol.',
                 'Silver_Vol.', 'Google_Vol.', 'Nvidia_Vol.', 'Berkshire_Vol.', 'Netflix_Vol.',
                  'Amazon_Vol.', 'Meta_Vol.', 'Gold_Vol.' ]
df['Avg_Liquidity'] = df[columns_list].rolling(window=30).mean().mean(axis=1)

df= df.replace(['None', 'nan', 'NaN'], pd.NA)
df= df.dropna()
# print(df)




# ----------------------------------------
# 4. 🔁 Volatility Risk (total return volatility across all assets)
# ----------------------------------------
df['Volatility_Risk'] = df[[f'{base_name}_Return' for a in df]].rolling(window=30).std().mean(axis=1)
# df= df.replace(['None', 'nan', 'NaN'], pd.NA)
# df= df.dropna()
# print(df)


# ----------------------------------------
# 5. ⏰ Timing Risk (drawdowns — peak-to-trough drop)
# ----------------------------------------
def calculate_drawdown(series):
    peak = series.expanding(min_periods=1).max()
    drawdown = (series - peak) / peak
    return drawdown

df['Timing_Risk'] = calculate_drawdown(df['S&P_500_Price'])

df= df.replace(['None', 'nan', 'NaN'], pd.NA)
df= df.dropna()
# print(df)


from sklearn.preprocessing import MinMaxScaler
asset = ['Natural_Gas', 'Crude_oil', 'Copper', 'Bitcoin', 'Platinum', 'Ethereum',
          'Apple', 'Tesla', 'Microsoft', 'Silver', 'Google', 'Nvidia', 'Berkshire',
          'Netflix', 'Amazon', 'Meta', 'Gold']

asset_data = []
# Step 1: Normalize the risk features
risk_features = ['Market_Risk', 'Avg_Liquidity', 'Volatility_Risk', 'Timing_Risk','Return','Volatility']
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df[risk_features]), columns=risk_features)
# print(df_scaled.head())

# Step 2: Combine into a single composite risk score (e.g., average)
df['Composite_Risk_Score'] = df_scaled.mean(axis=1)

# Step 3: Define thresholds for classification
def classify_risk(score):
    if score < 0.33:
        return 'Low'
    elif score < 0.66:
        return 'Medium'
    else:
        return 'High'


asset_data.append({
        'Asset': asset,
        'Overall_Market_Risk': df['Market_Risk'],
        'Avg_Return_company_specific': df_result,
        'Volatility': df['Volatility_Risk'],
        'Liquidity': df['Avg_Liquidity'],
        'Timing_Risk': df['Timing_Risk'],
        'Combined_Risk_Score': df['Composite_Risk_Score']
    })

asset_df = pd.DataFrame(asset_data).dropna()

df['Overall_Risk_Level'] = df['Composite_Risk_Score'].apply(classify_risk)
# asset_df['Risk_Level'] = asset_df['Normalized_Risk_Score'].apply(classify_risk)
 
asset_df.to_csv('asset_features.csv', index=False)
print("asset feature saved")




# Optional: Encode it for model training
risk_label_map = {'Low': 0, 'Medium': 1, 'High': 2}
df['Risk_Label'] = df['Overall_Risk_Level'].map(risk_label_map)



# Drop NaNs just in case
df.dropna(subset=['Risk_Label'], inplace=True)

# print(df)


#Model Training

# Example columns
features = [col for col in df if col.endswith('_Price') or col.endswith('_Vol.')]
target = ['Risk_Label']
# df[target] = df[target].apply(pd.to_numeric, errors='coerce')


# # print(df[features].head()) 

# # Train/test split
X = df[features]
print("Feature Data (X):")
print(X.head())
y = df[target]
print("Target Data (y):")
print(y.head())


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42)
print(X_train.shape, y_train.shape)

# # Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Accuracy
print("Accuracy:", model.score(X_test, y_test))
ab=model.predict(X_test)
print(ab)
accuracy = accuracy_score(y_test, ab)
print(accuracy)

import joblib

# Save the model to a file
joblib.dump(model, 'risk_model.pkl')

print("✅ Model saved as 'risk_model.pkl'")


