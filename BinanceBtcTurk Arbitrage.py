import sys
import requests
import time
import pandas as pd


# Configure pandas to show all rows and columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)  # Adjust table width
pd.set_option('display.colheader_justify', 'center')  # Center headers


# Binance Spot API Configuration
BINANCE_API_URL = "https://api.binance.com/api/v3"
BINANCE_FUTURES_URL = "https://fapi.binance.com/fapi/v1"

# BtcTurk API Configuration
BTCTURK_API_URL = "https://api.btcturk.com/api/v2"

# Function to fetch Binance spot order book
def get_binance_spot_order_book(symbol):
    url = f"{BINANCE_API_URL}/depth"
    params = {"symbol": symbol, "limit": 5}
    response = requests.get(url, params=params)
    data = response.json()
    return {
        "bid": float(data['bids'][0][0]),
        "ask": float(data['asks'][0][0]),
    }

# Function to fetch Binance futures order book
def get_binance_futures_order_book(symbol):
    url = f"{BINANCE_FUTURES_URL}/depth"
    params = {"symbol": symbol, "limit": 5}
    response = requests.get(url, params=params)
    data = response.json()
    return {
        "bid": float(data['bids'][0][0]),
        "ask": float(data['asks'][0][0]),
    }

# Function to fetch BtcTurk order book
def get_btcturk_order_book(pair_symbol):
    url = f"{BTCTURK_API_URL}/orderbook"
    params = {"pairSymbol": pair_symbol}
    response = requests.get(url, params=params)
    data = response.json()
    
    # Access the bids and asks from the nested "data" field
    bids = data["data"]["bids"]
    asks = data["data"]["asks"]
    
    # Ensure lists are not empty before accessing
    if not bids or not asks:
        raise ValueError("No bids or asks available in BtcTurk order book.")
    
    return {
        "bid": float(bids[0][0]),  # First element in bids is the price
        "ask": float(asks[0][0]),  # First element in asks is the price
    }


# Function to find arbitrage opportunities
def find_arbitrage_opportunities(symbol_map):
    SymbolsWithErrors = []
    opportunities = []
    i = 0
    
    print("Getting price data from Binance & Btcturk...")
    
    for symbol, pair_symbol in symbol_map.items():
        
        i = i + 1
        sys.stdout.write('\r')
        m = int(i/len(symbol_map)*20)
        n = i/len(symbol_map)*100
        sys.stdout.write(str(i)+"/"+str(len(symbol_map)) + " " + symbol + " " +"[%-20s] %d%%" % ('='*m, n)+ "                 ")
        sys.stdout.flush()  
        
        
        try:
            binance_spot = get_binance_spot_order_book(symbol)
            binance_futures = get_binance_futures_order_book(symbol)
            btcturk = get_btcturk_order_book(pair_symbol)

            # Calculate price differences
            spot_to_btcturk_diff = -(btcturk['ask'] - binance_spot['bid']) / binance_spot['bid'] * 100
            spot_to_futures_diff = -(binance_futures['bid'] - binance_spot['bid']) / binance_spot['bid'] * 100

            # Check for opportunities
            if 1:
                opportunities.append({
                    "symbol": symbol,
                    "spot_to_btcturk_diff": round(spot_to_btcturk_diff, 2),
                    "spot_to_futures_diff": round(spot_to_futures_diff, 2),
                    "binance_spot_bid": binance_spot['bid'],
                    "btcturk_bid": btcturk['bid'],
                    "btcturk_ask": btcturk['ask'],
                    "binance_futures_bid": binance_futures['bid'],
                })
        except Exception as e:
            #print(f"Error for symbol {symbol}: {e}")
            SymbolsWithErrors.append({symbol})
    
    return pd.DataFrame(opportunities),SymbolsWithErrors

