// Start here

// send order to the kitchen
var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
var sendOrder = document.getElementsByClassName("send-order");
var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
var transaction = "PINAVCI" + Math.floor(Math.random() * 10000000).toString();
var total_item = null;
var orderItem = null;

//Get total item
function getTotalItem() {
  $.ajax({
    url: "/texasgrillz/sendorder/",
    method: "GET",
    success: function (response) {
      console.log("response", response);
      total_item = response.total_item;

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

//SEND ORDER TO KITCHEN
for (let i = 0; i < sendOrder.length; i++) {
  sendOrder[i].addEventListener("click", function (e) {
    e.preventDefault();
    var action = this.dataset.action;
    var order = this.dataset.order;

    //sendMyOrder(action, order);
    cinetpayAPI();
    //checkout();
  });
}

function sendMyOrder(action, order) {
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
          //menu = location.href.replace("myorder/", "");
          //location.href = menu;
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
        total.innerHTML = `<b id="finalPrice" style="color:green;font-size:25px">${response.total} FCFA</b>`;
        console.log("TOPAY", response.total);

        if (response.tot_ind_item < 1) {
          console.log("YOU CAN DELETE ME");
          deleteItem(response.active_orderItem, response.item_name);
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
      /* isConfirmed, isDenied below */
      if (result.isConfirmed) {
        deleteItem(delete_item_id, delete_item_name);
      } else if (result.isDenied) {
        return;
      }
    });
  });
}

function deleteItem(itemID, itemName) {
  $.ajax({
    url: `/texasgrillz/deleteorderitem/`,
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
      item_id: itemID,
    },
    success: function (response) {
      Swal.fire({
        icon: "success",
        title: `${itemName} supprimer`,
        showConfirmButton: false,
        timer: 1500,
      });
      //delete_item[i].closest(".menudetails-items").style.display = "none";
      setTimeout(() => {
        location.reload();
      }, 2000);
    },
    complete: function (response) {
      console.log("Completed");
    },
  });
}

//Verify paiement
function verifyPaiement(api, site, transaction) {
  $.ajax({
    url: `https://api-checkout.cinetpay.com/v2/payment/check?apikey=${api}&site_id=${site}&transaction_id=${transaction}`,
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
    },
    dataType: "json",

    success: function (response) {
      status_res = response.data.status;
      amount = response.data.amount;
      currency = response.data.currency;
      description = response.data.description;
      operator_id = response.data.operator_id;
      payment_date = response.data.payment_date;
      payment_method = response.data.payment_method;

      if (status_res === "ACCEPTED") {
        setTimeout(function () {
          console.log("Paiement Verified, Redirecring you....", status_res);
          //location.href = "/";
        }, 5000);
      } else if (status_res === "REFUSED") {
        swal({
          icon: "error",
          title: "Transaction rejeter",
          timer: 2000,
        }).then(() => {
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        });
      }

      //Paiement Data
      data = {
        csrfmiddlewaretoken: csrfToken,
        user: "{{request.user.id}}",
        amount: amount,
        currency: currency,
        description: description,
        operator_id: operator_id,
        payment_date: payment_date,
        status: status_res,
        payment_method: payment_method,
      };

      //Add paiement to Database
      setTimeout(function () {
        processPaiement(data);
      }, 5000);
    },

    error: function (error) {
      console.log(error);
    },
  });
}

//Record payment to DataBase
function processPaiement(pay_data) {
  $.ajax({
    url: "/process_transaction/",
    method: "POST",
    headers: {
      accept: "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    data: {
      csrfmiddlewaretoken: csrfToken,
      user: "{{request.user.id}}",
      amount: amount,
      currency: currency,
      description: description,
      operator_id: operator_id,
      payment_date: payment_date,
      transactionID: transaction,
      status: status_res,
      payment_method: payment_method,
    },
    dataType: "json",
    success: function (response) {
      console.log("Paiement added to DataBase");
    },
  });
}

//Get Credential Cinetpay
function cinetpayAPI() {
  $.ajax({
    url: "/cinetpayapi/",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
    },
    dataType: "json",
    success: function (response) {
      api = response.apiKey;
      site = response.site_id;

      var toPay = document.getElementById("finalPrice").innerHTML;
      toPay = parseInt(toPay.split(" ")[0]);

      console.log("Amount to pay", toPay);

      checkout(api, site, toPay);

      //return response;
    },
  });
}

// Checkout API
function checkout(api, site, amount) {
  CinetPay.setConfig({
    apikey: api, //YOUR APIKEY
    site_id: site, //YOUR_SITE_ID
    notify_url: "http://mondomaine.com/notify/",
    mode: "PRODUCTION",
  });
  CinetPay.getCheckout({
    transaction_id: transaction, //YOUR TRANSACTION ID
    amount: amount,
    currency: "XOF",
    channels: "ALL",
    description: "Test paiement",
    customer_name: "Joe", //Customer name
    customer_surname: "Down", //The customer's first name
    customer_email: "down@test.com", //the customer's email
    customer_phone_number: "088767611", //the customer's email
    customer_address: "BP 0024", //customer address
    customer_city: "Antananarivo", // The customer's city
    customer_country: "CI", // the ISO code of the country
    customer_state: "CM", // the ISO state code
    customer_zip_code: "06510",
  });
  CinetPay.waitResponse(function (data) {
    if (data.status == "REFUSED") {
      console.log("refused");
    } else if (data.status == "ACCEPTED") {
      console.log("accepted");
    }
    verifyPaiement(api, site, transaction);
  });

  return "Caisse Ouverte";
}
