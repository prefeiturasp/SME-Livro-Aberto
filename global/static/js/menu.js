const menuBtn = document.querySelector('.menu-toggle');
const menu = document.getElementById('menu');

menuBtn.onclick = function(e) {
  e.preventDefault();
  menuToggle();
}

function menuToggle() {
  if (menu.classList) {
    menu.classList.toggle('show');
  } else {
    var classes = menu.className.split(' ');
    var existingIndex = classes.indexOf('show');
  
    if (existingIndex >= 0)
      classes.splice(existingIndex, 1);
    else
      classes.push('show');
  
    menu.className = classes.join(' ');
  }
}

document.addEventListener('click', function (e) {
	if (!e.target.matches('.menu-links')) return;
  menuToggle();
}, false);