import json
# import flask
from hashlib import sha256
from Transaction import Transaction
from Block import Block
from Blockchain import Blockchain

### TEST CODE ONLY ###
### RUN CLIENT/SERVER FOR ACTUAL USE ###

# transaction
# block
# proof method
# hashing
# server communications

def main():
    # trans = []
    # trans.append(Transaction("A", "B", 10))
    # trans.append(Transaction("A", "C", 10))
    # trans.append(Transaction("D", "B", 10))
    # trans.append(Transaction("A", "B", 11))
    #
    # b = Block(0, trans, 33)
    # c = Block(1, trans[0:1], 45)

    bc = Blockchain()

    bc.addtransaction("A", "C", 82)
    bc.addtransaction("B", "C", 12)
    bc.addtransaction("A", "D", 43)

    mine(bc)

    bc.addtransaction("A", "C", 2)
    bc.addtransaction("A", "B", 675)

    mine(bc)

    print(bc.readchain())


def mine(bc):
    transactionsString = bc.viewpendingtransactions()
    transactionsDict = json.loads(transactionsString)
    transactions = []
    for t in transactionsDict["Pending_transactions"]:
        transaction = Transaction(t["from"], t["to"], t["amount"])
        transactions.append(transaction)

    lastblock = json.loads(bc.readchain())["Blocks"][0]
    proof = 0
    hash = ""
    while (hash[:4] != "0000"):
        proof += 1
        testBlock = Block(sha256(json.dumps(lastblock).encode()).hexdigest(), transactions, proof)
        hash = sha256(testBlock.to_json().encode()).hexdigest()
        #print(hash, proof)

    bc.verifyblock(proof)


main()
