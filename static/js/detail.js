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
      const likeBtn = document.querySelector('#post-heart')
      
      if (isLiked === true) {
        likeBtn.classList.remove('bi-suit-heart');
        likeBtn.classList.add('bi-suit-heart-fill');
      } else {
        likeBtn.classList.remove('bi-suit-heart-fill');
        likeBtn.classList.add('bi-suit-heart');
      }
      const likesCountTag = document.querySelector('#likes-count')
      const likesCountData = response.data.likes_count
      likesCountTag.textContent = likesCountData
    })
})

class Carousel {
  constructor() {
    this.index = 0;
    this.$carousel = document.querySelector("#carousel");
    this.$prevButton = document.querySelector("#prevbtn");
    this.$nextButton = document.querySelector("#nextbtn");

    this.$prevButton.addEventListener("click", () => {
      this.prev();
    });

    this.$nextButton.addEventListener("click", () => {
      this.next();
    });

    if (this.index === 0) {
      this.$prevButton.hidden = true;
    }

    if (this.$carousel.childElementCount <= 4) {
      this.$nextButton.hidden = true;
    }

    if (this.index === 0 && this.$carousel.childElementCount > 4) {
      this.$nextButton.hidden = false;
    }
  }

  prev() {
    if (this.index <= 0) return;
  this.index -= 1;

    this.$carousel.style.transform = `translate3d(-${
      340 * this.index
    }px, 0, 0)`;

    if (this.index <= 0) {
      this.$prevButton.hidden = true;
    } else {
      this.$prevButton.hidden = false;
    }
    if (this.index >= this.$carousel.childElementCount) {
      this.$nextButton.hidden = true;
    } else {
      this.$nextButton.hidden = false;
    }
  }

  next() {
    if (this.index >= this.$carousel.childElementCount) return;
  this.index += 1;

  this.$carousel.style.transform = `translate3d(-${
    340 * this.index
  }px, 0, 0)`;

    if (this.index <= 0) {
      this.$prevButton.hidden = true;
    } else {
      this.$prevButton.hidden = false;
    }
    if (this.index >= this.$carousel.childElementCount - 4) {
      this.$nextButton.hidden = true;
    } else {
      this.$nextButton.hidden = false;
    }
  }
}

const carousel = new Carousel();



