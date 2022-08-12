console.log("what do you see");
var total_uncompleted_order = document.getElementById("total_uncompleted_order").innerHTML;

//FETCH DATA
async function fetchCuisineOrder() {
  var url = "/texasgrillz/GetOrderCuisine/";
  orders = await fetch(url);
  result = await orders.json();
  console.log(result);
  return result;
}

// async function fetchUncompletedOrder() {
//   var url = "/texasgrillz/GetOrderCuisine/";
//   orders = await fetch(url);
//   result = await orders.json();
//   data = result["uncompleted_order"];
//   console.log("MY DATA:", data.length);

//   if (parseInt(total_uncompleted_order) > data.length) {
//     console.log("REFRESHING....");
//     fetchCuisineOrder().then((data) => {
//       displayUncompletedOrder(data);
//       console.log("DISPLAY....");
//     });
//   }
// }

async function GetUpComingOrder() {
  var url = "/texasgrillz/sendorder/";
  orders = await fetch(url);
  result = orders.json();
  console.log(result);
}

//COMPLETED ORDER : AJAX
function completeOrder(orderID) {
  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
  $.ajax({
    url: "/texasgrillz/CompletedOrder/",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
      id: orderID,
    },
    dataType: "json",
    success: function (response) {
      $("#total_uncompleted_order").empty();

      fetchCuisineOrder().then((data) => {
        displayUncompletedOrder(data);
        console.log("DISPLAY....");
      });
      $("#total_uncompleted_order").append(response.uncompleted_order);
    },
    error: function () {
      console.log("AN ERROR HAS OCCURED");
    },
  });
}

//DISPLAY ORDER TO FRONT END
function displayUncompletedOrder(orders) {
  uncompleted_order = orders["uncompleted_order"];
  //   console.log(uncompleted_order);

  $("#data").empty();
  $("#total_uncompleted_order").empty();

  console.log("HOW MANY NOW:", uncompleted_order.length);
  $("#total_uncompleted_order").append(uncompleted_order.length);

  uncompleted_order.forEach((order) => {
    my_uncomp = {
      order_name: order.order_name,
      order_table: order.order_table,
    };

    items = [];

    order.order_item.forEach((orderitem) => {
      if (order.order_id == orderitem.order_id) {
        my_uncomp["quantity"] = orderitem.quantity;
        my_uncomp["item"] = orderitem.item;
        items.push(`<p class ='mt-0'> <span style = 'font-size:25px ;color:chocolate; font-weight:bold'>${orderitem.quantity}</span> - ${orderitem.item}<p>`);

        if (orderitem.ingredient) {
          my_uncomp["ingredient"] = orderitem.ingredient;
          items.push(`
          <p class ='mt-0'> <b>Ingredient:</b> ${orderitem.ingredient}</p>`);
        }

        if (orderitem.accompagnement) {
          my_uncomp["accompagnement"] = orderitem.accompagnement;
          items.push(`
          <p class ='mt-0'> <b>Accompagement(s):</b> ${orderitem.accompagnement}</p>`);
        }

        if (orderitem.supplement) {
          my_uncomp["supplement"] = orderitem.supplement;
          items.push(`
          <p class ='mt-0'> <b>Supplement(s):</b> ${orderitem.supplement}</p>`);
        }
      }
    });

    if (order.side_orderitem.length > 0) {
      items.push(`<p class ='mt-0'> <b> Other Accomp(s):</b></p>`);
      order.side_orderitem.forEach((side) => {
        if (order.order_id == side.order_id) {
          items.push(`<p class ='mt-0'> <span style = 'font-size:25px ;color:chocolate; font-weight:bold'>${side.quantity}</span> - ${side.name}<p>`);
        }
      });
    }

    //ORDER ITEMS
    for (var i in items) {
      my_items = items.join("");
    }

    // Uncompleted Order List
    $("#data").append(`<div class="col-auto mt-3">
    <div class="card shadow rounded-3 border border-danger" style="width:auto; height: auto; background-color: white">
      <div class="card-body mb-1">

        <h4 style="text-align: center"><b style="color: black">Table:</b> <span style='color:chocolate';> ${order.order_table}</span> </h4>
        <h4 class="card-title mb-1" style="color: black; text-align: center">
          <b>Client:</b> <span style='color:chocolate';> ${order.order_name}</span> 
        </h4>
        <hr style="color: black" />

        <div id="myorderitem" >
        <div id="order-item" class="card-text mb-2" style="color: black; text-align: center">${my_items}</div>
        <div class="mt-4" style="text-align: center">
          <form class = 'ordercompleted-form' method ='POST' >
            <small class="text-muted mb-4" >${order.order_name}</small><br>
            <button type="submit" data-action="completed" data-order=${order.order_id} class="btn mb-3 orderDone">Terminer</button>
          </form>
              </div>
            </div>
          </div>
      </div>`);
  });

  var completed_order_btn = document.getElementsByClassName("orderDone");
  for (let i = 0; i < completed_order_btn.length; i++) {
    completed_order_btn[i].addEventListener("click", (e) => {
      e.preventDefault();
      orderID = completed_order_btn[i].dataset.order;
      console.log("Order completed");
      completeOrder(orderID);
    });
  }
}

function GetOrderData() {
  fetchCuisineOrder().then((data) => {
    displayUncompletedOrder(data);
  });
}

GetOrderData();

setInterval(() => {
  console.log("GETTING DATA");
  GetOrderData();
}, 6000);
