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

