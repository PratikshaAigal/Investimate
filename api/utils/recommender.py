import pandas as pd
import joblib
import yfinance as yf

# Asset name to ticker symbol map
TICKER_MAP = {
    'Natural_Gas': 'NG=F',
    'Crude_oil': 'CL=F',
    'Copper': 'HG=F',
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD',
    'Platinum': 'PL=F',
    'Gold': 'GC=F',
    'Silver': 'SI=F',
    'Apple': 'AAPL',
    'Tesla': 'TSLA',
    'Microsoft': 'MSFT',
    'Google': 'GOOGL',
    'Nvidia': 'NVDA',
    'Amazon': 'AMZN',
    'Netflix': 'NFLX',
    'Meta': 'META',
    'Berkshire': 'BRK-B'
}
def recommend_assets(user_risk_level: str, top_n: int = 5):


    df = pd.read_csv('asset_features.csv')
    model = joblib.load('risk_model.pkl')

    # Predict using model (raw values, no scaling)
    X = df[['Volatility', 'Liquidity', 'Market_Risk', 'Timing_Risk', 'Avg_Return']]
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

    # Market summary using apply
    recommended['Market_Summary'] = recommended['Asset'].apply(
        lambda asset: get_simple_market_summary(TICKER_MAP.get(asset)) if TICKER_MAP.get(
            asset) else "No ticker symbol found."
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
        'Explanation',
       'Market_Summary']].rename(
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


def get_simple_market_summary(ticker_symbol, period="7d"):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            return f"No recent trend data for {ticker_symbol}."

        close_prices = hist['Close']
        start_price = close_prices.iloc[0]
        end_price = close_prices.iloc[-1]
        change = end_price - start_price
        percent = (change / start_price) * 100
        direction = "up" if change > 0 else "down"

        return (
            f"{ticker_symbol} is trading at ${end_price:.2f}, "
            f"{direction} {abs(percent):.2f}% over the last {period.replace('d',' days')}."
        )
    except Exception as e:
        return f"Error fetching trend for {ticker_symbol}: {str(e)}"