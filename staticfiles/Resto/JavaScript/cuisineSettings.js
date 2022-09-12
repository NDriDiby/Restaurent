console.log("Setting Cuisine");
var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

const fetchtItems = async () => {
  url = "/dashBoard_data/";
  var getItem = await fetch(url);
  var data = await getItem.json();
  console.log(data);
  return data;
};

// fetchtItems().then((data) => {
//   my_items = data["my_items"];
//   // $("#total_completed_order").empty();
//   $("#mes-recettes").empty();
//   // $("#total_completed_order").append(completed_order.length);

//   my_items.forEach((item) => {
//     my_acc = [];
//     my_sup = [];

//     if (item.accompagnement) {
//       item.accompagnement.forEach((acc) => {
//         my_acc.push(acc.accomp_name);
//       });
//     }

//     if (item.supplement) {
//       item.supplement.forEach((sup) => {
//         my_sup.push(sup.sup_name);
//       });
//     }

//     $("#mes-recettes").append(`
//           <tr class='text-center'>
//             <td style='color' scope="row">${item.name}</td>
//             <td>${item.prix}</td>
//             <td>${item.category}</td>
//             <td>${my_acc}</td>
//             <td>${my_sup}</td>
//             <td>
//             <button type='submit' data-order_id = ${item.name} class='completedbtn shadow order-details' data-bs-toggle="modal" data-bs-target="#staticBackdrop"> Modifier </button>
//             </td>
//           </tr>
//       `);
//   });
// });

function deleteItem(itemID, itemName) {
  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
  $.ajax({
    url: `/deleteitem/`,
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

const instructionReload = (error, message) => {
  Swal.fire({
    icon: error,
    title: message,
    showConfirmButton: true,
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.reload();
    }
  });
};

// DELETE RECETTE
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

// ACCOMP
var add_accomp_ajax = document.getElementsByClassName("add-accomp");
for (let i = 0; i < add_accomp_ajax.length; i++) {
  add_accomp_ajax[i].addEventListener("click", () => {
    itemID = add_accomp_ajax[i].dataset.item;
    localStorage.setItem("itemID", itemID);
    $(".accomp-item-add").empty();
  });
}

var add_accomp_ajax_btn = document.getElementById("add-accomp-ajax");
add_accomp_ajax_btn.addEventListener("click", (e) => {
  e.preventDefault();
  console.log("REAL TIME BRO");

  var accomp_name = $("#accomp_name").val();
  var accomp_prix = $("#accomp_prix").val();
  var accomp_img = $("#accomp_img").val();
  var item = localStorage.getItem("itemID");
  var action = $("#add-accomp-ajax").data("action");

  console.log("Item-numb", item);
  $.ajax({
    url: "/recette/",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
      accomp_name: accomp_name,
      accomp_prix: accomp_prix,
      accomp_img: accomp_img.split("\\")[2],
      action: action,
      item: item,
    },
    dataType: "json",
    success: function (response) {
      console.log(response);
      instructionReload("success", `${accomp_name} Ajouter`);
    },

    error: function (error) {
      console.log(error);
    },
  });

  localStorage.removeItem("ItemID");
});

var add_accomp_ajax_btn_old = document.getElementById("add-accomp-ajax-old");
add_accomp_ajax_btn_old.addEventListener("click", (e) => {
  e.preventDefault();
  console.log("REAL TIME BRO");

  var accomp_id = $("#id_accompagnement").val();
  var action = $("#add-accomp-ajax-old").data("action");
  var item = localStorage.getItem("itemID");

  console.log("Item-numb", accomp_id);

  $.ajax({
    url: "/recette/",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
      accomps: accomp_id.toString(),
      action: action,
      item: item,
    },
    dataType: "json",
    success: function (response) {
      console.log(response);
      if (response.message == "added") {
        instructionReload("success", `${accomp_id} Ajouter`);
      } else {
        instructionReload("error", `${accomp_id} Exist deja`);
      }
    },

    error: function (error) {
      console.log(error);
    },
  });

  localStorage.removeItem("ItemID");
  $(".accomp-item-add").append(`
  <label for="inputPassword4" class="form-label">Accompagement</label>
   {{form.accompagnement}}
   <small class="text-muted" >Appuyer cmd pour selectioner plusieur ou deselectioner</small>
  `);
});

// SUPPLEMENT
var add_sup_ajax = document.getElementsByClassName("add-sup");
for (let i = 0; i < add_sup_ajax.length; i++) {
  add_sup_ajax[i].addEventListener("click", () => {
    itemID = add_sup_ajax[i].dataset.item;
    localStorage.setItem("itemID", itemID);
    $(".sup-item-add").empty();
  });
}

