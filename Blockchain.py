import json
from Block import Block
from Transaction import Transaction
from hashlib import sha256


class Blockchain:

    def __init__(self):
        self.currBlock = Block(0, [], 0)
        self.firstBlock = self.currBlock
        self.pendingTransactions = []
        self.blocks = {}

    def addblock(self, block):
        self.blocks[block.prev_hash] = self.currBlock
        self.currBlock = block


    def readchain(self):
        readBlock = self.currBlock
        chainedblocks = []

        while readBlock != self.firstBlock:
            chainedblocks.append(readBlock.to_dict())
            readBlock = self.blocks[readBlock.prev_hash]
        chainedblocks.append(self.firstBlock.to_dict())
        blocksDict = {"Blocks": chainedblocks}
        return json.dumps(blocksDict,separators=(',', ':'))

    def viewpendingtransactions(self):
        transactionslist = []
        for item in self.pendingTransactions:
            transactionslist.append(item.to_dict())
        transactions = {"Pending_transactions": transactionslist}
        return json.dumps(transactions,separators=(',', ':'))

    def addtransaction(self, fromS, to, amount):
        transaction_to_add = Transaction(fromS, to, amount)
        self.pendingTransactions.append(transaction_to_add)

    def removetransactions(self):
        self.pendingTransactions.clear()

    def verifyblock(self, proof):
        transactions = []
        for t in self.pendingTransactions:
            transactions.append(t)

        newBlock = Block(sha256(self.currBlock.to_json().encode()).hexdigest(), transactions, proof)
        hash = sha256(newBlock.to_json().encode()).hexdigest()
        if hash[:4] == "0000":
            self.addblock(newBlock)
            self.removetransactions()
            return "VALID"
        else:
            print("INVALID BLOCK")
            return "INVALID"
