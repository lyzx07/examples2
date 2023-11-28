var colorDivs = document.getElementsByClassName("colors");

for (var i = 0; i < colorDivs.length; i++) {
  var randomColor = getRandomColor();
  colorDivs[i].style.backgroundColor = randomColor;
}

function getRandomColor() {
  var letters = "0123456789ABCDEF";
  var color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}


var colorContDivs = document.querySelectorAll('.color-cont');
var usedPositions = [];

colorContDivs.forEach(function(div) {
  var randomX, randomY, randomSize;
  var maxAttempts = 10;
  var attempts = 0;

  do {
    randomX = Math.random() * (window.innerWidth - 100);
    randomY = Math.random() * (window.innerHeight - 100);
    randomSize = Math.floor(Math.random() * (200 - 60 + 1)) + 60;
    attempts++;
  } while (isOverlapping(randomX, randomY) && attempts < maxAttempts);

  div.style.left = randomX + 'px';
  div.style.top = randomY + 'px';
  div.querySelector('.colors').style.width = randomSize + 'px';
  div.querySelector('.colors').style.height = randomSize + 'px';
  usedPositions.push({ x: randomX, y: randomY });
});

function isOverlapping(x, y) {
  for (var i = 0; i < usedPositions.length; i++) {
    var position = usedPositions[i];
    if (Math.abs(x - position.x) < 100 && Math.abs(y - position.y) < 100) {
      return true;
    }
  }
  return false;
}

