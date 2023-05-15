document.getElementById("thema").addEventListener("click", function(event) {
  event.preventDefault();

  const modal = document.getElementById("myModal");
  modal.style.display = "block";

  const closeButton = document.getElementsByClassName("close")[0];

  closeButton.addEventListener("click", function() {
    modal.style.display = "none";
  });

  const facilityBox = document.querySelector('.facility--box');
  facilityBox.addEventListener('click', function(event) {
    if (event.target.classList.contains('facility-icon')) {
      event.target.classList.toggle('selected');
    }
  });

  const submitBtn = document.getElementById('submitBtn');

  submitBtn.addEventListener('click', function() {
    const selectedFacilities = [];

    const facilityIcons = document.querySelectorAll('.facility-icon');
    
    facilityIcons.forEach(icon => {
      if (icon.classList.contains('selected')) {
        const facility = icon.getAttribute('data-filter');
        selectedFacilities.push('facility=' + facility);
      }
    });
    
    const url = '/posts/thema/?' + selectedFacilities.join('&');
    window.location.href = url;
    
  }
);
});