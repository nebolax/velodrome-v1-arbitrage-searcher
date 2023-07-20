import requests
import json
from collections import defaultdict


with open('raw_coingecko_coins_list.json') as f:
    response = json.loads(f.read())

symbol_to_id = defaultdict(list)

for item in response:
    symbol_to_id[item['symbol'].lower()].append(item['id'])


all_tokens = []

with open('pairs.json') as f:
    all_pairs_data = json.loads(f.read())

for pair_data in all_pairs_data:
    if any([x['address'] == pair_data['token0'] for x in all_tokens]) is False:
        all_tokens.append({
            'address': pair_data['token0'],
            'name': pair_data['name0'],
            'symbol': pair_data['symbol0'].lower(),
            'decimals': pair_data['decimals0']
        })
    if any([x['address'] == pair_data['token1'] for x in all_tokens]) is False:
        all_tokens.append({
            'address': pair_data['token1'],
            'name': pair_data['name1'],
            'symbol': pair_data['symbol1'].lower(),
            'decimals': pair_data['decimals1']
        })


with open('symbol_to_coingecko_id.json') as f:
    address_to_coingecko_id: dict = json.loads(f.read())


for token_data in all_tokens:
    if token_data['symbol'] in address_to_coingecko_id:
        print(f'Token with symbol {token_data["symbol"]} has already been matched to coingecko id {address_to_coingecko_id[token_data["symbol"]]}')
        continue

    if token_data['symbol'] not in symbol_to_id:
        print(f'Have not found any potential ids for token {token_data}. Enter the identifier manually or skip:')
        manual_identifier = input()
        if len(manual_identifier.strip()) != 0:
            address_to_coingecko_id[token_data['symbol']] = manual_identifier
        continue

    # Symbol is in symbol_to_id
    if len(symbol_to_id[token_data['symbol']]) == 1:
        matched_id = symbol_to_id[token_data['symbol']][0]
        print(f'Automatically matched symbol {token_data["symbol"]} to id {matched_id} since it was the only option')
        address_to_coingecko_id[token_data['symbol']] = matched_id
        continue

    # Length is 2+
    print(f'For token {token_data} there are multiple id options: {symbol_to_id[token_data["symbol"]]}. Please enter the index of the id to use')
    inp = input()
    try:
        idx = int(inp)
    except ValueError:
        print('Skipping')
    
    if idx < 0 or idx >= len(symbol_to_id[token_data['symbol']]):
        print('Skipping')

    matched_id = symbol_to_id[token_data['symbol']][idx]
    print(f'Matched symbol {token_data["symbol"]} to id {matched_id}')
    address_to_coingecko_id[token_data['symbol']] = matched_id

    with open('symbol_to_coingecko_id.json', 'w') as f:
        f.write(json.dumps(address_to_coingecko_id, indent=4))


with open('symbol_to_coingecko_id.json', 'w') as f:
    f.write(json.dumps(address_to_coingecko_id, indent=4))
