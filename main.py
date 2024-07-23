import os
import pandas as pd
from coinstat.helpers import get_token_amount, update_holdings, save_user_data, load_user_data, handle_address, add_tokens
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
        update_existing = input("Do you want to update your current portfolio? (yes/no): ").strip().lower()
        if update_existing == 'yes':
            add_new_tokens = input("Do you want to add new tokens? (yes/no): ").strip().lower()
            if add_new_tokens == 'yes':
                add_tokens(user_data, blockchains_file)
            user_data = update_holdings(user_data)
            save_user_data(user_file, user_data)
            # Display updated holdings and ratings
            show_ratings(user_file, coin_ratings_file)
        else:
            # Display existing holdings and ratings
            show_ratings(user_file, coin_ratings_file)
    else:
        print(f"New user detected: {user_name}")
        user_data = {'name': user_name, 'tokens': []}
        add_tokens(user_data, blockchains_file)
        save_user_data(user_file, user_data)
        show_ratings(user_file, coin_ratings_file)


if __name__ == "__main__":
    main()
