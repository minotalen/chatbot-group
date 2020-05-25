/**
 * Settings implementation.
 * Authors: Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modfidied: 25.05.2020
 */

let settingsButton = document.getElementById('settings'),
  settingsWindow = document.getElementById('settings-window'),
  closeSettingsButton = document.getElementById('close-settings'),
  settingsEntries,
  settings = {}; // settings object, stores settings as key/value pairs


// get all settings entries
settingsEntries = Array.from(document.getElementsByClassName('settings-entry'));

// setup event listeners to open and close settings window
settingsButton.addEventListener('click', toggleSettingsWindow, false);
closeSettingsButton.addEventListener('click', toggleSettingsWindow, false);


// add event listener to each checkbox
settingsEntries.forEach(entry => {
  entry.children[0].children[0].addEventListener('change', storeSettings, false);
});


// restore settings from localstorage if existent
if (localStorage.getItem('settings')) {
  settings = JSON.parse(localStorage.getItem('settings'));
  loadSettings();
} else {
  storeSettings();
}


/**
 * Store settings from UI into js object and localstorage.
 */
function storeSettings() {
  let entryValue, entryID;

  settingsEntries.forEach(entry => {
    entryValue = entry.children[0].children[0].checked;
    entryID = entry.children[0].children[0].id;
    settings[entryID] = entryValue;
  });

  localStorage.setItem('settings', JSON.stringify(settings));
}


/**
 * Loads settings from js object into UI.
 */
function loadSettings() {
  let entryID;

  settingsEntries.forEach(entry => {
    entryID = entry.children[0].children[0].id; 
    entry.children[0].children[0].checked = settings[entryID];
  });
}


/**
 * Toggle visibility of settings window.
 */
function toggleSettingsWindow() {
  if (settingsWindow.style.display == 'block') {
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


/**
 * Returns the value of the setting specified by the its id.
 * @param id setting id 
 */
function getSettingValue(id) {
  return settings[id];
}


export { closeSettings }