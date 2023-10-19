/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

jQuery(document).ready(function ($) {
  $(".card-cont").each(function () {
    var creator = $(this);
    var toggleBtn = creator.find(".wrap_toggle");
    var hiddenH4 = creator.find("#hidden-h4");
    var hiddenPinned = creator.find("#hidden-pinned");
    var hiddenP = creator.find("#hidden-p");
    toggleBtn.click(function () {
      var details = creator.find(".wrap");
      if (creator.index() === 0) {
        details.slideToggle("slow");
      } else {
        // Minimize the first card cont if it is open
        var firstCardCont = $(".card-cont").eq(0);
        var firstDetails = firstCardCont.find(".wrap");
        if (firstDetails.is(":visible")) {
          firstDetails.slideUp("fast");
          firstCardCont.find(".wrap_toggle").text("Expand Details");
          firstCardCont.find("#hidden-h4").show();
        }

        details.toggle("slow");
      }
      if (toggleBtn.text() == "Expand Details") {
        toggleBtn.html("Hide Details");
        hiddenH4.hide(); // hide the hidden-h4 element
        hiddenPinned.hide();
        hiddenP.hide();
      } else {
        toggleBtn.text("Expand Details");
        hiddenH4.show(); // show the hidden-h4 element
        hiddenPinned.show();
        hiddenP.show();
      }
    });
  });
});

jQuery(document).ready(function ($) {
  $(".card-cont").each(function () {
    var creator = $(this);
    var toggleBtn = creator.find(".wrap_toggle2");
    toggleBtn.click(function (event) {
      event.stopPropagation();
      var details = creator.find(".form4");
      if (creator.index() === 0) {
        details.slideToggle("slow");
      } else {
        details.toggle("slow");
      }

      if (toggleBtn.text() == "Minimize") {
        toggleBtn.html("Add or Modify Ratings for this Creator");
        toggleBtn.prepend(
          '<ion-icon name="star-sharp" class="icon1"></ion-icon>'
        );
        toggleBtn.append(
          '<ion-icon name="star-sharp" class="icon2"></ion-icon>'
        );
      } else {
        toggleBtn.text("Minimize");
        toggleBtn.prepend(
          '<ion-icon name="star-sharp" class="icon1"></ion-icon>'
        );
        toggleBtn.append(
          '<ion-icon name="star-sharp" class="icon2"></ion-icon>'
        );
      }
    });
  });
  // Prevent scrolling to first card cont when closing/minimizing forms
  $(".form4").click(function (event) {
    event.stopPropagation(); // Prevent event bubbling
  });
});

jQuery(document).ready(function ($) {
  $(".card-cont").each(function () {
    var creator = $(this);
    var toggleBtn = creator.find(".wrap_toggle3");
    toggleBtn.click(function () {
      var details = creator.find(".form3");
      if (creator.index() === 0) {
        details.slideToggle("slow");
      } else {
        details.toggle("slow");
      }

      if (toggleBtn.text() == "Minimize") {
        toggleBtn.html("Add Notes or Pick Highlighted Note for this Creator");
        toggleBtn.prepend(
          '<ion-icon name="document-text" class="icon1"></ion-icon>'
        );
        toggleBtn.append(
          '<ion-icon name="document-text" class="icon2"></ion-icon>'
        );
      } else {
        toggleBtn.text("Minimize");
        toggleBtn.prepend(
          '<ion-icon name="document-text" class="icon1"></ion-icon>'
        );
        toggleBtn.append(
          '<ion-icon name="document-text" class="icon2"></ion-icon>'
        );
      }
    });
  });
});

$(document).ready(function () {
  $(".delete-btn").click(function (e) {
    e.preventDefault();
    var form = $(this).closest("form");
    var channelId = form.find('input[name="channel_id"]').val();

    if (confirm("Final chance. All saved notes and ratings will be deleted!")) {
      $.ajax({
        url: "/delete_creator",
        method: "POST",
        data: {
          form_name: "form2",
          channel_id: channelId,
        },
        success: function (response) {
          // Handle the response here
          var parsedResponse = JSON.parse(response);
          if (parsedResponse.status === "success") {
            // Update the page content dynamically
            form.closest(".card-cont").remove();

            // Remove the deleted creator link from the container
            $(".creator-link-cont")
              .find(`a[href="#${channelId}"]`)
              .closest("li")
              .remove();
          } else {
            // Handle deletion error if needed
          }
        },
        error: function (xhr, status, error) {
          // Handle any errors that occur during the AJAX request
        },
      });
    }
  });
});

/* havent tested this yet. need to add highlighted note and change route to json dump instead */

/* $(document).ready(function () {
  $(".add-note-btn").click(function (e) {
    e.preventDefault();
    var form = $(this).closest("form");
    var channelId = form.find('input[name="channel_id"]').val();
    var note = form.find('textarea[name="message"]').val();
    console.log(note);

    $.ajax({
      url: "/add_note",
      method: "POST",
      data: {
        form_name: "form3",
        channel_id: channelId,
        note: note,
      },
      success: function (response) {
        // Handle the response here
        var parsedResponse = JSON.parse(response);
        if (parsedResponse.status === "success") {
          // Update the page content dynamically
          var notesContainer = $("#notes-cont");
          var newNote = document.createElement("li");
          newNote.textContent = note;
          notesContainer.find("#notes-ul").append(newNote);
        } else {
          // Handle addition error if needed
        }
      },
      error: function (xhr, status, error) {
        // Handle any errors that occur during the AJAX request
      },
    });
  });
}); */

// Add an event listener to the input field where the user enters the username
/* $("#form-id-search").on("submit", function(event) {
  event.preventDefault(); // Prevent the default form submission

  var username = $("#username-input").val();

  // Send the entered username to the Flask route
  $.ajax({
    url: "/add_creator",
    method: "POST",
    data: { username: username },
    success: function(response) {
      // Scroll to the card with the matching channel ID
      var channelId = response.channelId;
      $(".card-cont").each(function() {
        var cardId = $(this).attr("id");
        if (cardId === channelId) {
          // Scroll to the card with the matching channel ID
          $(this)[0].scrollIntoView();
          return false; // Exit the loop once a match is found
        }
      });
    },
    error: function(error) {
      console.log(error);
    },
  });
}); */

//maybe create another button for input field to check to see if creator already exists

// JavaScript/jQuery code
$(document).ready(function () {
  $(".creator-link").click(function (event) {
    event.preventDefault();
    var targetId = $(this).attr("href");
    $(targetId)[0].scrollIntoView();
  });
});
