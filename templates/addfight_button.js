async function postData(url = '', data = {}) {
    console.log("URL is " + url + " data is " + JSON.stringify(data))
    // Default options are marked with *
    const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    headers: {
        "Content-type": "application/json; charset=UTF-8"
        // 'Content-Type': 'application/x-www-form-urlencoded',
    },
      
      body: JSON.stringify('{"name": "Marcus"}') // body data type must match "Content-Type" header
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  }
  
