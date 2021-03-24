import requests
import json
from Transaction import Transaction
from Block import Block
from hashlib import sha256

apiUrl = "http://127.0.0.1:5000"

def getpendingtransactions():
    return requests.get(apiUrl + "/transactions").json()

def getchain():
    return requests.get(apiUrl + "/chain").json()

def getpendingtransactionsPretty():
    jsonStr = requests.get(apiUrl + "/transactions").json()
    return json.dumps(jsonStr, indent=2)

def getchainPretty():
    jsonStr = requests.get(apiUrl + "/chain").json()
    return json.dumps(jsonStr, indent=2)

def postnewtransaction(fromS, to, amount):
    return requests.post(apiUrl + "/transactions/new", data={'from': fromS, 'to': to, 'amount': amount})


def postnewproof(proof):
    return requests.post(apiUrl + "/mine/prove", data={'proof': proof})

def mine():
    transactionsDict = getpendingtransactions()["Pending_transactions"]
    transactions = []
    for t in transactionsDict:
        transaction = Transaction(t["from"], t["to"], t["amount"])
        transactions.append(transaction)

    lastblock = getchain()["Blocks"][0]

    proof = 0
    hash = ""
    while (hash[:4] != "0000"):
        proof += 1
        testBlock = Block(sha256(json.dumps(lastblock,separators=(',', ':')).encode()).hexdigest(), transactions, proof)
        hash = sha256(testBlock.to_json().encode()).hexdigest()

    postnewproof(proof)
    print("Block sent with proof: ", proof)


def main():
    while(1==1):
        userInput = str.lower(input("CLIENT >> "))
        if userInput == "e":
            exit(0)
        elif userInput == "c":
            print(getchainPretty())
        elif userInput == "m":
            mine()
        elif userInput == "t":
            print(getpendingtransactionsPretty())
        elif userInput == "a":
            fromS = input("from? - ")
            to =input("to? - ")
            amount = input("amount? - ")

            postnewtransaction(fromS, to, amount)
            print("Transaction added!")


main()