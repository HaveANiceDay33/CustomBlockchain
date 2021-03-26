import requests
import json
import rsa
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

def postnewtransaction(fromS, to, amount, signature):
    return requests.post(apiUrl + "/transactions/new", data={'from': fromS, 'to': to, 'amount': amount, 'signature': signature})


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

def addTransaction(publicKey, privateKey):
    fromS = input("from? - ")
    to =input("to? - ")
    amount = input("amount? - ")

    message = (fromS+to+amount).encode()
    hashed = rsa.compute_hash(message, 'SHA-1')
    signature = rsa.sign_hash(hashed, privateKey, 'SHA-1')
    postnewtransaction(fromS, to, amount, signature)
    print("Transaction added!")

def main():
    #TODO: Add loading of keys from disk
    publicKey = None
    privateKey = None
    hasKeys = False
    if(hasKeys == False):
        print("No key pair found. Generating new key pair...")
        (publicKey, privateKey) = rsa.newkeys(2048)
        print("New key pair generated.")
        #TODO: Save keys to disk
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
            addTransaction(publicKey, privateKey)


main()