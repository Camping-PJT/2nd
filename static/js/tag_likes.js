const forms = document.querySelectorAll('[id^="likes-form-"]');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

forms.forEach(function (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    axios({
      method: 'post',
      url: `/posts/${postId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {
        const isLiked = response.data.is_liked;
        const likesCountSpan = form.nextElementSibling;
        likesCountSpan.textContent = response.data.likes_count;
        const heartIcon = form.querySelector('i');
        if (isLiked) {
          heartIcon.classList.remove('bi-suit-heart');
          heartIcon.classList.add('bi-suit-heart-fill');
        } else {
          heartIcon.classList.remove('bi-suit-heart-fill');
          heartIcon.classList.add('bi-suit-heart');
        }
      })
      .catch((error) => {
        console.error(error);
      });
  });
});

