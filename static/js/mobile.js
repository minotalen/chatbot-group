let hamburgerMenu = document.getElementById('toggle');
let navbar = document.getElementsByTagName('nav')[0];

/**
 * Mobile Layout Transition Overlay
 */
hamburgerMenu.addEventListener('click', () => {
  let container = document.getElementsByClassName('container')[0];
  if (hamburgerMenu.checked) {
    container.style.filter = "brightness(50%)";
    container.style.top = window.getComputedStyle(navbar, null).getPropertyValue('height');
  } else {
    container.style = "";
  }
});