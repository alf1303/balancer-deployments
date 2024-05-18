import pprint as pprinter
from typing import Dict, List, Tuple
import eth_abi
import binascii
import random
from .blockchain_utils import BlockchainUtils
from .static.abis.weighted_pool_abi import weighted_pool_abi
from .static.abis.vault_abi import vault_abi
from .static.abis.weighted_pool_factory_abi import weighted_pool_factory_abi

rpc_dict = {}
    
def generateSalt(salt_input=None):
    if salt_input is None:
        salt_input = random.randint(0, 2**256 - 1)
    salt = eth_abi.encode(['uint256'],[int(salt_input)])
    salt_hex = binascii.hexlify(salt)
    salt_str = "0x" + salt_hex.decode("ascii")
    return(salt_str)

def extract_deploy_sample(sample: Dict[str, any]) -> Tuple[List[str], List[int], List[str], List[str]]:
    tdata = sample["tokens"]
    tokens = list(tdata.keys())
    tokens_sorted = sorted(tokens, key=lambda x: x.lower())
    weights = [tdata[t]["weight"] for t in tokens_sorted]
    rate_providers = [tdata[t]["rateProvider"] for t in tokens_sorted]
    asset_managers = [tdata[t]["assetManager"] for t in tokens_sorted]
    return tokens_sorted, weights, rate_providers, asset_managers

def extract_init_sample(sample: Dict[str, any]) -> Tuple[List[str], List[int]]:
    tdata = sample["tokens"]
    tokens = list(tdata.keys())
    tokens_sorted = sorted(tokens, key=lambda x: x.lower())
    amounts = [tdata[t]["amount"]for t in tokens_sorted]
    return tokens_sorted, amounts

def extract_pool_data_from_logs(tx_receipt):
    """For pool creating event"""
    pool_addr = "unknown"
    pool_id = "unknown"
    topic = "0x3c13bc30b8e878c53fd2a36b679409c073afd75950be43d8858768e956fbc20e"
    logs = tx_receipt["logs"]
    for log in logs:
        topics = [binascii.hexlify(t).decode('utf-8') for t in log["topics"]]
        if topic[2:] == topics[0]:
            pool_id = "0x" + topics[1]
            pool_addr = "0x" + topics[2][24:]       
    return pool_id, pool_addr

def decode_pool_id(pool_id: str) -> Tuple[str, int, int]:
    """pool_addr, pool_specialization, pool_nonce"""
    if len(pool_id) != 66:
        raise Exception(f"Invalid pool_id: {pool_id}")
    addr = pool_id[:42]
    pool_specialization = int(pool_id[45])
    pool_nonce = int(pool_id[46:])
    return addr, pool_specialization, pool_nonce

def get_deployed_pools_addresses(factory) -> List[str]:
    pools = []
    start_block_number = 5896550
    event_name = "PoolCreated"
    event_filter = factory.events[event_name].get_logs(fromBlock=start_block_number)
    for f in event_filter:
        pools.append(f["args"]["pool"])
    return pools
        
def get_pools_data(butils: BlockchainUtils, vault, pools: List[str], log: bool=False) -> Dict[str, Dict[str, any]]:
    pools_data = {}
    for p_address in pools:
        weighted_pool = butils.get_contract(contract_address=p_address, contract_abi=weighted_pool_abi)
        pool_id = butils.to_hex(weighted_pool.functions.getPoolId().call())
        pool_name = weighted_pool.functions.name().call()
        norm_weights = weighted_pool.functions.getNormalizedWeights().call()
        
        pool_tokens = vault.functions.getPoolTokens(pool_id).call()
        pool = {"id": pool_id, "address": p_address, "name": pool_name, "weights": norm_weights, "tokens": pool_tokens[0]}
        pools_data[p_address] = pool
        if log:
            print(f"pool name: {pool_name}")
            print(f"poolId: {butils.to_hex(pool_id)}, pool_addr: {p_address}")
            print(f"norm weights: {norm_weights}")
            print(f"pool tokens: {pool_tokens}")
            print("----------------------")
    return pools_data
