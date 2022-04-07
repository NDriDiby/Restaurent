// Add item to your cart
var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart");
var ingredients = document.querySelectorAll("input");
var form = document.getElementById("choiceOptions");

for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function (e) {
    var custChoice = [];

    e.preventDefault();
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

    //No ingredient item (choice)
    if (custChoice == undefined) {
      custChoice = " ";
    }

    //From order page (ingredient) - (no choice)
    if (ingre == "None") {
      ingre = " ";
      custChoice = ingre;
    }

    $.ajax({
      url: "/texasgrillz/updateitem/",
      method: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
        itemId: itemId,
        action: action,
        choice: custChoice.toString(),
      },
      dataType: "json",
      success: function (response) {
        orderItem = response.orderItem;
        total_cart = response.total_cart;
        item_name = response.item_name;
        tot_item = response.tot_item;
        console.log(response);

        msg = document.getElementById("message");

        msg.innerHTML = ` <div id="message" class="col-12">
        <div class="alert alert-success alert-dismissible" style="text-align: center" role="alert">
          <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
            <use xlink:href="#check-circle-fill" />
          </svg>
          <p> (${response.tot_item}) ${item_name} ajouté(es) a votre table </p>
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
      </div>`;

        total_item_box = document.getElementById("total-item");
        $("#cart-total").slideUp(100).slideDown(300);
        total_item_box.innerHTML = total_cart;

        $(".orderTotal-total").html(`My total - <b>${response.total}</b> FCFA`);
      },

      error: function (error) {
        console.log(error);
      },
    });
  });
}
