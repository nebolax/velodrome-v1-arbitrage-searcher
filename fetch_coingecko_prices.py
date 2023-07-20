import requests
import json
from tqdm import tqdm


with open('symbol_to_coingecko_id.json') as f:
    coingecko_ids = json.loads(f.read()).values()


with open('coingecko_prices.json') as f:
    prices = json.loads(f.read())

for id in tqdm(coingecko_ids):
    if id in prices:
        continue
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd')
        if response.status_code == 429:
            print('Rate limited, exiting')
            break
        price = response.json()[id]['usd']
        prices[id] = price
    except Exception as e:
        print(f'For id {id} got exception {str(e)}')

with open('coingecko_prices.json', 'w') as f:
    f.write(json.dumps(prices, indent=4))
    