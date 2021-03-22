from CustomBlockchain.Block import Block


class Blockchain:

    def __init__(self):
        self.currBlock = Block(0, [], 0)
        self.pendingTransactions = []


    def addblock(self, block):
        self