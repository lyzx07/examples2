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

function myFunction() {
  var moreText = document.getElementById("more");
  var btnText = document.getElementById("myBtn");
  var icon1 = document.createElement("ion-icon");
  var icon2 = document.createElement("ion-icon");
  icon1.name = "star-sharp";
  icon2.name = "star-sharp";
  icon1.classList.add("icon1");
  icon2.classList.add("icon2");

  if (moreText.style.display === "none") {
    moreText.style.display = "block";
    btnText.innerHTML = "Minimize";
    btnText.insertBefore(icon1, btnText.firstChild);
    btnText.appendChild(icon2);
  } else {
    moreText.style.display = "none";
    btnText.innerHTML = "Add or Modify Ratings for this Creator";
    btnText.insertBefore(icon1, btnText.firstChild);
    btnText.appendChild(icon2);
  }
}

function myFunction2() {
  var moreText = document.getElementById("more2");
  var btnText = document.getElementById("myBtn2");
  var icon1 = document.createElement("ion-icon");
  var icon2 = document.createElement("ion-icon");
  icon1.name = "document-text";
  icon2.name = "document-text";
  icon1.classList.add("icon1");
  icon2.classList.add("icon2");

  if (moreText.style.display === "none") {
    moreText.style.display = "block";
    btnText.innerHTML = "Minimize";
    btnText.insertBefore(icon1, btnText.firstChild);
    btnText.appendChild(icon2);
  } else {
    moreText.style.display = "none";
    btnText.innerHTML = "Add Notes or Pick Highlighted Note for this Creator";
    btnText.insertBefore(icon1, btnText.firstChild);
    btnText.appendChild(icon2);
  }
}

// Make an AJAX GET request
function makeAjaxRequest() {
  $.ajax({
    url: "/your-endpoint",
    type: "GET",
    dataType: "json",
    success: function (response) {
      // Request was successful
      $("#response-container").text(response.message);
    },
    error: function (xhr, status, error) {
      // Request failed
      console.error("Request failed. Status code: " + xhr.status);
    },
  });
}
