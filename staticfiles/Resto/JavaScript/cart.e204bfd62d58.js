// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart");
var ingredients = document.querySelectorAll("input");

let custChoice = [];

for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function () {
    var itemId = this.dataset.product;
    var action = this.dataset.action;
    var ingre = this.dataset.ingredient;

    //Customer ingredient choice
    for (let i = 1; i < ingredients.length; i++) {
      if (ingredients[i].checked === true) {
        custChoice.push(ingredients[i].value);
      }
    }

    //From order page (ingredient)
    if (custChoice[0] == null) {
      custChoice = ingre;
    }

    if (user === "AnonymousUser") {
      console.log("not logged in");
    } else {
      updateUserOrder(itemId, action, custChoice.toString());
      location.reload();
    }
  });
}

async function updateUserOrder(itemId, action, custChoice) {
  console.log(user, "is logged in, sending data....");

  var url = "/texasgrillz/updateitem/";

  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ itemId: itemId, action: action, choice: custChoice }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data:", data);
    });
}
