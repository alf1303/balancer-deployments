# w3.eth.wait_for_transaction_receipt()
from typing import Dict, List, Tuple

import eth_abi
import eth_abi.decoding
from utils.blockchain_utils import BlockchainUtils
from utils.static.abis.weighted_pool_factory_abi import weighted_pool_factory_abi
from utils.static.abis.vault_abi import vault_abi
from utils.static.abis.weighted_pool_abi import weighted_pool_abi
from SETTINGS import *
import os
from dotenv import load_dotenv
import sys
from hexbytes import HexBytes
from utils.utils import decode_pool_id, extract_init_sample
from samples.samples import init_sample

load_dotenv()
PRK = os.getenv("POOL_CREATOR")
    
def init_pool(butils: BlockchainUtils, init_sample: Dict[str, any]):
    from_internal_balance = False
    pool_id = init_sample["poolId"]
    join_kind = init_sample["joinKind"]
    tokens_sorted, amounts = extract_init_sample(init_sample)
    norm_amounts = [butils.to_wei(a) for a in amounts]
    pool_addr, pool_spec, pool_nonce = decode_pool_id(pool_id=pool_id)
    vault_contract = butils.get_contract(contract_address=VAULT, contract_abi=vault_abi)
    max_amounts_in = norm_amounts
    checksum_tokens = [butils.to_checksum(el) for el in tokens_sorted]
    user_data_encoded = eth_abi.encode(	['uint256', 'uint256[]'],
												[join_kind, max_amounts_in])
    join_pool_request = (checksum_tokens, max_amounts_in, user_data_encoded, from_internal_balance)
    
    for idx, tkn in enumerate(checksum_tokens):
        amou = max_amounts_in[idx]
        balance, name = butils.get_balance(token=tkn, human=True)
        if balance < amounts[idx]:
            raise Exception(f"Too low balance for {tkn}: {balance} {name}, need: {amounts[idx]}")
        butils.set_allowance(token_id=tkn, spender=VAULT, amount=amounts[idx])

    address = butils.w3.to_checksum_address(butils.account.address)

    join_init_fn = vault_contract.functions.joinPool(
        pool_id,
        address,
        address,
        join_pool_request
    )
    join_init_tx = join_init_fn.build_transaction({
        "from": address,
        "gasPrice": butils.get_current_gas(),
        "nonce": butils.get_nonce(),
    })
    signed_tx = butils.sign_tx(tx=join_init_tx)
    tx_hash = butils.broadcast_signed(signed_tx=signed_tx)
    tx_receipt = butils.w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    print(f"join tx_hash: {butils.w3.to_hex(tx_hash)}")

def main():
    # create helper for interacting with EVM blockchain
    butils = BlockchainUtils(provider_url=RPC_URL, prk=PRK, gas_multi=2)
    init_pool(butils=butils, init_sample=init_sample)
    
if __name__ == "__main__":
    main()