import time
import hashlib
import json
from uuid import uuid4


class Blockchain:
    def __init__(self, current_node_url=None):
        self.chain = []
        self.pending_transactions = []
        self.current_node_url = current_node_url
        
        self.network_nodes = []
        self.create_new_block(100,'0','0')

    def create_new_block(self, nonce, previous_block_hash, hash_):
        new_block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time.time() * 1000),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'hash': hash_,
            'previous_block_hash': previous_block_hash,
        }
        self.pending_transactions = []
        self.chain.append(new_block)
        return new_block
    
    def get_last_block(self):
        return self.chain[len(self.chain) - 1]
    
    def create_new_transaction(self,amount,sender,recipient):
        new_transaction = {
            'amount' : amount,
            'sender' : sender,
            'recipient' : recipient,
            'transaction_id': str(uuid4()).replace('-', '')
        }
        return new_transaction

    def hash_block(self, previous_block_hash, current_block_data, nonce):
        data_as_string = previous_block_hash + str(nonce) + json.dumps(current_block_data, separators=(',', ':'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        hash_object = hashlib.sha256(data_as_string.encode())
        hash_ = hash_object.hexdigest()
        return hash_
    
    def proof_of_work(self,previous_block_hash, current_block_data):
        nonce = 0
        hash_ = self.hash_block(previous_block_hash, current_block_data, nonce)
        while hash_[:4] != '0000':
            nonce += 1
            hash_ = self.hash_block(previous_block_hash, current_block_data, nonce)
            print(hash_)
        return nonce
    
    def add_transaction_to_pending_transactions(self,transaction_obj):
        self.pending_transactions.append(transaction_obj)
        return self.get_last_block()['index'] + 1
    

