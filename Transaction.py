import json


class Transaction:

    def __init__(self, source, destination, amount):
        self.source = source
        self.destination = destination
        self.amount = amount

    def to_json(self):
        return json.dumps(self.to_dict(),separators=(',', ':'))

    def to_dict(self):
        t = {
            "from": self.source,
            "to": self.destination,
            "amount": self.amount
        }
        return t
