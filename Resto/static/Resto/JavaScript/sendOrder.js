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

      // if (total_item == 0) {
      //   Swal.fire({
      //     icon: "warning",
      //     title: "There is no item in your cart",
      //     showConfirmButton: false,
      //     timer: 1500,
      //   });
      //   setTimeout(() => {
      //     menu = location.href.replace("myorder/", "");
      //     location.href = menu;
      //   }, 1300);
      // }
    },
    error: function (error) {
      console.log(error);
    },
  });
}

var total_order_item = getTotalItem();
total_order_item;

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

      beforeSend: function () {
        $("#spinner-div").show();
      },

      success: function (response) {
        console.log("total Item:", total_item);

        if (total_item > 0) {
          console.log("I can send your order");

          Swal.fire({
            icon: "success",
            title: "Nous avons bien reçu votre commande",
            showConfirmButton: false,
            timer: 3000,
          }).then(() => {
            menu = location.href.replace("myorder/", "");
            location.href = menu;
          });
        }
      },

      complete: function () {
        $("#spinner-div").hide(); //Request is complete so hide spinner
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
    var ordItem = this.dataset.orderItemID;
    var accompa = this.dataset.accomp;

    // var accompa = document.getElementsByClassName("accompa");
    // console.log(accompa);

    $.ajax({
      url: "/texasgrillz/updateitem/",
      method: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
        itemId: itemId,
        action: action,
        choice: ingre,
        accomp: accompa,
      },
      success: function (response) {
        orderItem = response.orderItem;
        active_item = null;

        // console.log("SET ITEM", orderItem[ord]["quantity"]);

        for (var ord in orderItem) {
          var total_item = document.getElementsByClassName("quantity-field")[ord];
          var item_total_price = document.getElementsByClassName("item-price")[ord];

          total_item.innerHTML = orderItem[ord]["quantity"];
          item_total_price.innerHTML = `${orderItem[ord]["total"]} FCFA`;
        }

        activeItem = document.getElementById(`item-total-price-${response.active_orderItem}`);

        $(`#item-total-price-${response.active_orderItem}`).slideUp(0).delay(100).slideDown(500);

        //GET THE VARIABLE
        total = document.getElementById("orderTotal-total");

        //UPDATE THE VALUE
        total.innerHTML = `<b style="color:green;font-size:25px">${response.total} FCFA</b>`;

        if (response.tot_item == 0) {
          console.log("YOU CAN DELETE ME");

          window.location.reload();
        }
      },
    });
  });
}

// Delete Order
delete_item = document.getElementsByClassName("delete-order");
for (let i = 0; i < delete_item.length; i++) {
  delete_item[i].addEventListener("click", () => {
    var delete_item_id = delete_item[i].dataset.delete;
    var delete_item_name = delete_item[i].dataset.item_name;

    Swal.fire({
      title: `Voulez vous supprimer <strong>${delete_item_name}</strong>?`,
      showDenyButton: true,
      confirmButtonText: "Supprimer",
      denyButtonText: `Abandonner`,
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        $.ajax({
          url: `/texasgrillz/deleteorderitem/`,
          method: "POST",
          data: {
            csrfmiddlewaretoken: csrfToken,
            item_id: delete_item_id,
          },
          success: function (response) {
            Swal.fire({
              icon: "success",
              title: `${delete_item_name} supprimer`,
              showConfirmButton: false,
              timer: 1500,
            });
            //delete_item[i].closest(".menudetails-items").style.display = "none";
            setTimeout(() => {
              location.reload();
            }, 1000);
          },
          complete: function (response) {
            console.log("Completed");
          },
        });
      } else if (result.isDenied) {
        return;
      }
    });
  });
}
