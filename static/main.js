
const apiUrl = "http://127.0.0.1:5000";

function htmlToElement(html) {
	var template = document.createElement('template');
	html = html.trim();
	template.innerHTML = html;
	return template.content.firstChild;
}

async function getCurrentChain(url){ 
    response = await fetch(url + "/chain");
    var data = await response.json();
    var blocks = data.Blocks;

    const container = document.querySelector("#chainDiv");
	const newList = htmlToElement('<div id="blocklist"></div>');

    for(let i = 0; i < blocks.length; i++){
        const newBlock = createBlock(blocks[i]);
        newList.appendChild(newBlock);
    }

    const oldList = document.querySelector("#blocklist");
	container.appendChild(oldList);
	oldList.removeAttribute("id");
	oldList.hidden = true;

	oldList.parentElement.appendChild(newList);
}

createBlock = (block) => {
    return htmlToElement(`<div class = 'block'>
    <h2 class = 'proof'>Proof: ${block.proof}</h2>
    
    </div>`);
}

createPendingTransaction = (transaction) => {
    return htmlToElement(`<div class = 'pendingTransaction'>
    <h2 class = 'transaction'>${transaction.from}   ${transaction.amount}-> ${transaction.to}</h2>
    
    </div>`)
}

async function getPendingTransactions(url){
    response = await fetch(url + "/transactions");
    var data = await response.json();
    var pending = data.Pending_transactions;

    const container = document.querySelector("#transactionDiv");
	const newList = htmlToElement('<div id="transactionsList"></div>');

    for(let i = 0; i < pending.length; i++){
        const newPend = createPendingTransaction(pending[i]);
        newList.appendChild(newPend);
    }

    const oldList = document.querySelector("#transactionsList");
	container.appendChild(oldList);
	oldList.removeAttribute("id");
	oldList.hidden = true;

	oldList.parentElement.appendChild(newList);
}

initPage = () => {
    getCurrentChain(apiUrl);
    getPendingTransactions(apiUrl);
}

initPage();