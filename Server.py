from flask import Flask
from flask import request
from Blockchain import Blockchain

app = Flask(__name__)

bc = Blockchain()

@app.route('/chain', methods = ["GET"])
def printBlockChain():
    return bc.readchain()

@app.route('/mine/prove', methods = ["POST"])
def verifyBlock():
    if request.method == 'POST':
        data = request.form
        return bc.verifyblock(data.get("proof"))
    else:
        return "Could not verify block"

@app.route('/transactions', methods = ["GET"])
def printTransaction():
    return bc.viewpendingtransactions()

@app.route('/mine/prove', methods = ["POST"])
def addtransaction():
    if request.method == 'POST':
        data = request.form
        return bc.addtransaction(data.get("from"), data.get("to"), data.get("amount"))
    else:
        return "Cannot add transaction"

if __name__ == '__main__':
    app.run()

