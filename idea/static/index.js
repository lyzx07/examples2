/* let curves = document.getElementById('curves');

window.addEventListener('scroll', () => {
    let value = window.scrollY;

   /* text.style.marginBottom = value * 2.5 + 'px'; */
    /* curves.style.right = value * -1.5 + 'px';
    
}) */ 

const hamburger = document.querySelector(".hamburger-svg");
const sidebar = document.querySelector(".sidebar");

hamburger.addEventListener("click", () => {
  sidebar.classList.toggle("open");
});