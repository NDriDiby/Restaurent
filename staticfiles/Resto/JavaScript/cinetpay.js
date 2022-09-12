//var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
var transaction = "PINAVCI" + Math.floor(Math.random() * 10000000).toString();
console.log(transaction);

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
          console.log("Paiement Verified, Redirecring you....", status);
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
    url: "{% url 'process_transaction' %}",
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
    url: "{% url 'cinetpayapi' %}",
    method: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
    },
    dataType: "json",
    success: function (response) {
      console.log(response);
      api = response.apiKey;
      site = response.site_id;
      console.log("responseBACKEND", api, site);
      checkout(api, site, 2000);
      return response;
    },
  });
}

// Checkout apis
function checkout(api, site, pay) {
  CinetPay.setConfig({
    apikey: api, //YOUR APIKEY
    site_id: site, //YOUR_SITE_ID
    notify_url: "http://mondomaine.com/notify/",
    mode: "PRODUCTION",
  });
  CinetPay.getCheckout({
    transaction_id: transaction, // YOUR TRANSACTION ID
    amount: pay,
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
