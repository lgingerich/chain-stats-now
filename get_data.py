import os
import datetime
from dotenv import load_dotenv
from web3 import Web3
from supabase_py import create_client, Client

# Setup env
load_dotenv()

url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

ETH_RPC_URL = os.getenv('ETH_RPC_URL')
web3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))


block_number = 1000002
block = web3.eth.getBlock(block_number, full_transactions=True)

chain_name = "ethereum"
block_num = block['number']
block_time = datetime.datetime.utcfromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
transaction_count = len(block['transactions'])

data = {
    "chain": chain_name,
    "block_number": block_num,
    "block_time": block_time,
    "transaction_count": transaction_count
}

response = supabase.table("chain_metrics").insert(data).execute()

if response['status_code'] == 201:
    print(f"Successfully inserted the record for {data['chain']} block {data['block_number']} into chain_metrics table.")
else:
    error_message = response.get('data', {}).get('message', 'Unknown error.')
    print(f"Error ({response['status_code']}): {error_message}")