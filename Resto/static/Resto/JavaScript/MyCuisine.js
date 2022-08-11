console.log("what do you see");

// var uncompleted_order_body = document.getElementById("card-text");
// var uncompleted_order_section = document.getElementById("uncompleted_order");
// var completed_order_btn = document.getElementsByClassName("order-uncompleted");
// var my_uncomp = document.getElementsByClassName("my_uncomp");
var my_order_item = document.getElementById("order-item");

async function fetchCuisineOrder() {
  var url = "/texasgrillz/GetOrderCuisine/";
  orders = await fetch(url);
  result = await orders.json();
  return result;
}

fetchCuisineOrder().then((data) => {
  console.log(data);
  uncompleted_order = data["uncompleted_order"];
  //   console.log(uncompleted_order);

  uncompleted_order.forEach((order) => {
    my_uncomp = {
      order_name: order.order_name,
      order_table: order.order_table,
    };

    order.order_item.forEach((orderitem) => {
      if (order.order_id == orderitem.order_id) {
        my_uncomp["quantity"] = orderitem.quantity;
        my_uncomp["item"] = orderitem.item;

        if (orderitem.ingredient) {
          my_uncomp["ingredient"] = orderitem.ingredient;
        }

        if (orderitem.accompagnement) {
          my_uncomp["accompagnement"] = orderitem.accompagnement;
        }

        if (orderitem.supplement) {
          my_uncomp["supplement"] = orderitem.supplement;
        }
      }
    });

    console.log(my_uncomp);

    // Uncompleted Order List
    $("#data").append(`<div class="col-auto mt-3">
    <div class="card" style="width:auto; height: auto; background-color: rgb(243, 166, 152)">
      <div class="card-body mb-1">
        <p class="card-text mb-1" style="color: black; text-align: center">Date:${order.order_name}</p>
        <p style="text-align: center"><b style="color: black">Table Number:</b>${order.order_table}</p>
        <h4 class="card-title mb-1" style="color: black; text-align: center">
          <b>Client:${order.order_name}</b>
        </h4>
        <hr style="color: black" />

        <div id="myorderitem" >
       

        <div class="mt-4" style="text-align: center">
          <form class = 'ordercompleted-form' method="POST">
            <small class="text-muted mb-4" >${order.order_name}</small><br>
            <button type="submit" data-action="completed" data-order=${order.order_name} class="btn btn-outline-success mb-3 orderDone">Complete</button>
          </form>
          
              </div>
            </div>
          </div>
      </div>`);

    // my_order_item.innerHTML += `
    // <div class='my_uncomp'> <p class ='mt-3'>${order.order_name} (${order.transaction_id})</p> </div>`;

    // uncompleted_order_section.innerHTML += `<a href="#"  class="btn btn-success mt-2 order-completed">Terminer</a>
    // <a href="#" class="btn btn-danger order-rejected">Rejeter</a>
    // <br class = 'mt-3'>
    // <hr>
  });
  console.log(my_order_item);
});
