import requests
import pandas as pd
import time
from datetime import datetime

# API設定
API_KEY = "Your dune api here"
BASE_URL = "https://api.dune.com/api/echo/v1/balances/evm"

def fetch_balance(address):
    """単一アドレスの残高情報を取得する"""
    headers = {
        "X-Dune-Api-Key": API_KEY
    }
    
    try:
        response = requests.get(f"{BASE_URL}/{address}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"アドレス {address} の残高取得に失敗しました: {response.status_code}")
            return None
    except Exception as e:
        print(f"リクエストエラー: {str(e)}")
        return None

def main():
    # CSVファイルを読み込む
    df = pd.read_csv("csv-data/01JKMGFYKZTFSRVTWN57D2RR1W.csv")
    
    # 結果リストを作成
    results = []
    
    # 各アドレスを処理
    total_addresses = len(df)
    for idx, row in df.iterrows():
        print(f"処理中 {idx + 1}/{total_addresses} アドレス: {row['address']}")
        
        balance_data = fetch_balance(row['address'])
        if balance_data:
            for balance in balance_data['balances']:
                results.append({
                    'address': row['address'],
                    'chain': balance.get('chain', ''),
                    'token_address': balance.get('address', ''),
                    'amount': balance.get('amount', ''),
                    'symbol': balance.get('symbol', ''),
                    'decimals': balance.get('decimals', ''),
                    'price_usd': balance.get('price_usd', ''),
                    'value_usd': balance.get('value_usd', ''),
                })
        
        # APIレート制限を避けるため遅延を追加
        time.sleep(1)
    
    # 結果をCSVとして保存
    results_df = pd.DataFrame(results)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"balance_results_{timestamp}.csv"
    results_df.to_csv(output_file, index=False)
    print(f"結果が保存されました: {output_file}")

if __name__ == "__main__":
    main() 