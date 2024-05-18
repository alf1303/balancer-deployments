from utils.blockchain_utils import BlockchainUtils
from utils.static.abis.weighted_pool_factory_abi import weighted_pool_factory_abi
from utils.static.abis.vault_abi import vault_abi
from SETTINGS import *
import os
from dotenv import load_dotenv
from utils.utils import get_deployed_pools_addresses, get_pools_data
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

load_dotenv()
PRK = os.getenv("POOL_CREATOR")

butils = BlockchainUtils(provider_url=RPC_URL, prk=PRK)
factory = butils.get_contract(contract_address=WEIGHTED_FACTORY, contract_abi=weighted_pool_factory_abi)
vault = butils.get_contract(contract_address=VAULT, contract_abi=vault_abi)

pools = get_deployed_pools_addresses(factory=factory)
pools_data = get_pools_data(butils=butils, vault=vault, pools=pools, log=False)
for address, data in pools_data.items():
    pp.pprint(data)
    print("-----------------")
print(f"Total deployed: {len(pools_data)}")
