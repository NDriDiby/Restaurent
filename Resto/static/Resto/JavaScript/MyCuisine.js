console.log("what do you see");

var uncompleted_order_body = document.getElementById("card-text");
var uncompleted_order_section = document.getElementById("uncompleted_order");
var completed_order_btn = document.getElementsByClassName("order-uncompleted");
var my_uncomp = document.getElementsByClassName("my_uncomp");

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
    uncompleted_order_section.innerHTML += `
    <div class='my_uncomp'> <p class ='mt-3'>${order.order_name} (${order.transaction_id})</p> </div>`;

    order.order_item.forEach((orderitem) => {
      uncompleted_order_section.innerHTML += `<li class='mt-2'>${orderitem.quantity}-${orderitem.item}</li>
      `;

      if (orderitem.ingredient) {
        uncompleted_order_section.innerHTML += `<p class=''mb-2>ingredient: ${orderitem.ingredient}</p>
        `;
      }

      if (orderitem.accompagnement) {
        uncompleted_order_section.innerHTML += `<p>${orderitem.accompagnement}</p>
        `;
      }

      if (orderitem.supplement) {
        uncompleted_order_section.innerHTML += `<p>${orderitem.supplement}</p>
        `;
      }
    });

    uncompleted_order_section.innerHTML += `<a href="#"  class="btn btn-success mt-2 order-completed">Terminer</a>
    <a href="#" class="btn btn-danger order-rejected">Rejeter</a>
    <br class = 'mt-3'>
    <hr>
    `;
  });

  for (var i = 0; i < completed_order_btn.length; i++) {
    completed_order_btn[i].addEventListener("click", () => {
      console.log("PRESSE ME", i);
    });
  }
});
