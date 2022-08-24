console.log("what do you see");

var total_uncompleted_order = document.getElementById("total_uncompleted_order").innerHTML;

fetchCuisineOrder().then((data) => {
  console.log("PLEASE STAY PATIENT WHILE WE'RE GETTING YOUR ORDER");
  console.log(data);
  displayUncompletedOrder(data["uncompleted_order"]);
  displayCompletedOrder(data["completed_order"]);
});

//FETCH DATA
async function fetchCuisineOrder() {
  var url = "/texasgrillz/GetOrderCuisine/";
  orders = await fetch(url);
  result = await orders.json();
  return result;
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
      $("#total_completed_order").empty();

      fetchCuisineOrder().then((data) => {
        console.log("ORDER COMPLETED, AJAX TO UPDATE");
        displayUncompletedOrder(data["uncompleted_order"]);
        displayCompletedOrder(data["completed_order"]);
      });

      $("#total_uncompleted_order").append(response.uncompleted_order);
      $("#total_completed_order").append(response.completed_order);
    },
    error: function () {
      console.log("AN ERROR HAS OCCURED");
    },
  });
}

//DISPLAY ORDER TO FRONT END
function displayUncompletedOrder(orders) {
  uncompleted_order = orders;

  $("#total_uncompleted_order").empty();
  $("#unCompletedOrder").empty();

  // console.log("HOW MANY NOW:", uncompleted_order.length);

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
    $("#unCompletedOrder").append(`<div class="col-auto mt-3">
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
            <small class="text-muted mb-4" >${order.order_date}</small><br>
            <button type="submit" data-action="completed" data-order=${order.order_id} class="completedbtn shadow mb-3 orderDone">Terminer</button>
          </form>
              </div>
            </div>
          </div>
      </div>
      `);
  });

  connectWebSocket();

  var completed_order_btn = document.getElementsByClassName("orderDone");
  for (let i = 0; i < completed_order_btn.length; i++) {
    completed_order_btn[i].addEventListener("click", (e) => {
      e.preventDefault();
      orderID = completed_order_btn[i].dataset.order;
      completeOrder(orderID);
    });
  }
}

// DJANGO-CHANNEL WEBSOCKET
function connectWebSocket() {
  let url = `ws://${window.location.host}/ws/sendOrder/`;
  const sendOrderSocket = new WebSocket(url);

  console.log("Connecting to webSocket");
  // OPEN DJANGO-CHANNELS
  sendOrderSocket.onopen = (e) => {
    console.log("I am connected to websocket.");
  };

  // MESSAGE FROM SERVER DJANGO-CHANNELS
  sendOrderSocket.onmessage = (e) => {
    var data = JSON.parse(e.data);
    console.log("Data from server:", data);
    if (data.type == "order_sent") {
      var all_uncompleted_orders = data["uncompleted_order"];
      displayUncompletedOrder(all_uncompleted_orders);
    }
  };

  // CLOSE DJANGO-CHANNELS
  sendOrderSocket.onclose = (e) => {
    console.log("Reconnecting WebSocket...");
    setTimeout(() => {
      connectWebSocket();
    }, 1000);
  };

  // ERROR DJANGO-CHANNELS
  sendOrderSocket.onerror = (error) => {
    console.log(error);
    sendOrderSocket.close();
  };
}

function displayCompletedOrder(orders) {
  completed_order = orders;

  $("#total_completed_order").empty();
  $("#completedOrder").empty();
  $("#total_completed_order").append(completed_order.length);

  completed_order.forEach((order) => {
    my_comp = {
      order_name: order.order_name,
      order_table: order.order_table,
    };

    // Uncompleted Order List
    $("#completedOrder").append(`
          <tr class='text-center' id ='card-${order.order_id}'>
            <td style='color' scope="row">${order.order_table}</td>
            <td>${order.order_name}</td>
            <td>${order.order_date_completed}</td>
            <td>
            <button type='submit' data-order_id = ${order.order_id} class='completedbtn shadow order-details' data-bs-toggle="modal" data-bs-target="#staticBackdrop"> Details </button>
            </td>
          </tr>
      `);
  });

  var details_order_btn = document.getElementsByClassName("order-details");
  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

  for (let i = 0; i < details_order_btn.length; i++) {
    details_order_btn[i].addEventListener("click", (e) => {
      $(".modal-body").empty();
      $("#order-tansaction").empty();

      order_items = [];

      $("#order-tansaction").append(`<span style = 'font-size:25px ;color:chocolate; font-weight:bold'>${completed_order[i].transaction_id}</span> <span class='badge'> Orange Money </span>`);
      completed_order[i].order_item.forEach((item) => {
        $("#quantity").append(`<p class ='mt-0'> <span style = 'font-size:25px ;color:chocolate; font-weight:bold'>${item.quantity}</span> - ${item.item}<p>`);
        order_items.push(`<p class ='mt-0'> <span style = 'font-size:25px ;color:chocolate; font-weight:bold'>${item.quantity}</span> - ${item.item}<p>`);

        if (item.ingredient) {
          $("#ingredient").append(`
          <p class ='mt-0'> <b>Ingredient:</b> ${item.ingredient}</p>`);
          order_items.push(`
          <p class ='mt-0'> <b>Ingredient:</b> ${item.ingredient}</p>`);
        }

        if (item.accompagnement) {
          $("#accompagnement").append(`
          <p class ='mt-0'> <b>Accompagement(s):</b> ${item.accompagnement}</p>`);
          order_items.push(`
          <p class ='mt-0'> <b>Accompagement(s):</b> ${item.accompagnement}</p>`);
        }

        if (item.supplement) {
          $("#supplement").append(`
          <p class ='mt-0'> <b>Supplement(s):</b> ${item.supplement}</p>`);
          order_items.push(`
          <p class ='mt-0'> <b>Supplement(s):</b> ${item.supplement}</p>`);
        }
      });

      if (completed_order[i].side_orderitem.length > 0) {
        $("#side_order").append(`<p class ='mt-0'> <b> Other Accomp(s):</b></p>`);
        completed_order[i].side_orderitem.forEach((side) => {
          order_items.push(`<p class ='mt-0'> <span style = 'font-size:25px ;color:chocolate; font-weight:bold'>${side.quantity}</span> - ${side.name}<p>`);
        });
      }

      //ORDER ITEMS
      for (var ord in order_items) {
        my_order_items = order_items.join("");
      }

      $(".modal-body").append(`
      <div id="order-item" class="card-text mb-2" style="color: black; text-align: center">${my_order_items}</div>
      `);
    });
  }
}
