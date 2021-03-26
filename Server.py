from flask import Flask, render_template
from flask import request
from flask_cors import CORS, cross_origin
from Blockchain import Blockchain

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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
        return bc.verifyblock(int(data.get("proof")))
    else:
        return "Could not verify block"

@app.route('/transactions', methods = ["GET"])
def printTransaction():
    return bc.viewpendingtransactions()

@app.route('/transactions/new', methods = ["POST"])
def addtransaction():
    if request.method == 'POST':
        data = request.form
        bc.addtransaction(data.get("from"), data.get("to"), data.get("amount"))
        return "ADDED transaction"
    else:
        return "Cannot add transaction"

if __name__ == '__main__':
    app.run()

