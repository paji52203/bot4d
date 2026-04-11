import ccxt, os
from dotenv import load_dotenv
load_dotenv()

def test_api(name, is_testnet):
    print(f'Testing {name}...')
    try:
        ex = ccxt.bybit({
            'apiKey': os.getenv('BYBIT_API_KEY'),
            'secret': os.getenv('BYBIT_API_SECRET'),
        })
        ex.set_sandbox_mode(is_testnet)
        # Attempt to fetch balance to trigger authentication
        ex.fetch_balance()
        print(f'SUCCESS: {name} connected!')
        return True
    except Exception as e:
        print(f'FAILED: {name} error: {str(e)}')
        return False

print('API Key:', os.getenv('BYBIT_API_KEY'))
test_api('Mainnet', False)
test_api('Testnet', True)
