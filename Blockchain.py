import json
import rsa
from rsa import VerificationError

from Block import Block
from Transaction import Transaction
from hashlib import sha256


class Blockchain:

    def __init__(self):
        self.currBlock = Block(0, [], 0)
        self.firstBlock = self.currBlock
        self.pendingTransactions = []
        self.blocks = {}
        self.balances = {}
        self.calculateBalances()

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
        return json.dumps(blocksDict,separators=(',', ':'), indent=2)

    def viewpendingtransactions(self):
        transactionslist = []
        for item in self.pendingTransactions:
            transactionslist.append(item.to_dict())
        transactions = {"Pending_transactions": transactionslist}
        return json.dumps(transactions,separators=(',', ':'), indent=2)

    def addtransaction(self, to, amount, signature, publicKeyN):
        if publicKeyN not in self.balances:
            self.balances[publicKeyN] = 0
        if to not in self.balances:
            self.balances[to] = 0
        if self.balances[publicKeyN] < int(amount):
            print("Inadequate payment attempt")
            return False
        self.balances[publicKeyN] -= int(amount)
        publicKey = rsa.PublicKey(int(publicKeyN, base=16), 65537)
        message = (publicKeyN + to + amount).encode('utf8')
        try:
            rsa.verify(message, bytes.fromhex(signature), publicKey)
        except VerificationError:
            print("False signature attempt")
            return False
        transaction_to_add = Transaction(publicKeyN, to, amount)
        self.pendingTransactions.append(transaction_to_add)
        return True

    def removetransactions(self):
        self.pendingTransactions.clear()

    def verifyblock(self, proof, publicKeyN):
        if publicKeyN not in self.balances:
            self.balances[publicKeyN] = 0
        if len(self.pendingTransactions) == 0:
            print("Nothing to mine")
            return "NO TRANSACTIONS TO MINE"
        transactions = []
        for t in self.pendingTransactions:
            transactions.append(t)
        transactions.append(Transaction("0", publicKeyN, 1))
        newBlock = Block(sha256(self.currBlock.to_json().encode()).hexdigest(), transactions, proof)
        hash = sha256(newBlock.to_json().encode()).hexdigest()
        if hash[:4] == "0000":
            self.addblock(newBlock)
            self.removetransactions()
            self.calculateBalances()
            return "BLOCK MINED SUCCESSFULLY"
        else:
            print("INVALID BLOCK")
            return "INVALID BLOCK - MINE FAILED"


    def calculateBalances(self):
        readBlock = self.currBlock
        for key in self.balances.keys():
            self.balances[key] = 0
        while readBlock != self.firstBlock:
            for t in readBlock.transactions:
                if t.source != '0':
                    self.balances[t.source] -= int(t.amount)
                self.balances[t.destination] += int(t.amount)
            readBlock = self.blocks[readBlock.prev_hash]
        balancesDict = {}
        balanceNameList = []
        for key in self.balances.keys():
            accountDict = {}
            accountDict['user'] = key
            accountDict['balance'] = self.balances[key]
            balanceNameList.append(accountDict)
        balancesDict["Balances"] = balanceNameList
        self.jsonBalString = json.dumps(balancesDict,separators=(',', ':'), indent=2)

    def jsonBalances(self):
        return self.jsonBalString

    def getBalance(self, publicKeyN):
        balanceDict = {}
        balanceDict["Balance"] = self.balances[publicKeyN]
        return json.dumps(balanceDict,separators=(',', ':'), indent=2)