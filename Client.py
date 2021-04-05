import requests
import json
import rsa
import pickle
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

def postnewtransaction(to, amount, signature, publicKey):
    return requests.post(apiUrl + "/transactions/new", data={'to': to, 'amount': amount,
                                                             'signature': signature, 'publicKeyN': hex(publicKey.n)})

def postnewproof(proof, publicKey):
    return requests.post(apiUrl + "/mine/prove", data={'proof': proof, 'publicKeyN': hex(publicKey.n)})

def mine(publicKey):
    transactionsDict = getpendingtransactions()["Pending_transactions"]
    transactions = []
    for t in transactionsDict:
        transaction = Transaction(t["from"], t["to"], t["amount"])
        transactions.append(transaction)

    transaction = Transaction("0", hex(publicKey.n), 1)
    transactions.append(transaction)
    lastblock = getchain()["Blocks"][0]

    proof = 0
    hash = ""
    while (hash[:4] != "0000"):
        proof += 1
        testBlock = Block(sha256(json.dumps(lastblock,separators=(',', ':')).encode()).hexdigest(), transactions, proof)
        hash = sha256(testBlock.to_json().encode()).hexdigest()

    success = postnewproof(proof, publicKey)
    print("Block sent with proof: ", proof)
    print(success.content.decode())

def addTransaction(publicKey, privateKey):
    to = input("to? - ")
    amount = input("amount? - ")

    message = (hex(publicKey.n)+to+amount).encode('utf8')
    hashed = rsa.compute_hash(message, 'SHA-256')
    signature = rsa.sign_hash(hashed, privateKey, 'SHA-256').hex()
    success = postnewtransaction(to, amount, signature.encode(), publicKey)
    print(success.content.decode())

def generateKeys():
    print("Generating new key pair...")
    keys = rsa.newkeys(512, exponent=65537)
    print("New key pair generated. Your public key is")
    print(hex(keys[0].n))
    pickle.dump(keys[0], open("publicKey.pickle", "wb"))
    pickle.dump(keys[1], open("privateKey.pickle", "wb"))
    return keys

def mineBad(publicKey):
    print("Submit invalid proof")
    proof = input("proof? - ")
    postnewproof(proof, publicKey)

def addTransactionBad():
    print("Submit invalid transaction")
    publicKeyN = input("from? - ")
    to = input("to? - ")
    amount = input("amount? - ")
    signature = input("signature? - ")
    postnewtransaction(to, amount, bytes(int(signature)).hex().encode(), rsa.PublicKey(int(publicKeyN, base=16), 65537))

def getBalance():
    userPK = pickle.load(open("publicKey.pickle", "rb"));
    return requests.get(apiUrl + "/balances/personal/"+str(hex(userPK.n))).json()

def main():
    try:
        publicKey = pickle.load(open("publicKey.pickle", "rb"))
        privateKey = pickle.load(open("privateKey.pickle", "rb"))
    except (OSError, IOError):
        print("No key pair found.")
        (publicKey, privateKey) = generateKeys()
    while(1==1):
        userInput = str.lower(input("CLIENT >> "))
        if userInput == "e":
            exit(0)
        elif userInput == "c":
            print(getchainPretty())
        elif userInput == "m":
            mine(publicKey)
        elif userInput == "t":
            print(getpendingtransactionsPretty())
        elif userInput == "a":
            addTransaction(publicKey, privateKey)
        elif userInput == "k":
            (publicKey, privateKey) = generateKeys()
        elif userInput == "y":
            mineBad(publicKey)
        elif userInput == "z":
            addTransactionBad()
        elif userInput == "b":
            print("Current Balance: " + str(getBalance()["Balance"]))
        else:
            print("Invalid Command")


main()