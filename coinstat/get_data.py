import requests
import pandas as pd

url = "https://openapiv1.coinstats.app/wallet/blockchains"

headers = {
    "accept": "application/json",
    "X-API-KEY": "G9bXc1n6Gp6xgMBpPrdZi6R7BJ9R0HlUIg2n599/+EI="
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    coin_list = []

    for item in data:
        coin_list.append({
            'connectionId': item.get('connectionId', 'N/A'),
            'name': item.get('name', 'N/A')
        })

    df = pd.DataFrame(coin_list)
    df.to_csv("/Users/cyh/Desktop/portfolio_manager/coin_stat/blockchains1.csv", index=False)
    print("Blockchain data saved to blockchains1.csv")
else:
    print(f"Failed to fetch blockchain data: {response.status_code}")
