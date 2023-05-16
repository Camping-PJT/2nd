  const reviews = document.querySelectorAll('#content-list');
  for (let i = 2; i < reviews.length; i++) {
    reviews[i].classList.add('hide');
  }
  const btnMore = document.querySelector('#btn-more');
  const hideClass = 'hide';
  let visibleReviews = 2;

  function showNextReviews() {
    for (let i = visibleReviews; i < visibleReviews + 2 && i < reviews.length; i++) {
      reviews[i].classList.remove(hideClass);
    }
    visibleReviews += 2;
    if (visibleReviews >= reviews.length) {
      btnMore.textContent = '간략히';
    }
  }

  btnMore.addEventListener('click', function() {
    if (visibleReviews >= reviews.length) {
      visibleReviews = 2;
      for (let i = visibleReviews; i < reviews.length; i++) {
        reviews[i].classList.add(hideClass);
      }
      btnMore.textContent = '더보기';
    } else {
      showNextReviews();
    }
  });

  if (reviews.length <= 2) {
    btnMore.classList.add(hideClass);
  }
