let hamburgerMenu = document.getElementById('toggle');
let navbar = document.getElementsByTagName('nav')[0];
let container = document.getElementsByClassName('container')[0];

/**
 * Mobile Layout Transition Overlay
 */
hamburgerMenu.addEventListener('click', () => {
  if (hamburgerMenu.checked) {
    container.style.filter = "brightness(50%)";
    container.style.top = window.getComputedStyle(navbar, null).getPropertyValue('height');
  } else {
    container.style = "";
  }
});

container.addEventListener('touchstart', (evt) => {
  if (container.style.filter == "brightness(50%)") {
    evt.preventDefault();
    container.style = "";
  }
  // TODO hier fehlt doch bestimmt was
});