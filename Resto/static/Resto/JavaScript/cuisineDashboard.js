// const body = document.querySelector("body"),
//   sidebar = body.querySelector("nav"),
//   toggle = body.querySelector(".toggle"),
//   searchBtn = body.querySelector(".search-box"),
//   modeSwitch = body.querySelector(".toggle-switch"),
//   modeText = body.querySelector(".mode-text");

// toggle.addEventListener("click", () => {
//   sidebar.classList.toggle("close");
// });

// searchBtn.addEventListener("click", () => {
//   sidebar.classList.remove("close");
// });

// modeSwitch.addEventListener("click", () => {
//   body.classList.toggle("dark");

//   if (body.classList.contains("dark")) {
//     modeText.innerText = "Light mode";
//   } else {
//     modeText.innerText = "Dark mode";
//   }
// });

// function openTab(evt, cityName) {
//   var i, tabcontent, tablinks;

//   tabcontent = document.getElementsByClassName("tabcontent");
//   for (i = 0; i < tabcontent.length; i++) {
//     tabcontent[i].style.display = "none";
//   }

//   tablinks = document.getElementsByClassName("tablinks");
//   for (i = 0; i < tablinks.length; i++) {
//     tablinks[i].className = tablinks[i].className.replace(" active", "");
//   }

//   document.getElementById(cityName).style.display = "block";
//   evt.currentTarget.className += " active";
// }

console.log("CHART.JS");

async function dashBordData() {
  url = "/texasgrillz/dashBoard_data/";
  data = await fetch(url);
  result = await data.json();
  return result;
}

var my_quantity = [];
var my_item = [];
var my_category = [];
const ctx = document.getElementById("pop-items").getContext("2d");
const orderTime = document.getElementById("order-time").getContext("2d");

// DataBar
var data = {
  labels: my_item,
  datasets: [
    {
      label: "Nombre total",
      data: my_quantity,
      backgroundColor: ["#34487A", "#B7BFD5", "#F9F0EE", "#F2C5BD", "#CF5A47"],
      borderColor: ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)", "rgba(75, 192, 192, 1)", "rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)"],
      borderWidth: 1,
      borderColor: "#777",
      hoverBorderWidth: 3,
      hoverBorderColor: "#000",
    },
  ],
};

var options = {
  layout: {
    padding: 10,
  },
  scales: {
    y: {
      beginAtZero: true,
    },
    x: {
      title: {
        color: "rgb(210, 105, 30)",
        display: true,
        text: "Order Items",
      },
    },
    y: {
      title: {
        color: "rgb(210, 105, 30)",
        display: true,
        text: "Nombre Total Vendus",
      },
    },
  },
  plugins: {
    title: {
      display: true,
      text: "Les 5 repas les plus adorés",
      color: "rgb(210, 105, 30)",
      font: {
        size: 18,
        family: "Poppins",
      },
    },
    legend: {
      display: false,
    },
    responsive: true,
  },
};

// Config
var config = {
  type: "bar",
  data,
  options,
};

// Render
dashBordData().then((data) => {
  console.log(data["dashboard"]);
  var topfive = data["dashboard"];

  topfive.forEach((item) => {
    console.log(item.Quantity);
    my_quantity.push(item.Quantity);
    my_item.push(item.item__name);
    my_category.push(item.item__category__name);
  });

  console.log(my_category);
  const myChart = new Chart(ctx, config);
});

var hour = [];
var count = [];

// DataLine
var dataHour = {
  labels: hour,
  datasets: [
    {
      label: "Nombre total",
      data: count,
      backgroundColor: ["#7893AD"],
      borderColor: ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)", "rgba(75, 192, 192, 1)", "rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)"],
      borderWidth: 1.5,
      tension: 0.2,
      fill: true,
      pointRadius: 3.5,
      pointHoverRadius: 5,
      borderColor: "#777",
      hoverBorderWidth: 3,
      hoverBorderColor: "#000",
    },
  ],
};

// Config
var configHour = {
  type: "line",
  data: dataHour,
  options,
};

dashBordData().then((data) => {
  time = data["ordertime"];
  console.log(time);
  time.forEach((item) => {
    hour.push(item.date_ordered__hour);
    count.push(item.count_order);
  });

  const order = new Chart(orderTime, configHour);
});
