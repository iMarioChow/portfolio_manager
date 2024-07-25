import json
import pandas as pd

def load_user_data(user_file):
    with open(user_file, 'r') as file:
        return json.load(file)

def load_coin_ratings(csv_file):
    df = pd.read_csv(csv_file)
    percentage_columns = [
        'underlying_technology_security',
        'token_performance',
        'ecosystem_development',
        'team_partners_investors',
        'token_economics',
        'roadmap_progress'
    ]
    for col in percentage_columns:
        df[col] = df[col].str.rstrip('%').astype(float)
    return df

def calculate_final_scores(user_tokens, coin_ratings):
    valid_tokens = [t for t in user_tokens if t['balanceUSD'] is not None and t['balanceUSD'] > 0]
    total_balance_usd = sum(t['balanceUSD'] for t in valid_tokens)

    if total_balance_usd == 0:
        return []

    final_scores = []
    for token in valid_tokens:
        symbol = token.get('symbol')
        if not symbol:
            continue
        holding_percentage = token.get('balanceUSD', 0) / total_balance_usd * 100
        if holding_percentage > 0:
            rating_info = coin_ratings[coin_ratings['symbol'].str.upper() == symbol.upper()]
            if not rating_info.empty:
                rating_info = rating_info.iloc[0]
                final_score = {
                    'symbol': symbol,
                    'name': token['name'],
                    'balanceUSD': token['balanceUSD'],
                    'holding_percentage': holding_percentage,
                    'rating_level': rating_info['rating_level'],
                    'rating_score': rating_info['rating_score'] * holding_percentage / 100,
                    'underlying_technology_security': rating_info['underlying_technology_security'] * holding_percentage / 100,
                    'token_performance': rating_info['token_performance'] * holding_percentage / 100,
                    'ecosystem_development': rating_info['ecosystem_development'] * holding_percentage / 100,
                    'team_partners_investors': rating_info['team_partners_investors'] * holding_percentage / 100,
                    'token_economics': rating_info['token_economics'] * holding_percentage / 100,
                    'roadmap_progress': rating_info['roadmap_progress'] * holding_percentage / 100
                }
                final_scores.append(final_score)
    return final_scores

def display_final_scores(final_scores):
    if not final_scores:
        print("Empty wallet.")
        return

    overall_scores = {
        'rating_score': 0,
        'underlying_technology_security': 0,
        'token_performance': 0,
        'ecosystem_development': 0,
        'team_partners_investors': 0,
        'token_economics': 0,
        'roadmap_progress': 0
    }

    total_portfolio_value = sum(score['balanceUSD'] for score in final_scores)


    for score in final_scores:
    #     print(f"Token: {score['name']} ({score['symbol']})")
    #     print(f"  Balance USD: {score['balanceUSD']}")
    #     print(f"  Holding Percentage: {score['holding_percentage']:.2f}%")
    #     print(f"  Rating Level: {score['rating_level']}")
    #     print(f"  Rating Score: {score['rating_score']/score['holding_percentage']*100:.2f}")
    #     print(f"  Underlying Technology Security: {score['underlying_technology_security']/score['holding_percentage']*100:.2f}")
    #     print(f"  Token Performance: {score['token_performance']/score['holding_percentage']*100:.2f}")
    #     print(f"  Ecosystem Development: {score['ecosystem_development']/score['holding_percentage']*100:.2f}")
    #     print(f"  Team Partners & Investors: {score['team_partners_investors']/score['holding_percentage']*100:.2f}")
    #     print(f"  Token Economics: {score['token_economics']/score['holding_percentage']*100:.2f}")
    #     print(f"  Roadmap Progress: {score['roadmap_progress']/score['holding_percentage']*100:.2f}")
    #     print("-" * 50)

        overall_scores['rating_score'] += score['rating_score']
        overall_scores['underlying_technology_security'] += score['underlying_technology_security']
        overall_scores['token_performance'] += score['token_performance']
        overall_scores['ecosystem_development'] += score['ecosystem_development']
        overall_scores['team_partners_investors'] += score['team_partners_investors']
        overall_scores['token_economics'] += score['token_economics']
        overall_scores['roadmap_progress'] += score['roadmap_progress']

    # print("\nFinal Report:")
    # print(f"  Total Rating Score: {overall_scores['rating_score']}")
    # print(f"  Total Underlying Technology Security: {overall_scores['underlying_technology_security']}")
    # print(f"  Total Token Performance: {overall_scores['token_performance']}")
    # print(f"  Total Ecosystem Development: {overall_scores['ecosystem_development']}")
    # print(f"  Total Team Partners & Investors: {overall_scores['team_partners_investors']}")
    # print(f"  Total Token Economics: {overall_scores['token_economics']}")
    # print(f"  Total Roadmap Progress: {overall_scores['roadmap_progress']}")

def show_ratings(user_file, coin_ratings_file):
    user_data = load_user_data(user_file)
    coin_ratings = load_coin_ratings(coin_ratings_file)
    final_scores = calculate_final_scores(user_data['tokens'], coin_ratings)
    display_final_scores(final_scores)
