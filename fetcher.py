import asyncio
import json
from web3 import Web3, WebsocketProvider

class BlockchainFetcher:

    def __init__(self, chain_name, rpc_url, fetch_interval, reorg_depth):
        self.chain_name = chain_name
        self.rpc_url = rpc_url
        self.fetch_interval = fetch_interval
        self.reorg_depth = reorg_depth
        self.w3 = self._connect()

    def _connect(self):
        return Web3(WebsocketProvider(self.rpc_url))

    async def fetch_data(self):
        while True:
            try:
                await self._fetch_single_block()
                await asyncio.sleep(self.fetch_interval)

            except ConnectionRefusedError:
                print(f"Connection error for {self.chain_name}. Retrying...")
                self.w3 = self._connect()
                await asyncio.sleep(self.fetch_interval)

    async def _fetch_single_block(self):
        block = self.w3.eth.get_block('latest')
        print(f"Received data for {self.chain_name}: {block['number']}")

async def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    fetch_interval = config["global_settings"]["fetch_interval"]

    tasks = []
    for chain in config["chains"]:
        fetcher = BlockchainFetcher(chain["chain_name"], chain["rpc_url"], fetch_interval, chain["reorg_depth"])
        tasks.append(fetcher.fetch_data())

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
