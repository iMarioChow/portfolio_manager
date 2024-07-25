import requests
import pandas as pd

# API headers
headers = {
    "accept": "application/json",
    "TI_API_KEY": "08cc949363654905a0c6dee962f0c29d" ## Your_api_key
}

# API endpoint for initial coin ratings
url = "https://api.tokeninsight.com/api/v1/rating/coins"

# Function to fetch initial coin data and save to CSV
def fetch_initial_coin_data():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get('data', {}).get('items', [])
        
        if not isinstance(data, list):
            print("Unexpected data structure:", type(data))
            return
        
        coin_list = []

        for item in data:
            if isinstance(item, dict):
                coin_list.append({
                    'tid': item.get('tid', 'N/A'),
                    'rating_level': item.get('rating_level', 'N/A'),
                    'rating_score': item.get('rating_score', 'N/A'),
                    'underlying_technology_security': item.get('underlying_technology_security', 'N/A'),
                    'token_performance': item.get('token_performance', 'N/A'),
                    'ecosystem_development': item.get('ecosystem_development', 'N/A'),
                    'team_partners_investors': item.get('team_partners_investors', 'N/A'),
                    'token_economics': item.get('token_economics', 'N/A'),
                    'roadmap_progress': item.get('roadmap_progress', 'N/A'),
                    'tags': ', '.join(item.get('tags', []))
                })
            else:
                print("Unexpected item structure:", type(item), item)

        df = pd.DataFrame(coin_list)
        df.to_csv("coin_list.csv", index=False)
        print("Initial coin data saved to coin_list.csv")
    else:
        print(f"Failed to fetch initial coin data: {response.status_code}")

# Execute the function
fetch_initial_coin_data()
