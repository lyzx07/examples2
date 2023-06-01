// Wrap code inside $(document).ready()

$(document).ready(function () {
  const mql = window.matchMedia("(max-width: 768px)");
  let isSmallScreen = false;

  if (mql.matches) {
    isSmallScreen = true;
  }

  $(document).on("scroll", function () {
    if (!isSmallScreen) {
      $(".logo").css("left", Math.max(535 - 1 * window.scrollY, 5) + "px");
    }
  });
});

const images = document.querySelectorAll(".slideshow-images img");

let currentImage = 0;
images[currentImage].classList.add("active");

function slideShow() {
  setInterval(() => {
    images[currentImage].classList.remove("active");
    if (currentImage === images.length - 1) {
      currentImage = 0;
    } else {
      currentImage++;
    }
    images[currentImage].classList.add("active");
  }, 5000);
}

slideShow();

const prev = document.querySelector(".prev");
const next = document.querySelector(".next");

prev.addEventListener("click", () => {
  images[currentImage].classList.remove("active");
  if (currentImage === 0) {
    currentImage = images.length - 1;
  } else {
    currentImage--;
  }
  images[currentImage].classList.add("active");
});

next.addEventListener("click", () => {
  images[currentImage].classList.remove("active");
  if (currentImage === images.length - 1) {
    currentImage = 0;
  } else {
    currentImage++;
  }
  images[currentImage].classList.add("active");
});
