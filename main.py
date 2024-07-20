from coinstat.helpers import get_token_amount, update_holdings, save_user_data, load_user_data
from tokeninsight.helpers import load_coin_ratings, calculate_final_scores, display_final_scores, show_ratings
import os
import pandas as pd

def main():
    user_dir = "/Users/cyh/Desktop/portfolio_manager/user"
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    user_name = input("Enter your name: ").strip().lower()
    user_file = os.path.join(user_dir, f"{user_name}.json")

    if os.path.exists(user_file):
        print(f"Welcome back, {user_name}!")
        user_data = load_user_data(user_file)
        update_existing = input("Do you want to update your current portfolio? (yes/no): ").strip().lower()
        if update_existing == 'yes':
            user_data = update_holdings(user_data)
            save_user_data(user_file, user_data)
    else:
        print(f"New user detected: {user_name}")
        user_data = {'name': user_name, 'tokens': []}

        while True:
            address = input("Enter the address (or type 'FINISH' to calculate and display portfolio): ").strip().lower()
            if address == 'finish':
                break

            # Loop through all connectionId and get valid tokens
            blockchains_file = "/Users/cyh/Desktop/portfolio_manager/coin_stat/blockchains.csv"
            blockchains_df = pd.read_csv(blockchains_file)

            for index, row in blockchains_df.iterrows():
                connection_id = row['connectionId']
                chain_name = row['name']
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

        save_user_data(user_file, user_data)

    add_new_tokens = input("Do you want to add new tokens? (yes/no): ").strip().lower()
    if add_new_tokens == 'yes':
        while True:
            address = input("Enter the address (or type 'FINISH' to stop adding tokens): ").strip().lower()
            if address == 'finish':
                break

            blockchains_file = "/Users/cyh/Desktop/portfolio_manager/coin_stat/blockchains.csv"
            blockchains_df = pd.read_csv(blockchains_file)

            for index, row in blockchains_df.iterrows():
                connection_id = row['connectionId']
                chain_name = row['name']
                try:
                    result = get_token_amount(address, connection_id)
                    if result:
                        for token in result:
                            if 'price' in token:
                                token['balanceUSD'] = token['amount'] * token['price']
                            else:
                                token['balanceUSD'] = None
                            token['chain'] = chain_name
                            token['address'] = address
                            token['connectionId'] = connection_id
                        user_data['tokens'].extend(result)
                        print(f"Tokens for {chain_name} ({connection_id}) added.")
                except (ConnectionError, ValueError) as e:
                    print(e)

        save_user_data(user_file, user_data)

    # Load coin ratings and calculate final scores
    coin_ratings_file = "/Users/cyh/Desktop/portfolio_manager/tokeninsight/coin_rating.csv"
    show_ratings(user_file, coin_ratings_file)

if __name__ == "__main__":
    main()
