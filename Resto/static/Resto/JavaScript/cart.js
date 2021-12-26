// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart");
var ingredient = document.getElementByClassName("ingredients");
var seasoning = document.getElementsByClassName("seasoning");
var cuisson = document.getElementsByClassName("cuisson");

for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function () {
    var itemId = this.dataset.product;
    var action = this.dataset.action;

    console.log("Ingredients:");
    for (var checkbox of ingredient) {
      if (checkbox.checked) console.log(checkbox.value);
    }

    if (user === "AnonymousUser") {
      console.log("not logged in");
    } else {
      updateUserOrder(itemId, action);
      location.reload();
    }
  });
}

async function updateUserOrder(itemId, action) {
  console.log(user, "is logged in, sending data....");

  var url = "/texasgrillz/updateitem/";

  await fetch(url, {
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
