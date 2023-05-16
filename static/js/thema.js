document.getElementById("thema").addEventListener("click", function(event) {
  event.preventDefault();

  const modal = document.getElementById("myModal");
  modal.style.display = "block";

  const closeButton = document.getElementsByClassName("close")[0];

  closeButton.addEventListener("click", function() {
    modal.style.display = "none";
  });

  const categoryBoxes = document.querySelectorAll('.category--box__category');
  const natureBoxes = document.querySelectorAll('.nature');
  const facilityBoxes = document.querySelectorAll('.facility');

  categoryBoxes.forEach(box => {
    box.addEventListener('click', function(event) {
      const targetIcon = event.target.querySelector('.category-icon');
      if (targetIcon) {
        targetIcon.classList.toggle('selected');
        box.classList.toggle('selected');
      } else {
        box.classList.toggle('selected');
      }
    });
  });

  natureBoxes.forEach(box => {
    box.addEventListener('click', function(event) {
      const targetIcon = event.currentTarget.querySelector('.nature-icon');
      if (targetIcon) {
        targetIcon.classList.toggle('selected');
        box.classList.toggle('selected');
      }
    });
  });

  facilityBoxes.forEach(box => {
    box.addEventListener('click', function(event) {
      const targetIcon = event.currentTarget.querySelector('.facility-icon');
      if (targetIcon) {
        targetIcon.classList.toggle('selected');
        box.classList.toggle('selected');
      }
    });
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
