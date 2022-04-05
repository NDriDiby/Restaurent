// Start here

// send order to the kitchen
var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
var sendOrder = document.getElementsByClassName("send-order");
var process_order = document.getElementById("process_order");
var success_transaction = document.getElementById("success_transaction");
var total_item = null;
var orderItem = null;

//Get total item
function getTotalItem() {
  $.ajax({
    url: "/texasgrillz/sendorder/",
    method: "GET",
    success: function (response) {
      total_item = response.total_item;
      console.log(response);
    },
    error: function (error) {
      console.log(error);
    },
  });
}

getTotalItem();

//send order to the kitchen
for (let i = 0; i < sendOrder.length; i++) {
  sendOrder[i].addEventListener("click", function (e) {
    e.preventDefault();
    var action = this.dataset.action;
    var order = this.dataset.order;

    $.ajax({
      url: "/texasgrillz/sendorder/",
      method: "POST",
      data: { csrfmiddlewaretoken: csrfToken, action: action, order: order },
      dataType: "json",
      success: function (response) {
        $(".basket").fadeOut(); // remove basket
        $(".summary").hide(); // remove summary

        console.log("total Item", total_item);

        if (total_item > 0) {
          // check if there is item in the basket
          process_order.innerHTML = ` 
        <div style='text-align:center'>
        <h1 style ='color:black;font-size:20px'> We're processing your order....</h1>
              <div class='p-3'>
              <div class="spinner-grow text-muted"></div>
              <div class="spinner-grow text-primary"></div>
              <div class="spinner-grow text-success"></div>
              <div class="spinner-grow text-info"></div>
              <div class="spinner-grow text-warning"></div>
              <div class="spinner-grow text-danger"></div>
              <div class="spinner-grow text-secondary"></div>
            <div>
        </div>`;

          setInterval(function () {
            $("#process_order").hide();
            success_transaction.innerHTML = `
          <div id="message" class="col-12">
            <div class="alert alert-success alert-dismissible" style="text-align: center" role="alert">
              <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
                <use xlink:href="#check-circle-fill" />
              </svg>
              <h4 style="color:black"> <b> Votre commande a ete bien recu par notre cuisine! </b></h4>
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
          </div>`;
          }, 3000);
        } else {
          //show succes messages
          success_transaction.innerHTML = ` 
          <div id="message" class="col-12">
            <div class="alert alert-warning alert-dismissible" style="text-align: center" role="alert">
              <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
                <use xlink:href="#check-circle-fill" />
              </svg>
              <h4 style="color:black"> <b> Votre pannier est vide! </b></h4>
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
          </div>`;
        }
      },

      error: function (error) {
        console.log(error);
      },
    });
  });
}

//UPDATE (INC - DEC) ITEM IN CART
update_but = document.getElementsByClassName("update-cart");
for (let i = 0; i < update_but.length; i++) {
  update_but[i].addEventListener("click", function (e) {
    e.preventDefault();

    var itemId = this.dataset.product;
    var action = this.dataset.action;
    var ingre = this.dataset.ingredient;
    var ordItem = this.dataset.orderItem;

    $.ajax({
      url: "/texasgrillz/updateitem/",
      method: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
        itemId: itemId,
        action: action,
        choice: ingre,
        ordItem: ordItem,
      },
      success: function (response) {
        orderItem = response.orderItem;

        active_item = null;

        for (var ord in orderItem) {
          var total_item = document.getElementsByClassName("quantity-field")[ord];
          var product_details = document.getElementsByClassName("product-details")[ord];
          var item_total = document.getElementsByClassName("subtotals")[ord];

          product_details.innerHTML = `<p id=item-quantity-${orderItem[ord]["orderItem_id"]} data-orderItem=${orderItem[ord]["orderItem_id"]}>
            <strong><span class="item-quantity">${orderItem[ord]["quantity"]}</span>-${orderItem[ord]["item"]}</strong>
          </p>
          <h1><strong>${orderItem[ord]["description"]}</strong></h1>
          <h1 class="mt-1" style="color: rgb(209, 112, 131)"><strong>${orderItem[ord]["ingredient"]}</strong></h1> `;

          total_item.value = orderItem[ord]["quantity"];
          item_total.innerHTML = `${orderItem[ord]["total"]} FCFA`;
        }
        $(`#item-quantity-${response.active_orderItem}`).slideUp(0).slideDown(500);
        $(`#item-quantity-${response.active_orderItem}`).css({ color: "green" });

        //GET THE VARIABLE
        prod_details = document.getElementById("item-quantity");
        tot_cart = document.getElementById("summary-total-items");
        subtotal = document.getElementById("basket-subtotal");
        total = document.getElementById("basket-total");
        item_total = document.getElementById("item-subtotal");

        //UPDATE THE VALUE
        total_cart = response.total_cart;
        total.innerHTML = `${response.total} FCFA`;
        subtotal.innerHTML = `${response.total} FCFA`;
        tot_cart.innerHTML = `<span class="total-items"></span> Menu dans votre panier (${total_cart}) `;
      },
    });
  });
}

// End here
