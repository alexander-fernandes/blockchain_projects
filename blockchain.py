################################
#
#
#
#
#
#  BLOCKCHAIN A1
#
#  PYTHON PROJECT  
#
#  what is a blockchain? blockchain is a system of data storage, a growing list or records (blocks) that are linked to one another. 
#  Bitcoin was the first known and successful application of the Blockchain method. while blockchains have been popular and
#  dominant as a ledger system, they are not restricted to storing financial information. the type of data being stored is 
#  inconsequential to and independent of the blockchain network.
#
#  the type of data stored within blockchains must have certain qualities and characteristics, specifically: 
#
#  - immutable (cryptographic hash functions) - cryptographic hash functions are a one way algorithm that take 
#  abitrarily sized input data (key) and maps it to values of fixed sizes (hash value).
#
#  - unhackable - above, blocks chained with cryptographic hash functions are only able to be read if you compare hashes. they are even
#  harder to hack if you ingrain each hash with a salt (random number of bits) before hashing, making each hash of the same source different,
#  making hacking hashes without the salt impossible to hack.
#
#  - persistent (no loss of data)
#
#  - distributed
#
#  these qualities are necessary to maintain the integrity of the blockchain.
#
#
################################
from flask import Flask, request
from hashlib import sha256
import json
import time
import requests

class Block:
    """
    this class constitutes the makeup of a single block that will be constructed for every new transaction within the chain

    I. a blockchain consists of blocks, each block contains data about the data/transaction that 
    took place. the intialisation of this class will make it look likea json dump, something like this:

{   
    "sender": "sender_name",
    "receiver": "receiver_name",
    "timestamp": "transaction_time", 
    "data": "transaction_data"
}

    II. in order to assure immutability we'll code it so that the hash of the previous block will include with the current.
    the awareness of the data within each block will establish a mechanism for protecting the chain's integrity.

    """

    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash # (II.)
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()



class Blockchain: 
    """
    I. Satoshi Nakomoto developed the proof-of work system. this makes it increasingly difficult to peform the work required
    to generate one new block. this means that someone who modifies a previous block would need to redo all the work of 
    of the block and all the other blocks that follow it. it starts by scanning for a value that starts with a certain 
    number of zeroes when hashed. this is known as a *nonce value*. the number of leading zero bits is known as difficulty.
    the average work required to create a block increases exponentionally with the number of leading zero bits, and therefore
    increases difficulty with each new block. this way we can prevent users from modifying previous blocks since it would be 
    far from practically possible to redo the following blocks and catch up to others.

    II. we will initially store the data of each transaction in unconfirmed_transactions, and once we confirm that the new block 
    is valid proof that satisfies the difficulty, we can add it to the chain. the process of performing computational work within 
    the system is commonly known as mining.

    """

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = [] # a simple list that will keep track of each block
        self.construct_genesis()
 
    # in order to get the system going we create this function to intiate the chain,
    # with both an index and previous hash of 0 and an empty transaction, then we add this to the chain
    def construct_genesis(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    # (I.)
    difficulty = 2
    def proof_of_work(self, block):
        block.nonce = computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
            return computed_hash
        
    def construct_full_block(self):
         pass

    def add_block(self, block, proof):

        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True
 
    def is_valid_proof(self, block, block_hash):
            return (block_hash.startswith('0' * Blockchain.difficulty) and
                    block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
                self.unconfirmed_transactions.append(transaction)

    def transaction(self, sender, recipient, amount):
        # TODO: transactions per block dictated by block size limit (ie 1MB?)

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.add_new_transaction(transaction)
        return
       # return self.last_block.index += 1
       
    # (II.)
    def mine(self):
            if not self.unconfirmed_transactions:
                return False
    
            last_block = self.last_block
    
            new_block = Block(index=last_block.index + 1,
                            transactions=self.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=last_block.hash)
    
            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)
            self.unconfirmed_transactions = []
            return new_block.index
 
# create a REST API for users to interact with the chain and begin mining.
# the best way users can make a request is by running 'curl  http://127.0.0.1:5000/chain'
# or whatever the port and ip are coded here as

app =  Flask(__name__)

blockchain = Blockchain()

# every time a user sends a GET request to the API, we'll return the blockchain data
# dump entire blockchain content to the console, and all the data for and in every block
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

app.run(debug=True, port=5000)