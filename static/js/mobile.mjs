/**
 * Script for mobile layout.
 * Authors: Jeffrey Pillmann, Kevin Katzkowski
 * Updated: 12.08.2020
 */

const hamburgerMenu = document.getElementById('toggle');
const navbar = document.getElementsByTagName('nav')[0];
const container = document.getElementsByClassName('container')[0];
const navlist = document.getElementById('nav-links');

/**
 * Mobile Layout Transition Overlay
 */
hamburgerMenu.addEventListener('click', () => {
  if (hamburgerMenu.checked) {
    navlist.classList.add('expanded');
    container.style.filter = "brightness(50%)";
  } else {
    container.style = "";
    navlist.classList.remove('expanded');
  }
});

container.addEventListener('touchstart', (evt) => {
  if (container.style.filter == "brightness(50%)") {
    evt.preventDefault();
    container.style = "";
  }
});