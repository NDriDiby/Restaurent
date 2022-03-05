// // send order to the kitchen
var sendOrder = document.getElementsByClassName("send-order");
// var cust_note = document.getElementById("customer_note");

for (let i = 0; i < sendOrder.length; i++) {
  sendOrder[i].addEventListener("click", function () {
    var action = this.dataset.action;
    var order = this.dataset.order;
    cuisine(action, order);
  });
}

function cuisine(act, ord) {
  var url = "/texasgrillz/sendorder/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ action: act, order: ord }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data:", data);
    });
}
