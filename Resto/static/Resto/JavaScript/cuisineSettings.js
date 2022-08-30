console.log("Setting Cuisine");

const fetchtItems = async () => {
  url = "/texasgrillz/dashBoard_data/";
  var getItem = await fetch(url);
  var data = await getItem.json();
  console.log(data);
  return data;
};

fetchtItems().then((data) => {
  my_items = data["my_items"];
  // $("#total_completed_order").empty();
  $("#mes-recettes").empty();
  // $("#total_completed_order").append(completed_order.length);

  my_items.forEach((item) => {
    my_acc = [];
    my_sup = [];

    if (item.accompagnement) {
      item.accompagnement.forEach((acc) => {
        my_acc.push(acc.accomp_name);
      });
    }

    if (item.supplement) {
      item.supplement.forEach((sup) => {
        my_sup.push(sup.sup_name);
      });
    }

    $("#mes-recettes").append(`
          <tr class='text-center'>
            <td style='color' scope="row">${item.name}</td>
            <td>${item.prix}</td>
            <td>${item.category}</td>
            <td>${my_acc}</td>
            <td>${my_sup}</td>
            <td>
            <button type='submit' data-order_id = ${item.name} class='completedbtn shadow order-details' data-bs-toggle="modal" data-bs-target="#staticBackdrop"> Modifier </button>
            </td>
          </tr>
      `);
  });
});

function deleteItem(itemID, itemName) {
  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
  $.ajax({
    url: `/texasgrillz/deleteitem/`,
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

var add_item_btn = document.getElementById("add-item");

add_item_btn.addEventListener("click", () => {
  console.log("I want to add an item");
});

const instruction = () => {
  Swal.fire({
    icon: "error",
    title: `Select or create a category`,
    showConfirmButton: true,
  });
};

var delete_recette_btn = document.getElementsByClassName("delete-recette");
for (let i = 0; i < delete_recette_btn.length++; i++) {
  delete_recette_btn[i].addEventListener("click", (e) => {
    e.preventDefault();
    item_id = delete_recette_btn[i].dataset.delete;
    item_name = delete_recette_btn[i].dataset.item_name;

    Swal.fire({
      title: `Voulez vous supprimer <strong>${item_name}</strong>?`,
      showDenyButton: true,
      confirmButtonText: "Supprimer",
      denyButtonText: `Abandonner`,
    }).then((result) => {
      /* isConfirmed, isDenied below */
      if (result.isConfirmed) {
        deleteItem(item_id, item_name);
      } else if (result.isDenied) {
        return;
      }
    });
  });
}

var new_cat = $("input[name=new-cat-name]");

$(".category").change(() => {
  var cat = $("#id_category :selected").text();
  if (cat != "---------") {
    new_cat.attr("disabled", "disabled");
  } else {
    new_cat.removeAttr("disabled", "disabled");
  }
  console.log(cat);
});

var create_recette_form = document.getElementById("create-recette");
var new_cat_list = [];
var all_accomp = [];
var all_sup = [];

create_recette_form.addEventListener("click", (e) => {
  console.log("MOVE ME");

  var new_cat = $("input[name=new-cat-name]").val();
  var cat = $("#id_category :selected").text();
  var nom = $("input[name=name]").val();
  var prix = $("input[name=prix]").val();
  var description = $("#id_description").val();

  // $("#id_supplement option")
  //   .filter(":selected")
  //   .each((acc, data) => {
  //     console.log(acc, data.value);
  //     all_sup.push(data.value);
  //   });

  // var new_sup = $("input[name=new-sup-name]").val();
  // var sup = $("#id_category :selected").text();
  // var new_sup = $("#id_category :selected").text();

  console.log("new:", new_cat);
  console.log("cat:", cat);
  console.log("nom:", nom);
  console.log("prix:", prix);
  console.log("description:", description);

  // console.log("sup:", all_sup);
  // console.log("new_sup:", new_sup);
});

var add_accomp_form = document.getElementById("add-accomp-form");
add_accomp_form.addEventListener("click", () => {
  $("#id_accompagnement option")
    .filter(":selected")
    .each((acc, data) => {
      console.log(acc, data.value);
      all_accomp.push(data.value);
    });

  var new_accomp = $("input[name=new-accomp-name]").val();

  console.log("accomp:", all_accomp);
  console.log("new_accomp:", new_accomp);
});
