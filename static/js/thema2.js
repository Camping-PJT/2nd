document.getElementById("thema2").addEventListener("click", function(event) {
  event.preventDefault();

  const modal2 = document.getElementById("myModal2");
  modal2.style.display = "block";

  const closeButton2 = document.getElementsByClassName("close2")[0];

  closeButton2.addEventListener("click", function() {
    modal2.style.display = "none";
  });

  const categoryBoxes2 = document.querySelectorAll('#category2');
  const natureBoxes2 = document.querySelectorAll('#nature2');
  const facilityBoxes2 = document.querySelectorAll('#facility2');

  categoryBoxes2.forEach(box2 => {
    box2.addEventListener('click', function(event) {
      const targetIcon2 = event.target.querySelector('#category-icon2');
      if (targetIcon2) {
        targetIcon2.classList.toggle('selected');
        box2.classList.toggle('selected');
      } else {
        box2.classList.toggle('selected');
      }
    });
  });

  natureBoxes2.forEach(box2 => {
    box2.addEventListener('click', function(event) {
      const targetIcon2 = event.currentTarget.querySelector('#nature-icon2');
      if (targetIcon2) {
        targetIcon2.classList.toggle('selected');
        box2.classList.toggle('selected');
      }
    });
  });

  facilityBoxes2.forEach(box2 => {
    box2.addEventListener('click', function(event) {
      const targetIcon2 = event.currentTarget.querySelector('#facility-icon2');
      if (targetIcon2) {
        targetIcon2.classList.toggle('selected');
        box2.classList.toggle('selected');
      }
    });
  });

  const submitBtn2 = document.getElementById('submitBtn2');

  submitBtn2.addEventListener('click', function() {
    const selectedCategories = [];
    const selectedNatures = [];
    const selectedFacilities = [];

    const categoryIcons = document.querySelectorAll('#category-icon2');
    const natureIcons = document.querySelectorAll('#nature-icon2');
    const facilityIcons = document.querySelectorAll('#facility-icon2');
    
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
