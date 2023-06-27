/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

$(document).ready(function () {
  var showMore = true; // Set initial state, true = show more

  $(".btn-show-more").on("click", function () {
    var $btn = $(this);
    var $list = $btn.prev(".song-list");

    if (showMore) {
      $list.css("max-height", "none");
      $btn.text("Show Less");
    } else {
      $list.css("max-height", "");
      $btn.text("Show More");
    }

    showMore = !showMore; // Toggle state
  });
});

