# Portfolio Manager

Portfolio Manager is a Python-based application to manage and analyze cryptocurrency portfolios. It integrates with various blockchain networks to fetch token holdings and provides a rating report using Token Insight data.

## Features

- Fetch and update token holdings from various blockchain networks.
- Calculate and display the total portfolio value.
- Generate and display a rating report for tokens using Token Insight data.

## Directory Structure

```plaintext
portfolio_manager/
├── coin_stat/
│   ├── __init__.py
│   ├── helpers.py
│   └── blockchains.csv
├── token_insight/
│   ├── __init__.py
│   ├── helpers.py
│   └── coin_rating.csv
├── user/
│   ├── json/
│   │   └── [user_name].json
│   ├── report/
│   │   └── [user_name]_portfolio_report.xlsx
│   ├── diagram/
│       ├── [user_name]_portfolio_pie_chart.png
│       └── [user_name]_portfolio_hexagon_diagram.png
├── main.py
└── README.md


```
## Installation
Clone the repository:

```bash
git clone https://github.com/iMarioChow/portfolio_manager.git
```
Navigate to the project directory:
```bash
cd portfolio_manager
Install the required dependencies (if any):
```

## Usage
Run the main script:

```bash
python main.py
```
Enter your name when prompted. If you are a returning user, you will be asked if you want to update your portfolio.

If you choose to update your portfolio, the script will fetch updated token holdings from the blockchain networks.

You will then be asked if you want to add new tokens to your portfolio. If you choose to add new tokens, you will need to provide the token addresses.

The script will display your total portfolio value and the token holdings.

Finally, a rating report will be generated and displayed using Token Insight data.

## Data Files
blockchains.csv
This file contains the blockchain networks and their connection IDs.

coin_rating.csv
This file contains the Token Insight ratings for various tokens.

[user_name].json
This file stores the user's token holdings and other relevant data.

##Requirements
To install the necessary packages for running the Portfolio Manager, use the following pip command:

```bash
pip install requests pandas matplotlib openpyxl numpy
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

