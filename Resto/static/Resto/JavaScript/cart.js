// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart");
var cart_plus = document.getElementById("plus");
var cart_minus = document.getElementById("moin");
for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function () {
    var itemId = this.dataset.product;
    var action = this.dataset.action;

    if (user === "AnonymousUser") {
      console.log("not logged in");
    } else {
      updateUserOrder(itemId, action);
      location.reload();
    }
  });

  console.log("just checking");
}

function updateUserOrder(itemId, action) {
  console.log(user, "is logged in, sengind data....");

  var url = "/texasgrillz/updateitem/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ itemId: itemId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data:", data);
    });
}
