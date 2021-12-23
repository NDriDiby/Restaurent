// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart");
var item_choice = document.getElementById("item_choice").value;

for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function () {
    var itemId = this.dataset.product;
    var action = this.dataset.action;

    if (user === "AnonymousUser") {
      console.log("not logged in");
    } else {
      updateUserOrder(itemId, action, item_choice);
      location.reload();
    }
  });
}

function updateUserOrder(itemId, action, item_choice) {
  console.log(user, "is logged in, sending data....");

  var url = "/texasgrillz/updateitem/";

  fetch(url, {
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
