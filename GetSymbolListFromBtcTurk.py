import requests

# BtcTurk API URL
BTCTURK_API_URL = "https://api.btcturk.com/api/v2"

def get_usdt_pairs():
    # Fetch all available trading pairs
    url = f"{BTCTURK_API_URL}/server/exchangeinfo"
    response = requests.get(url)
    data = response.json()

    # Ensure 'symbols' key exists in response data
    if "data" not in data or "symbols" not in data["data"]:
        raise ValueError("Invalid response from BtcTurk API")

    # Filter pairs that end with USDT
    usdt_pairs = [symbol["name"] for symbol in data["data"]["symbols"] if symbol["name"].endswith("USDT")]
    
    return usdt_pairs

# Call the function and get the result
usdt_pairs = get_usdt_pairs()

# Create the symbol_map in the desired format
symbol_map = {pair: pair.replace("USDT", "_USDT") for pair in usdt_pairs}

# Print the symbol_map
print("symbol_map = {")
for pair, formatted_pair in symbol_map.items():
    print(f'    "{pair}": "{formatted_pair}",')
print("}")
