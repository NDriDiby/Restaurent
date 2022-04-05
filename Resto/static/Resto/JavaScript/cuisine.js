$(document).ready(function () {
  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

  var active_order = null;

  function fetchdata(time) {
    setInterval(getdata, time);
  }

  //fetchdata(1000);
  getdata(); //

  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

  //Get uncompleted order
  function getdata() {
    $.ajax({
      url: "/texasgrillz/GetOrderCuisine/",
      method: "GET",
      data: {
        csrfmiddlewaretoken: csrfToken,
      },

      success: function (response) {
        console.log(response);

        $("#orderUncompleted").empty(); //no refresh
        $("#totalUncompleted").empty(); //no refresh
        $("#totalcompleted").empty(); //no refresh
        $("#data").empty(); //no refresh

        $("#accordion").empty();

        //Get the number of completed and uncompleted order
        $("#totalUncompleted").append(response.total_uncompleted_order);
        $("#totalcompleted").append(response.total_completed_order);

        //Get the variable from the response
        total_uncomp = response.total_uncompleted_order;
        total_uncomp = total_uncomp[0];

        total_comp = response.total_completed_order;
        total_comp = total_comp[0];

        //Give percentage of completed order
        perCompleted = 100 - Math.round((total_uncomp / total_comp) * 100, 0);
        console.log(perCompleted);

        order_uncomp = response.order;

        for (var ord in response.order) {
          data = {
            orderName: response.order[ord],
            order: response.order[ord]["id"],
            table: response.order[ord]["table"],
            dateOrdered: response.order[ord]["date_ordered"],
          };

          var myorderitem = [];

          for (var i in response.myorder) {
            {
              var ordername = response.myorder[i]["order"];
              if (response.myorder[i]["order_id"] == data["order"]) {
                data["orderName"] = response.myorder[i]["order"];
                data["quantity"] = response.myorder[i]["quantity"];
                data["ingredient"] = response.myorder[i]["ingredient"];
                myorderitem.push(`
                 <p style = 'color:black'>${response.myorder[i]["item"]} (${response.myorder[i]["quantity"]})<br><b>${response.myorder[i]["ingredient"]}</b></br> <p>`);
              }
            }
          }

          //ORDER ITEMS
          for (var i in myorderitem) {
            check = myorderitem.join(" ");
          }

          // Uncompleted Order List
          $("#data").append(`<div class="col-auto mt-3">
            <div class="card" style="width:auto; height: auto; background-color: rgb(243, 166, 152)">
              <div class="card-body mb-1">
                <p class="card-text mb-1" style="color: black; text-align: center">Date:${data["dateOrdered"]}</p>
                <p style="text-align: center"><b style="color: black">Table Number:</b>${data["table"]}</p>
                <h4 class="card-title mb-1" style="color: black; text-align: center">
                  <b>Customer:${data["orderName"]}</b>
                </h4>
                <hr style="color: black" />

                <div id="myorderitem" >
                <p class="card-text mb-2" style="color: black; text-align: center"><b>*</b>${check}</p>

                <div class="mt-4" style="text-align: center">
                  <form class = 'ordercompleted-form' method="POST">
                    <small class="text-muted mb-4" >${data["dateOrdered"]}</small><br>
                    <button type="submit" data-action="completed" data-order=${data["order"]} class="btn btn-outline-success mb-3 orderDone">Complete</button>
                  </form>
                  
                      </div>
                    </div>
                  </div>
              </div>`);
        }

        //if there is no order
        $("#noOrder").hide();

        for (var i in order_uncomp) {
          var form_order = document.getElementsByClassName("ordercompleted-form")[i];

          var orderDone = document.getElementsByClassName("orderDone")[i];

          orderDone.addEventListener(
            "click",
            (function (item) {
              return function (e) {
                order_click(item);

                e.preventDefault();
                update_order();
              };
            })(order_uncomp[i])
          );
        }

        //Completed Order List
        for (var i in response.completed_order) {
          myorderitem = [];

          for (var ord in response.completed_order_item) {
            if (response.completed_order[i]["id"] == response.completed_order_item[ord]["order_id"]) {
              orderName = response.completed_order_item[ord]["order"];
              ordernumber = response.completed_order[i]["id"];
              table = response.completed_order[i]["table"];
              transaction_id = response.completed_order[i]["transaction_id"];
              date_completed = response.completed_order[i]["date_completed"];
              orderStatus = response.completed_order[i]["status"];

              myorderitem.push(`
                 <p style = 'color:black'>${response.completed_order_item[ord]["item"]} (${response.completed_order_item[ord]["quantity"]})<p>`);
            }
          }

          //ORDER ITEMS
          for (var i in myorderitem) {
            check = myorderitem.join(" ");
          }

          //show success message after order completed
          msg = document.getElementById("message");
          msg.innerHTML = ` <div id="message" class="col-12">
              <div class="alert alert-success alert-dismissible" style="text-align: center" role="alert">
                <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
                  <use xlink:href="#check-circle-fill" />
                </svg>
                <h4 style="color:black"> <b>${perCompleted}%</b> completed </h4>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            </div>`;

          //Data from backend
          $("#accordion").append(`<span  data-bs-target='#order-${ordernumber}' data-bs-toggle="collapse" data-order ={{order.id}} >
            <div id ='cardnum-${active_order}' class="card">
              <div class="card-header">
                <h6 class="card-link"   href="#collapseOne">
                  Table:${table}- Customer Name: <strong style="color:rgb(3, 131, 250);"> ${orderName}</strong>
                  - Order Number:${ordernumber} - Ref: ${transaction_id} - Date: ${date_completed} - <strong style ='color:green' >${orderStatus}</strong>
                   <i style ='color:green' class="bi bi-check-square"></i>
                </h6>
                <div id="order-${ordernumber}" class="collapse show mt-2" data-parent="#accordion">
                  <div class="full_order">
                    <p class="card-text mb-2" style="color: black; text-align: center;"><b>*</b>${check}</p>
                  </div>
                </div>
              </div>
             </div>
          `);

          //order_comp = document.getElementById(`order_completed-${ordernumber}`)
          cardnum = document.getElementById(`cardnum-${active_order}`);

          //SHOW CARD COLOR FLASHING
          cardnum.style.backgroundColor = "rgb(54, 126, 54)";
          setInterval(function () {
            cardnum.style.backgroundColor = "white";
          }, 3000);

          //order_comp.addEventListener('click',function(e){
          // order_id(cardnum)
          // e.stopPropagation();

          // })
        }
      },
      error: function (response) {
        console.log("THERE IS AN ERROR", response);
      },
    });
  }

  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

  //COMPLETED ORDER
  function update_order() {
    $.ajax({
      url: "/texasgrillz/CompletedOrder/",
      method: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
        id: active_order,
      },
      dataType: "json",
      success: function (response) {
        getdata();
      },
      error: function () {
        console.log("AN ERROR HAS OCCURED");
      },
    });
  }

  function order_click(order_id) {
    console.log("you clicked me", order_id["id"]);
    active_order = order_id;
    active_order = active_order["id"];
  }

  function order_id(order_id) {
    console.log("Find Me", order_id);
  }
});
