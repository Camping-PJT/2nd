window.addEventListener('scroll', scrollFunction);
  
function scrollFunction() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    document.querySelector('#menu').style.top = '0';
  } else {
    document.querySelector('#menu').style.top = '-250px';
  }
}

var scrollButton = document.getElementById("scrollButton");

scrollButton.addEventListener("click", function() {
  if (scrollButton.classList.contains("go-up")) {
    document.documentElement.scrollTo({ top: 0 });
    document.body.scrollTo({ top: 0 });
  } else {
    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
  }
});

window.addEventListener("scroll", function() {
  var viewportHeight = window.innerHeight;
  var contentHeight = document.body.scrollHeight;
  var scrollPosition = window.scrollY;

  if (contentHeight > viewportHeight && scrollPosition > 0) {
    scrollButton.classList.add("go-up");
    scrollButton.classList.remove("go-down");
  } 
  else if (scrollPosition === 0) {
    scrollButton.classList.add("go-down");
    scrollButton.classList.remove("go-up");
  } 
  else {
    scrollButton.classList.add("go-down");
    scrollButton.classList.remove("go-up");
  }
});