var add_sup_ajax_btn = document.getElementById("add-sup-ajax");
add_sup_ajax_btn.addEventListener("click", (e) => {
  e.preventDefault();

  var sup_name = $("#sup_name_ajax").val();
  var sup_prix = $("#sup_prix_ajax").val();
  var item = localStorage.getItem("itemID");
  var action = $("#add-sup-ajax").data("action");

  console.log("Item-numb", item);

  $.ajax({
    url: "/recette/",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
      sup_name: sup_name,
      sup_prix: sup_prix,
      action: action,
      item: item,
    },
    dataType: "json",
    success: function (response) {
      console.log(response);
      if (response.message == "added") {
        instructionReload("success", `${accomp_id} Ajouter`);
      } else {
        instructionReload("error", `${accomp_id} Exist deja`);
      }
    },

    error: function (error) {
      console.log(error);
    },
  });
  localStorage.removeItem("ItemID");
});

var add_sup_ajax_btn_old = document.getElementById("add-sup-ajax-old");
add_sup_ajax_btn_old.addEventListener("click", (e) => {
  e.preventDefault();
  console.log("REAL TIME BRO");

  var sup_id = $("#id_supplement").val();
  var action = $("#add-sup-ajax-old").data("action");
  var item = localStorage.getItem("itemID");

  console.log("Item-numb", sup_id);

  $.ajax({
    url: "/recette/",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
      sups: sup_id.toString(),
      action: action,
      item: item,
    },
    dataType: "json",
    success: function (response) {
      console.log(response);
      if (response.message == "added") {
        instructionReload("success", `${sup_id} Ajouter`);
      } else {
        instructionReload("error", `${sup_id} Exist deja`);
      }
    },

    error: function (error) {
      console.log(error);
    },
  });

  localStorage.removeItem("ItemID");
  $(".sup-item-add").append(`
  <label for="inputPassword4" class="form-label">Supplement</label>
   {{form.supplement}}
   <small class="text-muted" >Appuyer cmd pour selectioner plusieur ou deselectioner</small>
  `);
});

// OPTION;
var add_opt_ajax = document.getElementsByClassName("add-sup");
for (let i = 0; i < add_sup_ajax.length; i++) {
  add_sup_ajax[i].addEventListener("click", () => {
    itemID = add_opt_ajax[i].dataset.item;
    localStorage.setItem("itemID", itemID);
  });
}

add_opt_btn = document.getElementById("add-opt");
add_opt_btn.addEventListener("click", (e) => {
  e.preventDefault();

  var action = $("#add-opt").data("action");
  var opt_name = $("#opt_name").val();
  var opt_cat = $("#id_choice_category").val();
  var receipe = $("#id_parent_food").val();
  var old_choice = $("#id_choice").val();

  console.log(opt_name, old_choice);

  data = {
    opt_name: opt_name,
    opt_cat: opt_cat,
    receipe: receipe.toString(),
    action: action,
    old_choice: old_choice,
    csrfmiddlewaretoken: csrfToken,
  };

  $.ajax({
    url: "/recette/",
    method: "POST",
    data: data,
    dataType: "json",
    success: function (response) {
      console.log(response);
      if (response.message == "added") {
        instructionReload("success", `${response.choice} Ajouter`);
      } else {
        instructionReload("error", `${response.choice} Exist deja`);
      }
    },

    error: function (error) {
      console.log(error);
    },
  });

  console.log("Let me add option");
});

// OPTION CAT
old_cat_choice = document.getElementById("id_category_opt");
old_cat_choice.addEventListener("change", () => {
  console.log(old_cat_choice.value.length > 0);
  if (old_cat_choice.value.length > 0) {
    $("#cat_opt_name").attr("disabled", true);
    console.log(old_cat_choice.value);
  } else {
    $("#cat_opt_name").removeAttr("disabled");
  }
});
function newCat() {
  var x = document.getElementById("cat_opt_name").value;

  if (x != "") {
    $("#id_category_opt").attr("disabled", true);
  } else {
    $("#id_category_opt").removeAttr("disabled");
  }
}

// Option Choices
old_choice = document.getElementById("id_choice");
old_choice.addEventListener("change", () => {
  console.log(old_cat_choice.value.length > 0);
  if (old_choice.value.length > 0) {
    $("#opt_name").attr("disabled", true);
    console.log(old_choice.value);
  } else {
    $("#opt_name").removeAttr("disabled");
  }
});
function newChoice() {
  var x = document.getElementById("opt_name").value;
  console.log(x);
  if (x != "") {
    $("#id_choice").attr("disabled", true);
  } else {
    $("#id_choice").removeAttr("disabled");
  }
}
