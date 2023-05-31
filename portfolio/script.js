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

