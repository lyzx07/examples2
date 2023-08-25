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
    toggleBtn.click(function () {
      var details = creator.find(".wrap");
      details.slideToggle("slow");

      if (toggleBtn.text() == "Expand Details") {
        toggleBtn.html("Hide Details");
        hiddenH4.hide(); // hide the hidden-h4 element
      } else {
        toggleBtn.text("Expand Details");
        hiddenH4.show(); // show the hidden-h4 element
      }
    });
  });
});

/* jQuery(document).ready(function ($) {
  $(".card-cont").each(function () {
    var creator = $(this);
    var toggleBtn = creator.find(".wrap_toggle");
    var hiddenH4 = creator.find("#hidden-h4");
    toggleBtn.click(function (event) {
      event.preventDefault(); // prevent the default behavior of the anchor tag
      var details = creator.find(".wrap");
      var cardHeight = creator.outerHeight();
      var windowHeight = $(window).height();
      var scrollAmount = cardHeight - windowHeight;
      $('html, body').animate({
        scrollTop: creator.offset().top - scrollAmount
      }, 1000); // scroll to the card's top minus the window height
      details.slideToggle("slow");

      if (toggleBtn.text() == "Expand Details") {
        toggleBtn.html("Hide Details");
        hiddenH4.hide(); // hide the hidden-h4 element
      } else {
        toggleBtn.text("Expand Details");
        hiddenH4.show(); // show the hidden-h4 element
      }
    });
  });
}); */
