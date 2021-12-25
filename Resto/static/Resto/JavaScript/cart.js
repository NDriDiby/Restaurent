// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart");
var item_choice = document.getElementById("item_choice");
var choice = document.getElementsByClassName("cust_choice");

// console.log("myChoice");
// if (choice.value != null) {
//   for (var j = 0; j < choice.length; j++) {
//     choice[j].addEventListener("click", function () {
//       console.log("myVChoice", choice[j]);
//     });
//   }
// } else {
//   choice = null;
// }

for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function () {
    var itemId = this.dataset.product;
    var action = this.dataset.action;

    if (item_choice != null) {
      var cust_choice = item_choice.value;
      if (user === "AnonymousUser") {
        console.log("not logged in");
      } else {
        updateUserOrder(itemId, action, cust_choice);
        location.reload();
      }
    } else {
      var cust_choice = null;
      updateUserOrder(itemId, action, cust_choice);
      location.reload();
    }
  });
}

async function updateUserOrder(itemId, action, item_choice) {
  console.log(user, "is logged in, sending data....");

  var url = "/texasgrillz/updateitem/";

  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ itemId: itemId, action: action, item_choice: item_choice }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data:", data);
    });
}
