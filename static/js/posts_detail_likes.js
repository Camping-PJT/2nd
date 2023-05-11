const form = document.querySelector('#likes-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
form.addEventListener('submit', function (event) {
  event.preventDefault()
  const postId = event.target.dataset.postId
  axios({
    method: 'post',
    url: `/posts/${postId}/likes/`,
    headers: {'X-CSRFToken': csrftoken},
  })
    .then((response) => {
      const isLiked = response.data.is_liked
      const likeBtn = document.querySelector(`#like-${postId}`)
      
      if (isLiked === true) {
        likeBtn.value = '좋아요 취소'
      } else {
        likeBtn.value = '좋아요'
      }
    })
    .catch((error) => {
      console.log(error.response)
    })
})