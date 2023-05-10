var button1 = document.querySelector('a[data-anchor="map"]');

button1.addEventListener('click', function(event) {
  event.preventDefault(); 

  var targetElement = document.getElementById('map');

  targetElement.scrollIntoView({
    behavior: 'smooth'
  });
});