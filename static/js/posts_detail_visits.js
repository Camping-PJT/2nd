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
      const visitBtn = document.querySelector(`#visit-${postId}`);

      if (isVisited === true) {
        visitBtn.value = '방문 취소';
      } else {
        visitBtn.value = '방문';
      }
    })
    .catch((error) => {
      console.log(error.response);
    });
});
