/**
 * Settings implementation.
 * Authors: Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modfidied: 20.05.2020
 */

let settingsButton = document.getElementById('settings'),
  settingsWindow = document.getElementById('settings-window'),
  closeSettingsButton = document.getElementById('close-settings');


settingsButton.addEventListener('click', toggleSettingsWindow, false);
closeSettingsButton.addEventListener('click', toggleSettingsWindow, false);


/**
 * Toggle visibility of settings window.
 */
function toggleSettingsWindow() {
  if(settingsWindow.style.display == 'block') {
    closeSettings();
  } else {
    settingsWindow.style.display = 'block';
  }
}


/**
 * Close settings window.
 */
function closeSettings() {
  settingsWindow.style.display = 'none';
}


export { closeSettings }