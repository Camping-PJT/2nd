class Carousel {
  constructor() {
    this.index = 0;
    this.$carousel = document.querySelector(".box3--carousel");
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

    if (this.$carousel.childElementCount <= 1) {
      this.$nextButton.hidden = true;
    }

    if (this.index === 0 && this.$carousel.childElementCount > 1) {
      this.$nextButton.hidden = false;
    }
  }

  prev() {
    if (this.index <= 0) return;
    this.index -= 1;

    this.$carousel.style.transform = `translate3d(0, -${
      200 * this.index
    }px, 0)`;

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

    this.$carousel.style.transform = `translate3d(0, -${
      200 * this.index
    }px, 0)`;

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

$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();   
});