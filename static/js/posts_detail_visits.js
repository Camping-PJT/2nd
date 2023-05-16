const v_form = document.querySelector('#visits-form');
const v_csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

v_form.addEventListener('submit', function (event) {
  event.preventDefault();
  const postId = event.target.dataset.postId;
  axios({
    method: 'post',
    url: `/posts/${postId}/visits/`,
    headers: {'X-CSRFToken': v_csrftoken},
  })
    .then((response) => {
      const isVisited = response.data.is_visited;
      const visitBtn = document.querySelector(`#post-visit`);

      if (isVisited === true) {
        visitBtn.classList.remove('bi-geo-alt');
        visitBtn.classList.add('bi-geo-alt-fill');
      } else {
        visitBtn.classList.remove('bi-geo-alt-fill');
        visitBtn.classList.add('bi-geo-alt');
      }
      const visitsCountTag = document.querySelector('#visits-count')
      const visitsCountData = response.data.visits_count
      visitsCountTag.textContent = visitsCountData
    })
    .catch((error) => {
      console.log(error.response);
    });
});