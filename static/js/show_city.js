  const reviews = document.querySelectorAll('#content-list');
  for (let i = 5; i < reviews.length; i++) {
    reviews[i].classList.add('hide');
  }
  const btnMore = document.querySelector('#btn-more');
  const hideClass = 'hide';
  let visibleReviews = 5;

  function showNextReviews() {
    for (let i = visibleReviews; i < visibleReviews + 5 && i < reviews.length; i++) {
      reviews[i].classList.remove(hideClass);
    }
    visibleReviews += 5;
    if (visibleReviews >= reviews.length) {
      btnMore.textContent = '간략히';
    }
  }

  btnMore.addEventListener('click', function() {
    if (visibleReviews >= reviews.length) {
      visibleReviews = 5;
      for (let i = visibleReviews; i < reviews.length; i++) {
        reviews[i].classList.add(hideClass);
      }
      btnMore.textContent = '더보기';
    } else {
      showNextReviews();
    }
  });

  if (reviews.length <= 5) {
    btnMore.classList.add(hideClass);
  }
