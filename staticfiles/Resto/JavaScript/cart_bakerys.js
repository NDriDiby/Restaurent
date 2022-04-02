// Add item to your cart
var updated_but = document.getElementsByClassName("update-cartBakerys");
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
}

function updateUserOrder(itemId, action) {
  console.log(user, "is logged in, sengind data....");

  var url = "/bakerys/updateitem/";

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
