from utils.blockchain_utils import BlockchainUtils
from utils.static.abis.weighted_pool_factory_abi import weighted_pool_factory_abi
from utils.static.abis.vault_abi import vault_abi
from SETTINGS import *
import os
from dotenv import load_dotenv
from b_init_pool import init_pool
from samples.samples import join_sample

load_dotenv()
PRK = os.getenv("INVESTOR")
    
# create helper for interacting with EVM blockchain
butils = BlockchainUtils(provider_url=RPC_URL, prk=PRK, gas_multi=2)

init_pool(butils=butils, init_sample=join_sample)