
from utils.blockchain_utils import BlockchainUtils
from utils.static.abis.weighted_pool_factory_abi import weighted_pool_factory_abi
from utils.static.abis.vault_abi import vault_abi
from SETTINGS import *
import os
from dotenv import load_dotenv
from samples.samples import deploy_sample
from utils.utils import extract_deploy_sample, extract_pool_data_from_logs
import sys

load_dotenv()
POOL_CREATOR_PRK = os.getenv("POOL_CREATOR")

# create helper for interacting with EVM blockchain
butils = BlockchainUtils(provider_url=RPC_URL, prk=POOL_CREATOR_PRK, gas_multi=2)

factory_contract = butils.get_contract(contract_address=WEIGHTED_FACTORY, contract_abi=weighted_pool_factory_abi)
tokens_sorted, weights, rate_providers, asset_managers = extract_deploy_sample(deploy_sample)
norm_weights = [butils.to_wei(w) for w in weights]

# build the create function on the contract
pool_creation_tx = factory_contract.functions.create(
    deploy_sample["name"], # pool name
    deploy_sample["symbol"], # pool symbol
    tokens_sorted, # pool tokens list
    norm_weights, # pool token weights list
    rate_providers, # contracts which provide rate data for tokens
    deploy_sample["swapFeePercentage"], # fee
    butils.account.address, # owner
    ZERO_BYTES32 # generateSalt()
).build_transaction({
    "from": butils.account.address,
    "gasPrice": butils.get_current_gas(),
    "nonce": butils.get_nonce()
    })

# sign and broadcast
signed_tx = butils.sign_tx(tx=pool_creation_tx)
tx_hash = butils.broadcast_signed(signed_tx=signed_tx)
tx_receipt = butils.w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"pool created, tx_hash: {butils.w3.to_hex(tx_hash)}")

# look in logs for 
pool_id, pool_addr = extract_pool_data_from_logs(tx_receipt)
print(f"pool created: addr: {pool_addr}, id: {pool_id}")


