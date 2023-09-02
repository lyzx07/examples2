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
      if (creator.index() === 0) {
        details.slideToggle("slow");
      } else {
        details.toggle("slow");
      }

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

/* document.addEventListener("DOMContentLoaded", function() {
  var moreText = document.getElementById("more");
  var btnText = document.getElementById("myBtn");

  btnText.addEventListener("click", function() {
    if (moreText.style.display === "none") {
      moreText.style.display = "block";
      btnText.innerHTML = "Minimize";
    } else {
      moreText.style.display = "none";
      btnText.innerHTML = "Add or Modify Ratings for this Creator";
    }
  });
}); */

function myFunction() {
  var moreText = document.getElementById("more");
  var btnText = document.getElementById("myBtn");

  if (moreText.style.display === "none") {
    moreText.style.display = "block";
    btnText.innerHTML = "Minimize";
  } else {
    moreText.style.display = "none";
    btnText.innerHTML = "Add or Modify Ratings for this Creator";
  }
}

btnText.addEventListener("click", function() {
  myFunction();
});


function myFunction2() {
  var moreText = document.getElementById("more2");
  var btnText = document.getElementById("myBtn2");

  if (moreText.style.display === "none") {
    moreText.style.display = "block";
    btnText.innerHTML = "Minimize";
  } else {
    moreText.style.display = "none";
    btnText.innerHTML = "Add Notes or Pick Highlighted Note for this Creator";
  }
}

btnText.addEventListener("click", function() {
  myFunction2();
});




