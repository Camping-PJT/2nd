const reviewLikeForms = document.querySelectorAll('.review-like-forms')
const reviewDislikeForms = document.querySelectorAll('.review-dislike-forms')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

reviewLikeForms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault()
    
    const reviewId = event.target.dataset.reviewId
    axios({
      method: 'post',
      url: `/reviews/${ reviewId }/emotes/1/`,
      headers: {'X-CSRFToken': csrftoken,},
    })
    .then((response) => {
      const isChecked = response.data.is_checked
      const emoteCnt = response.data.cnt
      const isAlert = response.data.alert
      const iTag = document.querySelector(`#review-like-${ reviewId }>i`)
      const cntSpanTag = document.querySelector(`#review-like-${ reviewId }>span`)

      if (isChecked === undefined) {
        // 경고창
        alert('로그인 후 이용해주세요.')
      } else if (isAlert) {
        alert('이미 싫어요를 눌렀습니다.')
      } else if (isChecked) {
        iTag.classList.replace('bi-hand-thumbs-up', 'bi-hand-thumbs-up-fill')
        iTag.classList.add('text-orange')
        cntSpanTag.textContent = emoteCnt
      } else {
        iTag.classList.replace('bi-hand-thumbs-up-fill', 'bi-hand-thumbs-up')
        iTag.classList.remove('text-orange')
        cntSpanTag.textContent = emoteCnt
      }
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})
reviewDislikeForms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault()
    
    const reviewId = event.target.dataset.reviewId
    axios({
      method: 'post',
      url: `/reviews/${ reviewId }/emotes/2/`,
      headers: {'X-CSRFToken': csrftoken,},
    })
    .then((response) => {
      const isChecked = response.data.is_checked
      const emoteCnt = response.data.cnt
      const isAlert = response.data.alert
      const iTag = document.querySelector(`#review-dislike-${ reviewId }>i`)
      const cntSpanTag = document.querySelector(`#review-dislike-${ reviewId }>span`)

      console.log(emoteCnt)

      if (isChecked === undefined) {
        // 경고창
        alert('로그인 후 이용해주세요.')
      } else if (isAlert) {
        alert('이미 좋아요를 눌렀습니다.')
      } else if (isChecked) {
        iTag.classList.replace('bi-hand-thumbs-down', 'bi-hand-thumbs-down-fill')
        iTag.classList.add('text-orange')
        cntSpanTag.textContent = emoteCnt
      } else {
        iTag.classList.replace('bi-hand-thumbs-down-fill', 'bi-hand-thumbs-down')
        iTag.classList.remove('text-orange')
        cntSpanTag.textContent = emoteCnt
      }
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})