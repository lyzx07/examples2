/* $(document).on('scroll', function(){
  $('.logo').css("left", Math.max(540 - 1 * window.scrollY, 25) + "px");
})
 */
const mql = window.matchMedia("(max-width: 768px)");
let isSmallScreen = false;

if (mql.matches) {
  isSmallScreen = true;
}

$(document).on('scroll', function(){
  if (!isSmallScreen) {
    $('.logo').css("left", Math.max(535 - 1 * window.scrollY, 5) + "px");
  }
});