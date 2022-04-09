// Add item to your cart
var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

// Add item to your cart
var updated_but = document.getElementsByClassName("update-cart");
var ingredients = document.querySelectorAll("input");
var form = document.getElementById("choiceOptions");

console.log("CHECKING");

var bag = [];
$("input")
  .not(".cuisson input")
  .click(function () {
    if ($(this).prop("checked")) {
      bag.push($(this).val());
    } else if ($(this).prop("checked", false)) {
      console.log("UNCHECKED", $(this).val());
      delete bag[bag.indexOf($(this).val())];
    }
    console.log(bag);
  });

var cuisson = [];
$(".cuisson input").click(function () {
  $(".cuisson input").not(this).prop("checked", false);
  if (cuisson.length == 0) {
    cuisson.push($(this).val());
  } else {
    cuisson[0] = $(this).val();
  }
});

for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function (e) {
    var custChoice = [];

    e.preventDefault();
    var itemId = this.dataset.product;
    var action = this.dataset.action;
    var ingre = this.dataset.ingredient;

    //Customer ingredient choice
    // for (let i = 1; i < ingredients.length; i++) {
    //   if (ingredients[i].checked === true) {
    //     custChoice.push(ingredients[i].value);
    //   }
    // }

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
        choice: bag.concat(cuisson).toString(),
        //custChoice.toString(),
      },
      dataType: "json",
      success: function (response) {
        orderItem = response.orderItem;
        total_cart = response.total_cart;
        item_name = response.item_name;
        tot_item = response.tot_item;
        console.log(response);
        console.log("THIS MY BAG", bag);

        msg = document.getElementById("message");

        msg.innerHTML = `
        <div class='justify-center items-center gap-x-2 bg-gray-500 mx-2 py-1 rounded-md sm:py-3 sm:mt-24 sm:text-2xl flex'>
          <p class="text-white"><strong>(${response.tot_item}) </strong>${item_name} ajouté(es) a votre table </p>
          <span><i class="bi bi-check-circle text-2xl font-bold text-green-300"></i></span>
        </div>`;

        total_item_box = document.getElementById("total-item");
        $("#cart-total").slideUp(100).slideDown(300);
        total_item_box.innerHTML = total_cart;

        $(".orderTotal-total").html(`My total - <b>${response.total}</b>`);
      },

      error: function (error) {
        console.log(error);
      },
    });
  });
}
