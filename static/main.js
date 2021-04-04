
const apiUrl = "http://127.0.0.1:5000";

function htmlToElement(html) {
	var template = document.createElement('template');
	html = html.trim();
	template.innerHTML = html;
	return template.content.firstChild;
}

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

async function getCurrentChain(url){ 
    response = await fetch(url + "/chain");
    var data = await response.json();
    var blocks = data.Blocks;

    const container = document.querySelector("#chainDiv");
	const newList = htmlToElement('<div id="blocklist"></div>');

    for(let i = 0; i < blocks.length; i++){
        const newBlock = createBlock(blocks[i]);
        const transactionsList = blocks[i].transactions;
        const table = createTransactionTable();
        for(let j = 0; j < transactionsList.length; j++){
            const newTrans = createTransaction(transactionsList[j]);
            table.append(newTrans);
        }
        newBlock.append(table);
        newBlock.style.backgroundColor = "rgb("+Math.floor(Math.random() * 255)+","+Math.floor(Math.random() * 255)+","+Math.floor(Math.random() * 255)+",0.4)";
        const newChainLink = createLink();
        newList.appendChild(newChainLink);
        newList.appendChild(newBlock);
    }

    const oldList = document.querySelector("#blocklist");
	container.appendChild(oldList);
	oldList.removeAttribute("id");
	oldList.hidden = true;

	oldList.parentElement.appendChild(newList);
}

createBlock = (block) => {
    return htmlToElement(`
    <div class = 'block'>
    <h2 class = 'proof'>Proof: ${block.proof}</h2>
    <h4 class = 'prevHash'>Previous Hash: ${block.prevHash}</h2>

    </div>`);
}

createTransactionTable = () => {
    return htmlToElement(`<table>
        <tr>
        <th>From</th>
        <th>To</th>
        <th>Amount</th>
        <tr>
    </table>`)
}

createTransaction = (t) => {
    return htmlToElement(`
        <tr>
        <td>${t.from}</th>
        <td>${t.to}</th>
        <td>${t.amount}</th>
        <tr>`)
}

createLink = () => {
    return htmlToElement(`<div class = 'chainlink'><i class='fas fa-link'></i></div>`)
}

createBalanceTable = () => {
    return htmlToElement(`<table>
        <tr>
        <th>User</th>
        <th>Balance</th>
        <tr>
    </table>`)
}

createBalance = (b) => {
    return htmlToElement(`
        <tr>
        <td>${b.user}</th>
        <td>${b.balance}</th>
        <tr>`)
}

async function getBalances(url){
    response = await fetch(url + "/balances");
    var data = await response.json();
    var bals = data.Balances;

    const container = document.querySelector("#balancesDiv");
	const newList = htmlToElement('<div id="balancesList"></div>');
    const table = createBalanceTable();
    for(let j = 0; j < bals.length; j++){
        const newBal = createBalance(bals[j]);
        table.append(newBal);
    }
    newList.append(table);
    const oldList = document.querySelector("#balancesList");
	container.appendChild(oldList);
	oldList.removeAttribute("id");
	oldList.hidden = true;

	oldList.parentElement.appendChild(newList);
}

async function getPendingTransactions(url){
    response = await fetch(url + "/transactions");
    var data = await response.json();
    var pending = data.Pending_transactions;

    const container = document.querySelector("#transactionDiv");
	const newList = htmlToElement('<div id="transactionsList"></div>');
    const table = createTransactionTable();
    for(let j = 0; j < pending.length; j++){
        const newTrans = createTransaction(pending[j]);
        table.append(newTrans);
    }
    newList.append(table);
    const oldList = document.querySelector("#transactionsList");
	container.appendChild(oldList);
	oldList.removeAttribute("id");
	oldList.hidden = true;

	oldList.parentElement.appendChild(newList);
}

async function getPersonalBalance(url){
    response = await fetch(url + "/transactions/");
    var data = await response.json();
    var balance = data.Balance;

    document.querySelector("#balance").innerHTML = "Your Balance - " + balance;
}

initPage = () => {
    getCurrentChain(apiUrl);
    getPendingTransactions(apiUrl);
    getBalances(apiUrl);
    getPersonalBalance(apiUrl);
}

initPage();