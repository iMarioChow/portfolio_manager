import requests
import json

DEFAULT_COIN_STAT_API_KEY = "G9bXc1n6Gp6xgMBpPrdZi6R7BJ9R0HlUIg2n599/+EI="
MIN_TOKEN_VALUE_USD = 0.2

def get_token_amount(address, connection_id, api_key=DEFAULT_COIN_STAT_API_KEY):
    url = f'https://openapiv1.coinstats.app/wallet/balance?address={address}&connectionId={connection_id}'

    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: Status Code {response.status_code}")
        print(f"Response: {response.text}")
        return None

def update_holdings(user_data):
    for token in user_data['tokens']:
        address = token.get('address')
        connection_id = token.get('connectionId')
        
        if not address or not connection_id or 'symbol' not in token:
            continue
        
        try:
            result = get_token_amount(address, connection_id)
            if result:
                updated = False
                for updated_token in result:
                    if 'symbol' in updated_token and updated_token['symbol'].upper() == token['symbol'].upper():
                        token['amount'] = updated_token['amount']
                        token['price'] = updated_token['price']
                        token['balanceUSD'] = updated_token['amount'] * updated_token['price'] if 'price' in updated_token else None
                        updated = True
                        break
                if not updated:
                    print(f"Token {token['symbol']} not found in the response.")
        except (ConnectionError, ValueError) as e:
            print(e)
    return user_data

def display_token_holdings(token_holdings):
    if not token_holdings:
        print("No tokens with value found.")
        return

    # Filter out tokens with value less than MIN_TOKEN_VALUE_USD
    filtered_token_holdings = [token for token in token_holdings if token['balanceUSD'] is not None and token['balanceUSD'] >= MIN_TOKEN_VALUE_USD]

    total_portfolio_value = sum(float(token['balanceUSD']) for token in filtered_token_holdings)
    token_summary = sorted(filtered_token_holdings, key=lambda x: float(x['balanceUSD']), reverse=True)

    print(f"Total Portfolio Value (USD): {total_portfolio_value}")
    print("-" * 50)

    for token in token_summary:
        balanceUSD = token['balanceUSD']
        holding_percentage = (float(balanceUSD) / total_portfolio_value) * 100 if total_portfolio_value else 0
        print(f"Token: {token.get('name')} ({token.get('symbol')})")
        print(f"  Token Contract Address: {token.get('coinId')}")
        print(f"  Holding Amount: {token.get('amount')}")
        print(f"  Token Value (USD): {balanceUSD}")
        print(f"  Holding Percentage: {holding_percentage:.2f}%")
        print("-" * 50)

def save_user_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_user_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
