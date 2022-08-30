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

const ctx = document.getElementById("pop-items").getContext("2d");
const orderTime = document.getElementById("order-time").getContext("2d");
const monthReport = document.getElementById("month-report").getContext("2d");
const revPerMonth = document.getElementById("revPerMonth").getContext("2d");

Chart.defaults.font.size = 10;
Chart.defaults.font.family = "poppins";
Chart.defaults.plugins.title.align = "center";

var my_quantity = [];
var my_item = [];
var my_category = [];
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

var optionsBar = {
  layout: {
    padding: 10,
  },
  scales: {
    y: {
      beginAtZero: true,
    },
    x: {
      title: {
        color: "#34487A",
        display: true,
        text: "Order Items",
      },
    },
    y: {
      title: {
        color: "#34487A",
        display: true,
        text: "Nombre Total Vendus",
      },
    },
  },
  plugins: {
    title: {
      display: true,
      text: "Les 5 repas les plus adorés",
      color: "#CF5A47",
      font: {
        size: 12,
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
  options: optionsBar,
};

// Render
dashBordData().then((data) => {
  var topfive = data["dashboard"];

  topfive.forEach((item) => {
    my_quantity.push(item.Quantity);
    my_item.push(item.item__name);
    my_category.push(item.item__category__name);
  });

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
      backgroundColor: ["#34487A", "#B7BFD5", "#F9F0EE", "#F2C5BD", "#CF5A47"],
      borderColor: ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)", "rgba(75, 192, 192, 1)", "rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)"],
      borderWidth: 1.5,
      tension: 0.2,
      fill: false,
      pointRadius: 5,
      pointHoverRadius: 5,
      borderColor: "#777",
      hoverBorderWidth: 3,
      hoverBorderColor: "#000",
    },
  ],
};

var optionsLine = {
  layout: {
    padding: 10,
  },
  scales: {
    y: {
      beginAtZero: true,
    },
    x: {
      title: {
        color: "#34487A",
        display: true,
        text: "Heure de Commande",
      },
    },
    y: {
      title: {
        color: "#34487A",
        display: true,
        text: "Nombre total de commande",
      },
    },
  },
  plugins: {
    title: {
      display: true,
      text: "Commande par heure",
      color: "#CF5A47",
      font: {
        size: 12,
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
var configHour = {
  type: "line",
  data: dataHour,
  options: optionsLine,
};

dashBordData().then((data) => {
  time = data["ordertime"];
  time.forEach((item) => {
    hour.push(item.date_ordered__hour);
    count.push(item.count_order);
  });

  const order = new Chart(orderTime, configHour);
});

var total_menu = [];
var menu = [];

// // DataRevMenu
var dataRevMenu = {
  labels: menu,
  datasets: [
    {
      label: "Nombre total",
      data: total_menu,
      backgroundColor: ["#34487A", "#B7BFD5", "#F9F0EE", "#F2C5BD", "#CF5A47"],
      borderColor: ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)", "rgba(75, 192, 192, 1)", "rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)"],
      borderWidth: 1.5,
      borderColor: "#777",
      hoverBorderWidth: 3,
      hoverBorderColor: "#000",
    },
  ],
};

var optionsPie = {
  plugins: {
    title: {
      display: true,
      text: "Commande par heure",
      color: "#CF5A47",
      font: {
        size: 12,
        family: "Poppins",
      },
    },
    legend: {
      display: true,
    },
    responsive: true,
    animation: {
      animateScale: true,
      animateRotate: true,
    },
  },
};

// Config
var configRevMenu = {
  type: "doughnut",
  data: dataRevMenu,
  options: optionsPie,
};

console.log(configRevMenu.options);

dashBordData().then((data) => {
  rev_month = data["revPerMenu"];
  console.log(rev_month);
  rev_month.forEach((rev) => {
    menu.push(rev.item__category__name);
    total_menu.push(rev.my_sum);
  });

  const order = new Chart(monthReport, configRevMenu);
});

// Revenue per Month
var month = [];
var rev_tot = [];

// // DataBar
var dataRevPerMonth = {
  labels: month,
  datasets: [
    {
      label: "Nombre total",
      data: rev_tot,
      backgroundColor: ["#34487A", "#B7BFD5", "#F9F0EE", "#F2C5BD", "#CF5A47"],
      borderColor: ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)", "rgba(75, 192, 192, 1)", "rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)"],
      borderWidth: 1,
      borderColor: "#777",
      hoverBorderWidth: 3,
      hoverBorderColor: "#000",
    },
  ],
};

// var optionsBar = {
//   layout: {
//     padding: 10,
//   },
//   scales: {
//     y: {
//       beginAtZero: true,
//     },
//     x: {
//       title: {
//         color: "#34487A",
//         display: true,
//         text: "Order Items",
//       },
//     },
//     y: {
//       title: {
//         color: "#34487A",
//         display: true,
//         text: "Nombre Total Vendus",
//       },
//     },
//   },
//   plugins: {
//     title: {
//       display: true,
//       text: "Les 5 repas les plus adorés",
//       color: "#CF5A47",
//       font: {
//         size: 12,
//         family: "Poppins",
//       },
//     },
//     legend: {
//       display: false,
//     },
//     responsive: true,
//   },
// };

// // Config
var configRevPerMonth = {
  type: "bar",
  data: dataRevPerMonth,
  // options: optionsBar,
};

// // Render
dashBordData().then((data) => {
  var topfive = data["revPerMonth"];

  topfive.forEach((item) => {
    month.push(item.date_added__date__month);
    rev_tot.push(item.my_sum);
  });

  const myChart = new Chart(revPerMonth, configRevPerMonth);
});