# Symbol map (Binance symbol -> BtcTurk pairSymbol)
symbol_map = {
    "BTCUSDT": "BTC_USDT",
    "AAVEUSDT": "AAVE_USDT",
    "ACMUSDT": "ACM_USDT",
    "ADAUSDT": "ADA_USDT",
    "AFCUSDT": "AFC_USDT",
    "AIOZUSDT": "AIOZ_USDT",
    "ALGOUSDT": "ALGO_USDT",
    "AMPUSDT": "AMP_USDT",
    "ANKRUSDT": "ANKR_USDT",
    "APEUSDT": "APE_USDT",
    "API3USDT": "API3_USDT",
    "APTUSDT": "APT_USDT",
    "ARBUSDT": "ARB_USDT",
    "ARKMUSDT": "ARKM_USDT",
    "ARPAUSDT": "ARPA_USDT",
    "ASRUSDT": "ASR_USDT",
    "ATMUSDT": "ATM_USDT",
    "ATOMUSDT": "ATOM_USDT",
    "AUDIOUSDT": "AUDIO_USDT",
    "AVAXUSDT": "AVAX_USDT",
    "AXLUSDT": "AXL_USDT",
    "AXSUSDT": "AXS_USDT",
    "BANDUSDT": "BAND_USDT",
    "BARUSDT": "BAR_USDT",
    "BATUSDT": "BAT_USDT",
    "BLURUSDT": "BLUR_USDT",
    "BNTUSDT": "BNT_USDT",
    "BONKUSDT": "BONK_USDT",
    "CHZUSDT": "CHZ_USDT",
    "CITYUSDT": "CITY_USDT",
    "COMPUSDT": "COMP_USDT",
    "CRVUSDT": "CRV_USDT",
    "CTSIUSDT": "CTSI_USDT",
    "CVCUSDT": "CVC_USDT",
    "DASHUSDT": "DASH_USDT",
    "DOGEUSDT": "DOGE_USDT",
    "DOTUSDT": "DOT_USDT",
    "EIGENUSDT": "EIGEN_USDT",
    "ENJUSDT": "ENJ_USDT",
    "ENSUSDT": "ENS_USDT",
    "EOSUSDT": "EOS_USDT",
    "ETCUSDT": "ETC_USDT",
    "ETHUSDT": "ETH_USDT",
    "ETHWUSDT": "ETHW_USDT",
    "FBUSDT": "FB_USDT",
    "FETUSDT": "FET_USDT",
    "FILUSDT": "FIL_USDT",
    "FLOKIUSDT": "FLOKI_USDT",
    "FLOWUSDT": "FLOW_USDT",
    "FLRUSDT": "FLR_USDT",
    "FTMUSDT": "FTM_USDT",
    "GALAUSDT": "GALA_USDT",
    "GALUSDT": "GAL_USDT",
    "GLMRUSDT": "GLMR_USDT",
    "GLMUSDT": "GLM_USDT",
    "GMTUSDT": "GMT_USDT",
    "GRTUSDT": "GRT_USDT",
    "HBARUSDT": "HBAR_USDT",
    "HNTUSDT": "HNT_USDT",
    "HOTUSDT": "HOT_USDT",
    "IMXUSDT": "IMX_USDT",
    "INJUSDT": "INJ_USDT",
    "INTERUSDT": "INTER_USDT",
    "JASMYUSDT": "JASMY_USDT",
    "JUPUSDT": "JUP_USDT",
    "JUVUSDT": "JUV_USDT",
    "KAVAUSDT": "KAVA_USDT",
    "KSMUSDT": "KSM_USDT",
    "LDOUSDT": "LDO_USDT",
    "LINKUSDT": "LINK_USDT",
    "LPTUSDT": "LPT_USDT",
    "LRCUSDT": "LRC_USDT",
    "LTCUSDT": "LTC_USDT",
    "LUNAUSDT": "LUNA_USDT",
    "MAGICUSDT": "MAGIC_USDT",
    "MANAUSDT": "MANA_USDT",
    "MASKUSDT": "MASK_USDT",
    "MKRUSDT": "MKR_USDT",
    "MNTUSDT": "MNT_USDT",
    "NAPUSDT": "NAP_USDT",
    "NEARUSDT": "NEAR_USDT",
    "NEOUSDT": "NEO_USDT",
    "NMRUSDT": "NMR_USDT",
    "OGNUSDT": "OGN_USDT",
    "OMGUSDT": "OMG_USDT",
    "ONDOUSDT": "ONDO_USDT",
    "OPUSDT": "OP_USDT",
    "PAXGUSDT": "PAXG_USDT",
    "PEPEUSDT": "PEPE_USDT",
    "POLUSDT": "POL_USDT",
    "PSGUSDT": "PSG_USDT",
    "PYTHUSDT": "PYTH_USDT",
    "QNTUSDT": "QNT_USDT",
    "RADUSDT": "RAD_USDT",
    "RAREUSDT": "RARE_USDT",
    "RENDERUSDT": "RENDER_USDT",
    "RLCUSDT": "RLC_USDT",
    "RUNEUSDT": "RUNE_USDT",
    "SANDUSDT": "SAND_USDT",
    "SHIBUSDT": "SHIB_USDT",
    "SKLUSDT": "SKL_USDT",
    "SNXUSDT": "SNX_USDT",
    "SOLUSDT": "SOL_USDT",
    "SPELLUSDT": "SPELL_USDT",
    "STORJUSDT": "STORJ_USDT",
    "STRKUSDT": "STRK_USDT",
    "STXUSDT": "STX_USDT",
    "SUPERUSDT": "SUPER_USDT",
    "SUSHIUSDT": "SUSHI_USDT",
    "TIAUSDT": "TIA_USDT",
    "TONUSDT": "TON_USDT",
    "TRAUSDT": "TRA_USDT",
    "TRXUSDT": "TRX_USDT",
    "TUSDT": "T_USDT",
    "UMAUSDT": "UMA_USDT",
    "UNIUSDT": "UNI_USDT",
    "USDCUSDT": "USDC_USDT",
    "WIFUSDT": "WIF_USDT",
    "WLDUSDT": "WLD_USDT",
    "WUSDT": "W_USDT",
    "XCNUSDT": "XCN_USDT",
    "XLMUSDT": "XLM_USDT",
    "XRPUSDT": "XRP_USDT",
    "XTZUSDT": "XTZ_USDT",
    "ZKUSDT": "ZK_USDT",
    "ZROUSDT": "ZRO_USDT",
    "ZRXUSDT": "ZRX_USDT",
}

# Run the checker
if __name__ == "__main__":
    while True:
        
        #print(get_binance_spot_order_book("BTCUSDT"))
        #print(get_binance_futures_order_book("BTCUSDT"))
        #print(get_btcturk_order_book("BTC_USDT"))
        
        opportunities,SymbolsWithErrors = find_arbitrage_opportunities(symbol_map)
        if not opportunities.empty:
            print(opportunities)
            print(f"SymbolsWithErrors:  {SymbolsWithErrors} \n")
        else:
            print("No arbitrage opportunities found.")
        time.sleep(5)  # Fetch every 5 seconds

