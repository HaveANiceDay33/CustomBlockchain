from hashlib import sha256
import json
import Transaction


class Block:

    def __init__(self, prev_hash, transactions, proof):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.proof = proof

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_transactions = []
        for t in self.transactions:
            json_transactions.append(t.to_dict())
        json_transactions = sorted(json_transactions, key=lambda i: (i["from"], i["to"], i["amount"]))
        b = {
            "prevHash": self.prev_hash,
            "transactions": json_transactions,
            "proof": self.proof
        }
        return b
