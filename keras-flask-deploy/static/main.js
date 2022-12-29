
//========================================================================
// Main button events
//========================================================================

function submitImage() {
  // action for the submit button
  console.log("submit");
  // call the predict function of the backend
  predictImage();
}

var predResult = document.getElementById("pred-result");

function predict() {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
  })   
   .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          display_res(data);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
});};

/* function wait() {
  fetch("/handle_data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
  })   
   .then(resp => {
      if (resp.ok)
        resp.json().then(msg => {
          display_msg(msg);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
});};
function display_msg(msg){
  document.getElementById('wait').innerHTML = msg.result;
  show(document.getElementById('wait'));
	
}
 */

function display_res(data) {
  // display the result
  predResult.innerHTML = data.result;
  show(predResult);
}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}