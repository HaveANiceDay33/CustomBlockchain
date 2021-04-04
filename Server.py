import pickle
from flask import Flask, render_template
from flask import request
from flask_cors import CORS, cross_origin
from Blockchain import Blockchain

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
try:
    bc = pickle.load(open("blockchain.pickle", "rb"))
except (OSError, IOError):
    print("No blockchain found on disk. Creating new blockchain")
    bc = Blockchain()


@app.route('/')
@cross_origin()
def displayPage():
    return render_template("index.html")

@app.route('/chain', methods = ["GET"])
def printBlockChain():
    return bc.readchain()

@app.route('/mine/prove', methods = ["POST"])
def verifyBlock():
    if request.method == 'POST':
        data = request.form
        result = bc.verifyblock(int(data.get("proof")), data.get("publicKeyN"))
        pickle.dump(bc, open("blockchain.pickle", "wb"))
        return result
    else:
        return "Could not verify block"

@app.route('/transactions', methods = ["GET"])
def printTransaction():
    return bc.viewpendingtransactions()

@app.route('/transactions/new', methods = ["POST"])
def addtransaction():
    if request.method == 'POST':
        data = request.form
        if(bc.addtransaction(data.get("to"), data.get("amount"), data.get("signature"),
                          data.get("publicKeyN"))):
            pickle.dump(bc, open("blockchain.pickle", "wb"))
            return "ADDED transaction"
        else:
            return "Invalid signature"
    else:
        return "Cannot add transaction"

@app.route('/balances', methods = ["GET"])
def getBalances():
    return bc.calculateBalances()

if __name__ == '__main__':
    app.run()

