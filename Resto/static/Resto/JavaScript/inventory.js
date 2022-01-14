function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the link that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}
window.onload = function () {
  document.getElementById("Products").style.display = "none";
  document.getElementById("Dashboard").style.display = "none";
  document.getElementById("AddProducts").style.display = "none";
};

const button = document.getElementById("btn");
const message = document.getElementById("message");
const x = document.getElementById("x");
const para = document.createElement("li");
para.innerHTML = "<span>X</span>";

btn.addEventListener("click", () => {
  message.style.display = "block";
  setTimeout(() => {
    message.style.display = "none";
  }, 5000);

  setTimeout(() => {
    const node = document.createTextNode("pepsi");
    para.appendChild(node);
    const element = document.querySelector("#ul2");
    element.appendChild(para);
    para.style.opacity = 1;
  }, 1000);

  setTimeout(() => {
    para.style.backgroundColor = "rgb(245, 252, 245)";
    para.style.color = "black";
  }, 3000);
});
