
const apiUrl = "http://127.0.0.1:5000";

async function getCurrentChain(url){ 
    response = await fetch(url + "/chain");
    var data = await response.json();
    console.log(data);
}

getCurrentChain(apiUrl);