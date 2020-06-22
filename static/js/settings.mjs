/**
 * Settings implementation.
 * Authors: Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modified: 25.05.2020
 */

let settingsButton = document.getElementById('settings'),
  settingsWindow = document.getElementById('settings-window'),
  closeSettingsButton = document.getElementById('close-settings'),
  settingsEntries,
  settings = {}; // settings object, stores settings as key/value pairs

const toggleSwitch = document.getElementById('setting-dark-mode'),
  currentTheme = getStoredTheme();

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
 * Switches between dark and light theme
 */
function switchTheme() {
  let toggle = document.getElementById('setting-dark-mode');
  console.log(toggle);
  if (toggle.checked) {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
  }
}

/**
 * Returns the stored theme, user system preference theme, or null.
 */
function getStoredTheme() {
  let theme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

  // check for user system preference
  if (theme == null) {
    if (!window.matchMedia) {
      theme = null;
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      theme = 'dark';
    } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
      theme = 'light';
    }
  }
  return theme;
}

// check checkbox on page load
if (currentTheme) {
  document.documentElement.setAttribute('data-theme', currentTheme);
  if (currentTheme === 'dark') {
    toggleSwitch.checked = true;
  }
}

toggleSwitch.addEventListener('change', switchTheme, false);


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
 * @param id the HTML ID of the input checkbox element.
 */
function getSettingValue(id) {
  return settings[id];
}




export { closeSettings, getSettingValue }
