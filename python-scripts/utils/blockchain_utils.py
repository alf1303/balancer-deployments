from datetime import datetime, timedelta
from time import time, sleep
from typing import List
from web3 import Web3
from decimal import Decimal
from utils.static.abis.erc20_abi import erc20_abi
from utils.static.abis.erc721_abi import erc721_abi
from web3.middleware import geth_poa_middleware

from utils.loggin import loginfo

class BlockchainUtils():
    """Utility class for simplifying interaction with blockchain"""
    def __init__(self, provider_url: str, prk="", base_name="ETH", poa=True, gas_multi=1):
        """
        Parameters:
        provider_url (str): Blockchain rpc url.
        prk (str): private key of account which should interact with blockchain.
        base_name (str): symbol for native chain currency
        poa (bool): False for PoW and PoS chains (Ethereum), True for Proof of Authority chains (most L2 that use validators)
        """
        self.prk = prk
        self.base_name = base_name
        self.GWEI = 10 ** 9
        self.gas_multi = gas_multi
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.chain_id = self.w3.eth.chain_id
        # self.account = None
        if poa:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        if self.w3.is_connected():
            if prk:
                self.account = self.w3.eth.account.from_key(self.prk)
                loginfo(f"signer: {self.account.address}")
            loginfo(f"Connected get_url lastBlock: {self.w3.eth.get_block('latest')['number']}")
        else:
            loginfo(f"Failed to connect to network: {provider_url}")
            
    def _get_approve_gas_limit():
        return 70000
            
    ### UTIL METHODS ###
    
    def decode_logs(self, address: str, abi, event_name, log):
        pool_contract = self.w3.eth.contract(self.to_checksum(address), abi=abi)
        decoded_logs = pool_contract.events[event_name]().process_log(log)
        return decoded_logs
    
    def to_hex(self, address):
        return self.w3.to_hex(address)
    
    def to_checksum(self, address: str):
        return self.w3.to_checksum_address(address)
        
    def to_wei(self, amount: float):
        """convert float amount in human readable format to decimal format"""
        return int(self.w3.to_wei(amount, 'ether'))

    def from_wei(self, amount: int):
        """convert int amount in decimal format to human readable format"""
        return self.w3.from_wei(amount, 'ether')

    def get_current_gas(self) -> int:
        """ Get checks network gas price """
        return self.w3.eth.gas_price * self.gas_multi

    def get_max_fee_per_gas(self) -> int:
        """ Get maxFeePerGas param for EIP-1559 networks and gasPrice for others """
        return self.get_current_gas() * self.gas_multi

    def get_eth_balance(self, address="", human=False):
        """get native currency balance
        Parameters:
        address (str): if address not set, then is used address from private key, used during creating Blockchain Utils instance.
        human (bool): if True, then returns float in human readable format, False - returns in decimal format
        """
        if not address:
            address = self.account.address
        eth_balance = self.w3.eth.get_balance(address)
        if human:
            return self.from_wei(eth_balance)
        else:
            return eth_balance
    
    def get_nonce(self, address=""):
        """get nonce (transactions count of account)
        Parameters:
        address (str): if address not set, then is used address from private key, used during creating Blockchain Utils instance.
        """
        if not address:
            address = self.account.address
        nonce = self.w3.eth.get_transaction_count(address)
        return nonce
    
    def set_allowance(self, token_id: str, spender: str, amount: float, convert_to_wei=True):
        if convert_to_wei:
            amount = self.to_wei(amount)
        else:
            amount = int(amount)
        tkn_contract = self.get_token_contract(token_address=token_id)
        approve_tx = tkn_contract.functions.approve(spender, amount).build_transaction({
            "gasPrice": self.get_current_gas(),
            "nonce": self.get_nonce()
            })
        signed_tx = self.sign_tx(tx=approve_tx)
        tx_hash = self.broadcast_signed(signed_tx=signed_tx)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"allowance tx_hash: {self.w3.to_hex(tx_hash)}")
        print(f"set allowance to {self.from_wei(amount)} for {token_id}, spender: {spender}")
    
    def broadcast_signed(self, signed_tx):
        """Broadcast signed transaction to blockhain"""
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # loglog(f"tx hash: {self.w3.to_hex(tx_hash)}")
        return tx_hash
    
    def wait_to_complete(self, tx_hashes: List[str], timeout=20, delay=0.2):
        """Wait till transactions become mined, timeout in seconds"""
        # raise Exception("Unimplemented error")
        start_t = time()
        mined = []
        while time() - start_t < timeout:
            if len(mined) == len(tx_hashes):
                loginfo(f"All txs mined")
                break
            for tx_hash in tx_hashes:
                receipt = self.w3.eth.wait_for_transaction_receipt()
    
    def sign_tx(self, tx):
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.prk)
        return signed_tx
    
    def get_token_contract(self, token_address):
        """Returns token contract object, used for interacting"""
        contract = self.w3.eth.contract(address=self.w3.to_checksum_address(token_address.lower()), abi=erc20_abi)
        return contract
    
    def get_contract(self, contract_address: str, contract_abi):
        """returns contract object for interacting
        Parameters:
        contract_abi (json): abi of contract
        """
        contract = self.w3.eth.contract(address=self.w3.to_checksum_address(contract_address.lower()), abi=contract_abi)
        return contract
    
    def create_transfer_eth_tx(self, amount: float, to: str, nonce_increaser=0):
        # loglog("--> Creating transfer ETH tx")
        nonce = self.w3.eth.get_transaction_count(self.account.address) + nonce_increaser
        # loglog(f"nonce: {nonce}")
        gas_price = self.w3.eth.gas_price
        # loglog(f"gas price: {gas_price}")
        tx = {
            "nonce": nonce,
            "to": to,
            "value": self.w3.to_wei(amount, 'ether'),
        }
        est = self.w3.eth.estimate_gas(transaction=tx)
        # loglog(f"estimated: {est}")
        tx["gas"] = est
        tx["gasPrice"] = gas_price
        print(f"Transfer ETH tx:")
        print(tx)
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.prk)
        return signed_tx
    
    def approve_token_usage(self, private_key: str, contract_address: str, spender: str, amount: int) -> bool:
        account = self.account
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=erc20_abi)
        
        tx = contract.functions.approve(spender, amount).build_transaction({       
        'from': account.address,
        'gas': self._get_approve_gas_limit(),
        'gasPrice': int(self.get_current_gas()),
        'nonce': self.get_nonce(account.address)})
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction) 
        
        try:        
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except Web3.exceptions.TimeExhausted:
            print('Approve tx waiting time exceeded')
            return False
        return True
    
    def get_balance(self, address="", token="", human=False):
        """get token balance
        Parameters:
        address (str): if address not set, than is used address from private key, used during creating Blockchain Utils instance.
        token (str): token address, if not set, then native currency (e.g. ETH) balance is returned
        human (bool): if True, then returns float in human readable format, False - returns in decimal format
        """
        if not token:
            b = self.get_eth_balance(address=address)
            if human:
                return self.from_wei(b), self.base_name
            else:
                return b, self.base_name
        else:
            adr = address if address else self.account.address
            contract = self.get_token_contract(token_address=token)
            b = contract.functions.balanceOf(self.w3.to_checksum_address(adr.lower())).call()
            decimals = contract.functions.decimals().call()
            name = contract.functions.name().call()
            
            if human:
                return b/10**decimals, name
            else:
                return b, name
    
    ####################
    
    
            
    