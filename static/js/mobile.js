let hamburgerMenu = document.getElementById('toggle');

/**
 * Mobile Layout Transition Overlay
 */
hamburgerMenu.addEventListener('click', () => {
  let container = document.getElementsByClassName('container')[0];
  if (hamburgerMenu.checked) {
    container.style.filter = "brightness(50%)";
    container.style.top = "11.75rem";
  } else {
    container.style = "";
  }
});
