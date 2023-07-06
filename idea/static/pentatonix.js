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

    // Scroll to the position of the list before the "Show More" button was clicked
    var scrollPosition = $list.offset().top;
    window.scrollTo(0, scrollPosition);
  });
});

/* // Get all checkboxes
const checkboxes = document.querySelectorAll('.toggle-song');
 */
/* // Add event listener to each checkbox
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', () => {
    // Get song ID from data attribute
    const songId = checkbox.dataset.songId;

    // Make AJAX request to save song
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/pentatonix');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = () => {
      if (xhr.status === 200) {
        console.log(xhr.responseText);
      } else {
        console.error(xhr.statusText);
      }
    };
    xhr.send(JSON.stringify({ songId }));
  });
});
 */