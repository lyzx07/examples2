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


// these code blocks need to be merged into one

/* // Add event listener to checkboxes
const checkboxes = document.querySelectorAll('.toggle-song');
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', function() {
    const videoId = this.dataset.videoId;
    const isChecked = this.checked;

    if (isChecked) {
      // Checkbox is checked, save the song to the database
      const songTitle = this.parentElement.previousElementSibling.textContent;
      const currentDate = new Date().toISOString().split('T')[0]; // Get current date in YYYY-MM-DD format

      // Send AJAX request to Flask app to save the song
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/save-song', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          console.log(response.message);
        }
      };
      xhr.send(JSON.stringify({ title: songTitle, date: currentDate }));
    } else {
      // Checkbox is unchecked, remove the song from the database
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/remove-song', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          console.log(response.message);
        }
      };
      xhr.send(JSON.stringify({ videoId }));
    }
  });
});

// Add event listener to checkboxes
const checkboxes = document.querySelectorAll('.toggle-song');
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', function() {
    const videoId = this.dataset.videoId;
    const isChecked = this.checked;

    // Select all checkboxes with the same song ID
    const associatedCheckboxes = document.querySelectorAll(`.toggle-song[data-song-id="${videoId}"]`);

    associatedCheckboxes.forEach(associatedCheckbox => {
      // Update the checked state of all associated checkboxes
      associatedCheckbox.checked = isChecked;
      
      // Perform additional actions if needed for each associated checkbox
      // ...
    });

    // Rest of your code...
  });
}); */