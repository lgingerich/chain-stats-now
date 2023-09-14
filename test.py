from web3 import Web3, WebsocketProvider

# Connect to Ethereum mainnet using WebSockets
w3 = Web3(Web3.WebsocketProvider('wss://ethereum.publicnode.com'))

if not w3.isConnected():
    print("Error: Couldn't connect to the Ethereum node.")
    exit()

print("Connected to Ethereum node.")

# Function to handle new block header
def handle_block(block):
    print(f"New Block: {block['number']} | Hash: {block['hash']}")

# New block filter
block_filter = w3.eth.filter('latest')

# Poll for new blocks
while True:
    for block_hash in block_filter.get_new_entries():
        block = w3.eth.getBlock(block_hash)
        handle_block(block)
