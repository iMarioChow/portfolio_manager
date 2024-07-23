import os
import pandas as pd
from coinstat.helpers import get_token_amount, update_holdings, save_user_data, load_user_data
from tokeninsight.helpers import load_coin_ratings, calculate_final_scores, display_final_scores, show_ratings

def main():
    # Define relative paths
    script_dir = os.path.dirname(__file__)
    user_dir = os.path.join(script_dir, "user")
    blockchains_file = os.path.join(script_dir, "coinstat", "blockchains.csv")
    coin_ratings_file = os.path.join(script_dir, "tokeninsight", "coin_rating.csv")
    
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    user_name = input("Enter your name: ").strip().lower()
    user_file = os.path.join(user_dir, f"{user_name}.json")

    if os.path.exists(user_file):
        print(f"Welcome back, {user_name}!")
        user_data = load_user_data(user_file)
        add_new_tokens = input("Do you want to add new tokens? (yes/no): ").strip().lower()
        if add_new_tokens == 'yes':
            add_tokens(user_data, blockchains_file)
        update_existing = input("Do you want to update your current portfolio? (yes/no): ").strip().lower()
        if update_existing == 'yes':
            user_data = update_holdings(user_data)
            save_user_data(user_file, user_data)
    else:
        print(f"New user detected: {user_name}")
        user_data = {'name': user_name, 'tokens': []}
        add_tokens(user_data, blockchains_file)
        save_user_data(user_file, user_data)

    # Load coin ratings and calculate final scores
    show_ratings(user_file, coin_ratings_file)

def add_tokens(user_data, blockchains_file):
    blockchains_df = pd.read_csv(blockchains_file)
    while True:
        address = input("Enter the address (or type 'FINISH' to calculate and display portfolio): ").strip()
        if address == 'finish':
            break

        if address.startswith("bc"):
            connection_id = "bitcoin"
            chain_name = blockchains_df[blockchains_df['connectionId'] == connection_id]['name'].values[0]
            handle_address(address, connection_id, chain_name, user_data)
        elif address.startswith("0x"):
            is_evm = input("Is this an EVM address? (yes/no): ").strip().lower() == 'yes'
            evm_filter = 1 if is_evm else 0
            for index, row in blockchains_df[blockchains_df['EVM'] == evm_filter].iterrows():
                connection_id = row['connectionId']
                chain_name = row['name']
                handle_address(address, connection_id, chain_name, user_data)
        else:
            for index, row in blockchains_df[blockchains_df['EVM'] == 0].iterrows():
                connection_id = row['connectionId']
                chain_name = row['name']
                handle_address(address, connection_id, chain_name, user_data)

def handle_address(address, connection_id, chain_name, user_data):
    try:
        result = get_token_amount(address, connection_id)
        if result:
            for token in result:
                if 'price' in token:
                    token['balanceUSD'] = token['amount'] * token['price']
                else:
                    token['balanceUSD'] = None
                token['chain'] = chain_name  # Add chain name to token data
                token['address'] = address  # Add address to token data
                token['connectionId'] = connection_id  # Add connectionId to token data
            user_data['tokens'].extend(result)
            print(f"Tokens for {chain_name} ({connection_id}) added.")
    except (ConnectionError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"Failed to retrieve data: {e}")

if __name__ == "__main__":
    main()
