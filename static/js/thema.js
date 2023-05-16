document.getElementById("thema").addEventListener("click", function(event) {
  event.preventDefault();

  const modal = document.getElementById("myModal");
  modal.style.display = "block";

  const closeButton = document.getElementsByClassName("close")[0];

  closeButton.addEventListener("click", function() {
    modal.style.display = "none";
  });

  const categoryBox = document.querySelector('.category--box');
  categoryBox.addEventListener('click', function(event) {
    if (event.target.classList.contains('category-icon')) {
      event.target.classList.toggle('selected');
    }
  });

  const natureBox = document.querySelector('.nature--box');
  natureBox.addEventListener('click', function(event) {
    if (event.target.classList.contains('nature-icon')) {
      event.target.classList.toggle('selected');
    }
  });

  const facilityBox = document.querySelector('.facility--box');
  facilityBox.addEventListener('click', function(event) {
    if (event.target.classList.contains('facility-icon')) {
      event.target.classList.toggle('selected');
    }
  });

  const submitBtn = document.getElementById('submitBtn');

  submitBtn.addEventListener('click', function() {
    const selectedCategories = [];
    const selectedNatures = [];
    const selectedFacilities = [];

    const categoryIcons = document.querySelectorAll('.category-icon');
    const natureIcons = document.querySelectorAll('.nature-icon');
    const facilityIcons = document.querySelectorAll('.facility-icon');
    
    categoryIcons.forEach(icon => {
      if (icon.classList.contains('selected')) {
        const category = icon.getAttribute('data-filter');
        selectedCategories.push('category=' + category);
      }
    });

    natureIcons.forEach(icon => {
      if (icon.classList.contains('selected')) {
        const nature = icon.getAttribute('data-filter');
        selectedNatures.push('nature=' + nature);
      }
    });

    facilityIcons.forEach(icon => {
      if (icon.classList.contains('selected')) {
        const facility = icon.getAttribute('data-filter');
        selectedFacilities.push('facility=' + facility);
      }
    });
    
    const url = '/posts/thema/?' +  selectedCategories.join('&') + '&' + selectedNatures.join('&') + '&' + selectedFacilities.join('&');
    window.location.href = url;

  });
});

