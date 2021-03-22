import json
#import flask
from hashlib import sha256
from Transaction import Transaction
from Block import Block
from Blockchain import Blockchain

#transaction
#block
#proof method
#hashing
#server communications

def main():

    trans = []
    trans.append(Transaction("A", "B", 10))
    trans.append(Transaction("A", "C", 10))
    trans.append(Transaction("D", "B", 10))
    trans.append(Transaction("A", "B", 11))

    b = Block(0, trans, 33)
    c = Block(1, trans[0:1], 45)

    bc = Blockchain()

    bc.addtransaction("A", "C", 82)
    bc.addtransaction("B", "C", 12)
    bc.addtransaction("A", "D", 43)


    bc.addblock(b)
    bc.addblock(c)

    mine(bc)
    #bc.readchain()

    #print(b.to_json())

def mine(bc):
    transactions = bc.viewpendingtransactions()
    lastblock = json.loads(bc.readchain())["Blocks"][0]
    proof = 0
    hash = ""
    while(hash[0:3] != "0000"):
        testBlock = Block(sha256(json.dumps(lastblock).encode()).hexdigest(), transactions, proof)
        hash = sha256(testBlock.to_json().encode()).hexdigest()
        proof += 1

    bc.verifyblock(testBlock)
main()