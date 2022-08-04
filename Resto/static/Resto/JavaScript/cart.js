// Add item to your cart
var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

// Add item to your cart
var form = $("#item-details-form");
var updated_but = document.getElementsByClassName("update-cart");
var ingredients = document.getElementsByClassName("ingredient-input");
var accompagnement = document.getElementsByClassName("accompagement");
var supplement = document.getElementsByClassName("supplement-input");

//Accompagement
$(".accompagement").on("click", function () {
  $(this).toggleClass("active");
});

//Cuisson
var cuisson;
$(".cuisson input").click(function () {
  $(".cuisson input").not(this).prop("checked", false);

  cuisson = $(this).val();
  console.log(cuisson);
});

for (var i = 0; i < updated_but.length; i++) {
  updated_but[i].addEventListener("click", function (e) {
    var custChoice = [];
    var accomp_id = [];
    var supplements = [];
    msg = document.getElementById("message");

    e.preventDefault();
    var itemId = this.dataset.product;
    var side_itemId = this.dataset.product_side;
    var action = this.dataset.action;
    var ingre = this.dataset.ingredient;

    if (cuisson) {
    }

    for (let i = 0; i < accompagnement.length; i++) {
      if (accompagnement[i].className == "accompagement active") {
        accomp_id.push(accompagnement[i].dataset.accomp_name);
      }
    }

    //Customer ingredient choice
    for (let i = 0; i < ingredients.length; i++) {
      if (ingredients[i].checked === true) {
        custChoice.push(ingredients[i].value);
      }
    }

    //Customer supplement choice
    for (let i = 0; i < supplement.length; i++) {
      if (supplement[i].checked === true) {
        supplements.push(supplement[i].value);
        console.log(supplement[i].value);
      }
    }
    console.log(supplements);

    // GET TABLE NUMBER
    table = location.href.split("&")[1].split("=")[1];

    // DATA TO PROCESS
    if (side_itemId) {
      data = {
        csrfmiddlewaretoken: csrfToken,
        side_itemId: side_itemId,
        action: action,
        table: table,
      };
    } else {
      data = {
        csrfmiddlewaretoken: csrfToken,
        itemId: itemId,
        action: action,
        choice: custChoice.toString(),
        accomp: accomp_id.toString(),
        sup: supplements.toString(),
        table: table,
      };
    }

    $.ajax({
      url: "/texasgrillz/updateitem/",
      method: "POST",
      data: data,
      dataType: "json",
      success: function (response) {
        orderItem = response.orderItem;
        total_cart = response.total_cart;
        item_name = response.item_name;
        tot_item = response.tot_item;

        console.log(response);

        var old_total = document.getElementById("orderTotal-total").innerText;
        old_total = parseInt(old_total.split("FCFA")[0]);

        item_price = parseInt(document.getElementById("item-price").innerText);
        var new_total = response.total;

        msg.innerHTML = `
        <div class='justify-center text-sm w-full items-center bg-gray-500 px-2 mx-2 py-1 rounded-md sm:py-3 sm:mt-24 sm:text-2xl flex'>
          <p class="text-white pr-1"><strong>(${tot_item}) </strong>${item_name} ajouté(es) a votre table </p>
          <span><i class="bi bi-check-circle text-xl font-bold text-green-300"></i></span>
        </div>`;

        total_item_box = document.getElementById("total-item");
        $("#cart-total").slideUp(100).slideDown(300);
        $("#message").show();
        total_item_box.innerHTML = total_cart;

        $("#message").delay(3000).fadeOut("slow");

        count = old_total;

        let counting = setInterval(countUp, 10);

        function countUp() {
          count = count + 50;

          if (count == new_total) {
            clearInterval(counting);
          }
          $(".orderTotal-total").html(`<b style="color:green;font-size:25px" >${count} FCFA</b>`);
        }

        document.getElementById("orderTotal-total").innerText = new_total;

        // Reset Form
        form[0].reset();
        $(".accompagement").removeClass("active");
      },

      error: function (error) {
        console.log(error);
      },
    });
  });
}
