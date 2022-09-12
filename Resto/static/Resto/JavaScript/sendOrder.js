// Start here
// send order to the kitchen
var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
var sendOrder = document.getElementsByClassName("send-order");

var total_item = null;
var orderItem = null;

//  WEBSOCKET ROOTING
// let url = `ws://${window.location.host}/ws/sendOrder/uncompleted-order/`;
// const sendOrderSocket = new WebSocket(url);

// sendOrderSocket.onclose = (e) => {
//   console.log("Reconnecting....");
// };

// //OPEN DJANGO-CHANNELS
// sendOrderSocket.onopen = (e) => {
//   console.log("I am connected to websocket", url);
// };

// sendOrderSocket.onerror = (error) => {
//   console.log(error);
//   sendOrderSocket.close();
// };

//Get total item
function getTotalItem() {
  $.ajax({
    url: "/sendorder/",
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

    console.log("Paiement_method", paiement_method.innerText);

    if (paiement_method.innerText === "Mobile") {
      //CINETPAY API
      cinetpayAPI();
    } else {
      sendMyOrder(action, order);
    }

    //SEND MESSAGE TO SERVER DJANGO-CHANNEL
    // sendOrderSocket.send(
    //   JSON.stringify({
    //     message: order,
    //     type: "order_status",
    //   })
    // );
  });
}

function sendMyOrder(action, order) {
  $.ajax({
    url: "/sendorder/",
    method: "POST",
    data: { csrfmiddlewaretoken: csrfToken, action: action, order: order },
    dataType: "json",

    beforeSend: function () {
      $("#spinner-div").show();
    },

    success: function (response) {
      console.log(response.Order_Status == "Sent to kitchen");
      console.log("total Item:", total_item);

      if (response.Order_Status == "Sent to kitchen") {
        // DJANGO CHANNEL

        $(".menudetails-content").fadeOut(1000);
        $(".paiement-box").fadeOut(1000);
        $(".total-box").fadeOut(1000);
        $(".userfield").fadeOut(1000);
        $(".logofield").fadeOut(1000);

        $(".notification-order-box").fadeIn(100).append(`
          <div class="text-center">

          <div class="py-5 p-2 flex text-center mt-5">
          <p class="mb-4 mt-5 animate-bounce" style="font-size: 1.5rem; color: chocolate">Please remain patient while we're 
          sending your order to the kitchen</p>
          </div>

          <button type="submit" class="bg-indigo-500 btn">
            Processing...
          </button>

          <div class="logofield py-5 p-2 flex justify-center mt-5 animate-pulse">
          
          <span class="businesslogo "><img src="${response.icarus_img}" alt="" width="150px" height="150px" /></span>
         </div>

        </div>`);
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
    var ordItem = this.dataset.orderitem;
    var sideorderitem = this.dataset.sideorderitem;
    var accompa = this.dataset.accomp;

    console.log("ORDER ITEM ID", ordItem);
    console.log("action:", action);

    // GET TABLE NUMBER
    table = location.href.split("&")[1].split("=")[1];

    $.ajax({
      url: "/checkoutpage/",
      method: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
        itemId: itemId,
        ordItem: ordItem,
        action: action,
        table: table,
        sideorderitem: sideorderitem,
      },
      success: function (response) {
        console.log(response);
        active_item = null;

        // Get Response from backend
        orderitem_id = response.order_item_id;
        orderitem_quantity = response.tot_ind_item;
        total_orderitem = response.total_order_item;
        total_sup = response.total_supplement;

        var total_item = document.getElementById(`item-quantity-${orderitem_id}`);
        var item_total_price = document.getElementById(`item-total-price-${orderitem_id}`);

        total_item.innerHTML = orderitem_quantity;
        item_total_price.innerHTML = `${total_orderitem} FCFA`;

        activeItem = document.getElementById(`item-total-price-${response.active_orderItem}`);

        $(`#item-total-price-${response.active_orderItem}`).slideUp(0).delay(100).slideDown(500);

        //GET THE VARIABLE
        total = document.getElementById("orderTotal-total");

        //UPDATE THE VALUE
        total.innerHTML = `<b id="finalPrice" style="color:green;font-size:25px">${response.total} FCFA</b>`;

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
    url: `/deleteorderitem/`,
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
      processPaiement(data, transaction);
      if (status_res === "ACCEPTED") {
        console.log("Paiement Verified, Redirecring you....", status_res);
        Swal.fire({
          icon: "success",
          title: "Nous avons bien reçu votre commande",
          showConfirmButton: false,
          timer: 4000,
        }).then(() => {
          setTimeout(() => {
            menu = location.href.replace("myorder/", "homepage/");
            location.href = menu;
          }, 3000);
        });
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
    },

    error: function (error) {
      console.log(error);
    },
  });
}

//Record payment to DataBase
function processPaiement(pay_data, transaction) {
  var orderID = $("#order_id").val();
  $.ajax({
    url: "/process_transaction/",
    method: "POST",
    headers: {
      accept: "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    data: {
      csrfmiddlewaretoken: csrfToken,
      amount: amount,
      currency: currency,
      description: description,
      operator_id: operator_id,
      payment_date: payment_date,
      transactionID: transaction,
      status: status_res,
      payment_method: payment_method,
      orderID: orderID,
    },
    dataType: "json",
    success: function (response) {
      console.log("Paiement added to DataBase");
    },
  });
}

//Get Credential Cinetpay
function cinetpayAPI() {
  var toPay = document.getElementById("finalPrice").innerHTML;
  toPay = parseInt(toPay.split(" ")[0]);

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

      //PAY FOR ORDER
      checkout(api, site, 100);
    },
  });
}

// Checkout API
function checkout(api, site, amount) {
  //TRANSACTION_ID
  var transaction = "Icarus-" + Math.floor(Math.random() * 10000000).toString();
  console.log("MY ORDER ID", transaction);

  //ORDER_ID
  var orderID = $("#order_id").val();
  console.log("MY ORDER ID", orderID);

  CinetPay.setConfig({
    apikey: api, //YOUR APIKEY
    site_id: site, //YOUR_SITE_ID
    notify_url: "http://mondomaine.com/notify/",
    mode: "PRODUCTION",
  });
  CinetPay.getCheckout({
    transaction_id: transaction, //YOUR TRANSACTION ID
    amount: 100,
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
      return;
    } else if (data.status == "ACCEPTED") {
      console.log("accepted");
      sendMyOrder("Sent", orderID);
    }
    verifyPaiement(api, site, transaction);
  });

  return "Caisse Ouverte";
}
