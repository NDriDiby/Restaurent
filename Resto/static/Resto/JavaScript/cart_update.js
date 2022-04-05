var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
update_but = document.getElementsByClassName("update-cart");

for (let i = 0; i < update_but.length; i++) {
  update_but[i].addEventListener("click", function () {
    var itemId = this.dataset.product;
    var action = this.dataset.action;
    var ingre = this.dataset.ingredient;

    $.ajax({
      url: "/texasgrillz/updateitem/",
      method: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
        itemId: itemId,
        action: action,
        choice: ingre,
      },
      success: function () {
        console.log(itemId, action, ingre);
      },
    });
  });
}
