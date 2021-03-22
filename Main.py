import json
#import flask
from hashlib import sha256
from Transaction import Transaction
from Block import Block

#transaction
#block
#proof method
#hashing
#server communications

def main():

    trans = []
    trans.append(Transaction("A", "B", 10))
    trans.append(Transaction("B", "C", 20))

    b = Block(0, trans, 33)

    print(b.to_json())

main()