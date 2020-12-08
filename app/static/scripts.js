const getReccs = (e) => {

    const form = document.querySelector('form')
    console.log(form)
    const formInputs = Object.values(form).reduce((obj,field) => { obj[field.name] = field.value; return obj }, {})
    console.log(formInputs)
    const reqParams = new URLSearchParams();

    Object.keys(formInputs).map(function(key, index) {
      if(key && formInputs[key]){
        reqParams.set(key, formInputs[key]);
      }
    });

    const target = `./api/recommender/v1/get_recc?${reqParams.toString()}`;
    console.log(target)
    console.log(reqParams.toString());
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.status === 200 && this.readyState === 4) {
          renderReccs(JSON.parse(this.responseText)['products'])
        }
        else if (this.status === 400 && this.readyState === 4){
          showError(JSON.parse(this.responseText)['err'])
        }

    };
    xhttp.open("GET", target, true);
    xhttp.send();
}

const renderReccs = (reccList) => {
    // make result area visible
    const resultsArea = document.querySelector('#results')
    resultsArea.className = ""

    // set the appropriate heading
    document.querySelector('#res-heading').innerHTML = "Recommended Products"

    // clear any error messages
    document.querySelector('#err-msg').innerHTML = ""

    const prodList = document.querySelector('#prod-list')

    //empty the list otherwise we'll just be appending to the list with every recommendation instead of refreshing
    prodList.innerHTML = "";

    // add all the node items to it
    reccList.map((item) => {
        const node = document.createElement("LI");                 // Create a <li> node
        const textnode = document.createTextNode(item);         // Create a text node
        node.appendChild(textnode);
        prodList.appendChild(node)
    })
}

const showError = (errMsg) => {
    // make result area visible
    const resultsArea = document.querySelector('#results')
    resultsArea.className = ""

    // set the appropriate heading
    document.querySelector('#res-heading').innerHTML = "Error: Cannot recommend products"

    // empty any previous reccs
    document.querySelector('#prod-list').innerHTML = "";

    // render the error message
    document.querySelector('#err-msg').innerHTML = `${errMsg}`

}