import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from coinstat.helpers import get_token_amount, update_holdings, save_user_data, load_user_data, handle_address, add_tokens, group_holdings, save_report_csv, plot_holdings
from tokeninsight.helpers import load_coin_ratings, calculate_final_scores, display_final_scores, show_ratings

def plot_pie_chart(data, username):
    df = pd.DataFrame(data)
    df = df[df['balanceUSD'] > 0]  # Filter out zero balances
    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(df['balanceUSD'], labels=None, autopct='%1.1f%%', startangle=140, textprops=dict(color="w"))
    for i, (text, autotext) in enumerate(zip(texts, autotexts)):
        text.set_text(f"{df['symbol'][i]}")
        text.set_fontsize(8)
        autotext.set_text(f"{df['symbol'][i]} ({autotext.get_text()})")
        autotext.set_color('black')
        autotext.set_fontsize(8)
    plt.title(f'{username} Portfolio Distribution')
    plt.tight_layout()
    pie_chart_filename = f'{username}_portfolio_pie_chart.png'
    plt.savefig(pie_chart_filename)
    plt.close()
    return pie_chart_filename

def plot_hexagon_diagram(overall_scores, username):
    categories = [
        'Total Rating Score', 'Total Underlying Technology Security', 
        'Total Ecosystem Development', 'Total Team Partners & Investors', 
        'Total Token Economics', 'Total Roadmap Progress'
    ]
    values = [
        overall_scores['Total Rating Score'], overall_scores['Total Underlying Technology Security'],
        overall_scores['Total Ecosystem Development'], overall_scores['Total Team Partners & Investors'],
        overall_scores['Total Token Economics'], overall_scores['Total Roadmap Progress']
    ]
    
    # Calculate angles for each category
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)

    # Add the score values to the hexagon chart
    for i, (angle, value) in enumerate(zip(angles, values)):
        if i < len(categories):
            ax.text(angle, value + 2, f'{value:.2f}', ha='center', va='center', fontsize=10)

    plt.title(f'{username} Overall Portfolio Rating', size=16, color='blue', y=1.1)
    plt.tight_layout()
    hexagon_diagram_filename = f'{username}_portfolio_hexagon_diagram.png'
    plt.savefig(hexagon_diagram_filename)
    plt.close()
    return hexagon_diagram_filename


def save_final_report(overall_scores, holdings_df, file_path):
    # Create DataFrame with only overall scores
    metrics_df = pd.DataFrame([overall_scores]).drop(columns=['plot_file', 'hexagon_plot_file'])
    metrics_df.index = ['Final Report']
    
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        metrics_df.to_excel(writer, sheet_name='Metrics')
        holdings_df.to_excel(writer, sheet_name='Holdings', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Metrics']

        # Insert the images into the Excel file with proper sizing and positions
        worksheet.insert_image('B5', overall_scores['plot_file'], {'x_scale': 0.5, 'y_scale': 0.5})
        worksheet.insert_image('B30', overall_scores['hexagon_plot_file'], {'x_scale': 0.5, 'y_scale': 0.5})

    print(f"Report saved to {file_path}")

def main():
    # Define relative paths
    script_dir = os.path.dirname(__file__)
    user_dir = os.path.join(script_dir, "user")
    report_dir = os.path.join(user_dir, "report")
    diagram_dir = os.path.join(user_dir, "diagram")
    json_dir = os.path.join(user_dir, "json")
    blockchains_file = os.path.join(script_dir, "coinstat", "blockchains.csv")
    coin_ratings_file = os.path.join(script_dir, "tokeninsight", "coin_rating.csv")
    
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    if not os.path.exists(diagram_dir):
        os.makedirs(diagram_dir)
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    user_name = input("Enter your name: ").strip().lower()
    user_file = os.path.join(json_dir, f"{user_name}.json")

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

    # Load ratings and calculate final scores
    coin_ratings = load_coin_ratings(coin_ratings_file)
    final_scores = calculate_final_scores(user_data['tokens'], coin_ratings)

    # Group holdings by symbol and calculate total balance
    grouped_holdings = group_holdings(user_data['tokens'])
    total_portfolio_value = sum(item['balanceUSD'] for item in grouped_holdings)
    overall_scores = {
        'Total Rating Score': sum(score['rating_score'] for score in final_scores),
        'Total Underlying Technology Security': sum(score['underlying_technology_security'] for score in final_scores),
        'Total Ecosystem Development': sum(score['ecosystem_development'] for score in final_scores),
        'Total Team Partners & Investors': sum(score['team_partners_investors'] for score in final_scores),
        'Total Token Economics': sum(score['token_economics'] for score in final_scores),
        'Total Roadmap Progress': sum(score['roadmap_progress'] for score in final_scores),
        'Total Portfolio USD Balance': total_portfolio_value
    }

    # Sort holdings by balanceUSD in descending order
    holdings_df = pd.DataFrame(grouped_holdings).sort_values(by='balanceUSD', ascending=False)

    # Plot and save the diagrams
    plot_file = plot_pie_chart(grouped_holdings, user_name)
    hexagon_plot_file = plot_hexagon_diagram(overall_scores, user_name)
    os.rename(plot_file, os.path.join(diagram_dir, plot_file))
    os.rename(hexagon_plot_file, os.path.join(diagram_dir, hexagon_plot_file))
    overall_scores['plot_file'] = os.path.join(diagram_dir, plot_file)
    overall_scores['hexagon_plot_file'] = os.path.join(diagram_dir, hexagon_plot_file)

    # Save the report in Excel
    report_file_path = os.path.join(report_dir, f"{user_name}_portfolio_report.xlsx")
    save_final_report(overall_scores, holdings_df, report_file_path)

if __name__ == "__main__":
    main()
