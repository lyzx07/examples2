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

// JavaScript code for toggling accordion panels
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function () {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    this.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}
