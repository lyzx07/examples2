let text = document.getElementById("text");
let pic1 = document.getElementById("pic1");
let pic2 = document.getElementById("pic2");

window.addEventListener("scroll", () => {
  let value = window.scrollY;

  text.style.marginBottom = value * 2.5 + "px";
  pic1.style.bottom = value * 1.5 + "px";
  pic1.style.right = value * -1.5 + "px";
  pic2.style.left = value * -1.5 + "px";
  pic2.style.bottom = value * 1.5 + "px";
});

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("btn-modal");

var link = document.getElementById("link-modal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function () {
  modal.style.display = "block";
};

link.onclick = function () {
  modal.style.display = "block";
  modal.style.background = "black";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};


document.addEventListener('DOMContentLoaded', function() {
  const inputs = document.querySelectorAll('.raised');

  for (const input of inputs) {
    input.addEventListener('input', function() {
      const label = document.querySelector('label[for="' + input.id + '"]');

      if (input.value.trim() !== '') {
        label.style.top = '-5px';
      } else {
        label.style.top = '0px';
      }
    });
  }
});
