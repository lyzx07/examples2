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

//I added the newly updated watched variable to the add and delete routes 
//but i still need to somehow update the watched variable for the watched tablelist.
//mybe with another ajax request or to modify current request

document.addEventListener("DOMContentLoaded", function () {
  fetch("/watched")
    .then((response) => response.json())
    .then((data) => {
      const watched = data.watched;
      console.log(watched);
      // Function to check checkboxes based on videoId
      function checkCheckboxes(videoId, isChecked) {
        // Select all checkboxes with the same video ID
        const associatedCheckboxes = document.querySelectorAll(
          `.toggle-song[data-video-id="${videoId}"]`
        );
        associatedCheckboxes.forEach((associatedCheckbox) => {
          // Update the checked state of all associated checkboxes
          associatedCheckbox.checked = isChecked;
        });
      }
      // Call the function for each videoId in the watched variable
      watched.forEach((videoId) => {
        checkCheckboxes(videoId, true);
      });
    });
});

// Add event listener to checkboxes
const checkboxes = document.querySelectorAll(".toggle-song");
checkboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", function () {
    const isChecked = this.checked;
    const songTitle = this.parentElement.previousElementSibling.textContent;
    const videoId = checkbox.dataset.videoId;

    console.log(videoId);
    console.log(songTitle);

    // Select all checkboxes with the same video ID
    const associatedCheckboxes = document.querySelectorAll(
      `.toggle-song[data-video-id="${videoId}"]`
    );
    associatedCheckboxes.forEach((associatedCheckbox) => {
      // Update the checked state of all associated checkboxes
      associatedCheckbox.checked = isChecked;
    });

    const data = {
      title: songTitle,
      videoId: videoId,
    };

    console.log(data);

    if (isChecked) {
      // Checkbox is checked, save the song to the database
      const xhr = new XMLHttpRequest();
      xhr.open("POST", "/save-song", true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          console.log(response.message);
        }
      };
      xhr.send(JSON.stringify(data));
    } else {
      // Checkbox is unchecked, remove the song from the database
      const xhr = new XMLHttpRequest();
      xhr.open("POST", "/remove-song", true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          console.log(response.message);
        }
      };
      xhr.send(JSON.stringify(data));
    }
  });
});

var openDialogButton = document.getElementById('open-dialog-btn');

var dialogCont = document.getElementById('dialog-watched');

var closeDialog = document.getElementById('close-dialog-btn');

// "Open dialog box" button opens the <dialog> modally
openDialogButton.addEventListener('click', function () {
  if (typeof dialogCont.showModal === "function") {
    dialogCont.showModal();
  } else {
    console.log("The <dialog> API is not supported by this browser");
  }
});

closeDialog.addEventListener('click', function() {
  dialogCont.close();
})

dialogCont.addEventListener("click", event => {
  const rect = dialogCont.getBoundingClientRect();
  if (event.clientY < rect.top || event.clientY > rect.bottom ||
      event.clientX < rect.left || event.clientX > rect.right) {
      dialogCont.close();
  }
});

