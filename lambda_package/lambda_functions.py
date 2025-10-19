import json
import time
import yfinance as yf
import concurrent.futures

# Cache to reduce API calls
_cache = {"data": None, "timestamp": 0}
CACHE_TTL = 300  # 5 minutes

# Top 100 tickers (US market cap)
TOP_100_TICKERS = [
    "AAPL","MSFT","GOOGL","AMZN","TSLA","META","NVDA","BRK-B","JPM","JNJ",
    "V","PG","UNH","MA","HD","DIS","BAC","XOM","ADBE","CRM",
    "NFLX","CSCO","PFE","CMCSA","TMO","VZ","INTC","ABT","NKE","CVX",
    "KO","PEP","MRK","ABBV","ACN","AVGO","ORCL","T","COST","MCD",
    "WMT","DHR","LLY","NEE","LIN","BMY","TXN","PM","QCOM","HON",
    "SBUX","IBM","LOW","RTX","CVS","AMGN","INTU","MS","AMD","GS",
    "BLK","ISRG","MDT","PLD","GE","CHTR","NOW","SPGI","BKNG","ADP",
    "FIS","MDLZ","REGN","SYK","GILD","CI","ZTS","MU","ANTM","TMUS",
    "CAT","SCHW","BDX","LRCX","AXP","CME","AMAT","DE","TJX",
    "MO","MMC","ADI","TGT","ITW","EQIX","CSX","SO","FISV","EW",
    "PNC","ADI","ICE","CCI","EL","HUM","NOC","AON","MCO","SHW"
]

# CORS headers
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "Content-Type": "application/json"
}

def fix_ticker(ticker):
    """Convert Yahoo-incompatible tickers like BRK-B -> BRK.B"""
    return ticker.replace("-", ".")

def fetch_ticker(ticker):
    """Fetch last 60 days of historical stock data with retries"""
    ticker_fixed = fix_ticker(ticker)
    for attempt in range(3):
        try:
            data = yf.download(ticker_fixed, period="60d", progress=False, auto_adjust=True)
            if data.empty:
                continue
            data = data.sort_index(ascending=True)
            history = [{
                'date': idx.strftime('%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            } for idx, row in data.iterrows()]
            return {'ticker': ticker, 'history': history}
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {ticker}: {e}")
            time.sleep(1)
    print(f"No data after retries for {ticker}")
    return {'ticker': ticker, 'history': []}  # placeholder for missing data

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS' or event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

    try:
        current_time = time.time()
        if _cache["data"] and current_time - _cache["timestamp"] < CACHE_TTL:
            return {"statusCode": 200, "headers": CORS_HEADERS,
                    "body": json.dumps({"count": len(_cache["data"]), "stocks": _cache["data"]})}

        # Fetch tickers concurrently
        all_stocks = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(fetch_ticker, t): t for t in TOP_100_TICKERS}
            for future in concurrent.futures.as_completed(futures):
                try:
                    res = future.result()
                    if res:
                        all_stocks.append(res)
                except Exception as e:
                    print(f"Future error: {str(e)}")

        # Map back to original order and ensure all tickers exist
        all_stocks_dict = {s['ticker']: s for s in all_stocks}
        ordered_stocks = [all_stocks_dict.get(t, {'ticker': t, 'history': []}) for t in TOP_100_TICKERS]

        # Cache and return
        _cache["data"] = ordered_stocks
        _cache["timestamp"] = current_time

        return {"statusCode": 200, "headers": CORS_HEADERS,
                "body": json.dumps({"count": len(ordered_stocks), "stocks": ordered_stocks})}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"statusCode": 500, "headers": CORS_HEADERS,
                "body": json.dumps({"error": str(e), "type": type(e).__name__})}
