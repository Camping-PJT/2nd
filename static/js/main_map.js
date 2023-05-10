function changeImage(element) {
  var className = element.getAttribute("class");
  var img = document.getElementById("Map");

  img.src = "/static/image/" + className + ".gif";
}


var areas = document.getElementsByTagName("area");
for (var i = 0; i < areas.length; i++) {
  areas[i].addEventListener("mouseover", function () {
    changeImage(this);
  });
}