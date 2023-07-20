import json
import requests

with open('pairs.json') as f:
    all_pairs_data = json.loads(f.read())

with open('symbol_to_coingecko_id.json') as f:
    symbol_to_coingecko_id = json.loads(f.read())

with open('coingecko_prices.json') as f:
    prices = json.loads(f.read())

calculated_pairs = []

for pair in all_pairs_data:
    pair['symbol0'] = pair['symbol0'].lower()
    pair['symbol1'] = pair['symbol1'].lower()

    if pair['symbol0'] not in symbol_to_coingecko_id or pair['symbol1'] not in symbol_to_coingecko_id:
        print(f'Skipping {pair} since one of the tokens is not in symbol_to_coingecko_id')
        continue

    pair['coingecko0'] = symbol_to_coingecko_id[pair['symbol0']]
    pair['coingecko1'] = symbol_to_coingecko_id[pair['symbol1']]
    if pair['coingecko0'] not in prices or pair['coingecko1'] not in prices:
        print(f'Skipping {pair} since {pair["coingecko0"]} or {pair["coingecko1"]} is not in prices')
        continue

    pair['price0'] = prices[pair['coingecko0']]
    pair['price1'] = prices[pair['coingecko1']]
    pair['normalized_amount_0'] = pair['reserve0'] / 10 ** pair['decimals0']
    pair['normalized_amount_1'] = pair['reserve1'] / 10 ** pair['decimals1']
    pair['value0'] = pair['normalized_amount_0'] * pair['price0']
    pair['value1'] = pair['normalized_amount_1'] * pair['price1']

    calculated_pairs.append(pair)

with open('calculated_pairs.json', 'w') as f:
    f.write(json.dumps(calculated_pairs, indent=4))
