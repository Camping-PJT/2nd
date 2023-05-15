const l_forms = document.querySelectorAll('[id^="review-likes-form-"]');
const r_l_csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

l_forms.forEach(function (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();

    const reviewId = event.target.dataset.reviewId;
    axios({
      method: 'post',
      url: `/reviews/${reviewId}/likes/`,
      headers: { 'X-CSRFToken': r_l_csrftoken },
    })
      .then((response) => {
        const risLiked = response.data.r_is_liked;
        const reviewlikesCountSpan = form.nextElementSibling;
        const thumbsupIcon = form.querySelector('#review-up');
        const dislikeForm = document.querySelector(`#review-dislikes-form-${reviewId}`);

        if (risLiked) {
          thumbsupIcon.classList.remove('bi-hand-thumbs-up');
          thumbsupIcon.classList.add('bi-hand-thumbs-up-fill');
          dislikeForm.querySelector('button').disabled = true;
        } else {
          thumbsupIcon.classList.remove('bi-hand-thumbs-up-fill');
          thumbsupIcon.classList.add('bi-hand-thumbs-up');
          dislikeForm.querySelector('button').disabled = false;
        }

        reviewlikesCountSpan.textContent = response.data.review_likes_count;
      })
      .catch((error) => {
        console.error(error);
      });
  });
});

const d_forms = document.querySelectorAll('[id^="review-dislikes-form-"]');
const r_d_csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

d_forms.forEach(function (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();

    const reviewId = event.target.dataset.reviewId;
    axios({
      method: 'post',
      url: `/reviews/${reviewId}/dislikes/`,
      headers: { 'X-CSRFToken': r_d_csrftoken },
    })
      .then((response) => {
        const risdisLiked = response.data.r_is_disliked;
        const reviewdislikesCountSpan = form.nextElementSibling;
        const thumbsdownIcon = form.querySelector('#review-down');
        const likeForm = document.querySelector(`#review-likes-form-${reviewId}`);

        if (risdisLiked) {
          thumbsdownIcon.classList.remove('bi-hand-thumbs-down');
          thumbsdownIcon.classList.add('bi-hand-thumbs-down-fill');
          likeForm.querySelector('button').disabled = true;
        } else {
          thumbsdownIcon.classList.remove('bi-hand-thumbs-down-fill');
          thumbsdownIcon.classList.add('bi-hand-thumbs-down');
          likeForm.querySelector('button').disabled = false;
        }

        reviewdislikesCountSpan.textContent = response.data.review_dislikes_count;
      })
      .catch((error) => {
        console.error(error);
      });
  });
});