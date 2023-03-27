let text = document.getElementById('text');
let pic1 = document.getElementById('pic1');
let pic2 = document.getElementById('pic2');

window.addEventListener('scroll', () => {
    let value = window.scrollY;

    text.style.marginTop = value * 2.5 + 'px';
    pic1.style.bottom = value * 1.5 + 'px';
    pic1.style.right = value * -1.5 + 'px';
    pic2.style.left = value * -1.5 + 'px';
    pic2.style.bottom = value * 1.5 + 'px';
})