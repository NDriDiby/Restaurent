// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart");
var ingredients = document.querySelectorAll("input");

let custChoice = [];
var my_choice;
var give_me;

for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function () {
    var itemId = this.dataset.product;
    var action = this.dataset.action;

    for (let i = 1; i < ingredients.length; i++) {
      if (ingredients[i].checked === true) {
        custChoice.push(ingredients[i].value);
        //console.log(custChoice.toString())
      }
    }

    console.log("fromOrdePage:", my_choice);

    if (user === "AnonymousUser") {
      console.log("not logged in");
    } else {
      localStorage.setItem("choice", custChoice);
      my_choice = localStorage.getItem("choice");
      var orderItem = give_me;
      updateUserOrder(itemId, action, custChoice.toString(), orderItem);
      location.reload();

      // console.log(custChoice.toString());
      // console.log(my_choice);
    }
  });
}

async function updateUserOrder(itemId, action, custChoice, orderItem) {
  console.log(user, "is logged in, sending data....");

  var url = "/texasgrillz/updateitem/";

  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ itemId: itemId, action: action, choice: custChoice, orderItem: orderItem }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data:", data);
    });
}
