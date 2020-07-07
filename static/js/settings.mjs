/**
 * Settings implementation.
 * Authors: Kevin Katzkowski, Jeffrey Pillmann
 * Last modified: 06.07.2020
 */

const changeUsername = document.getElementById('change-username'),
  deleteAccount = document.getElementById('delete-account'),
  showSuggestions = document.getElementById('show-suggestion'),
  readMessages = document.getElementById('read-messages'),
  systemTheme = document.getElementById('system'),
  lightTheme = document.getElementById('light'),
  darkTheme = document.getElementById('dark'),
  deleteGameProgress = document.getElementById('delete-game-progress'),
  gpt2Output = document.getElementById('gpt2-output'),
  settings = {
    username: "",
    showSuggestions: "",
    readMessages: "",
    userTheme: "",
    gpt2Output: ""
  };

// get from database or set initially
getSetttingsJSON(null);

changeUsername.addEventListener('click', () => {
  console.log("changeUsername");
}, false);

deleteAccount.addEventListener('click', () => {
  console.log("deleteAccount");
}, false);

showSuggestions.addEventListener('click', () => {
  settings.showSuggestions = showSuggestions.checked;
  sendSettingsJSON();
}, false);

readMessages.addEventListener('click', () => {
  settings.readMessages = readMessages.checked;
  sendSettingsJSON();
}, false);

gpt2Output.addEventListener('click', () => {
  settings.gpt2Output = gpt2Output.checked;
  sendSettingsJSON();
}, false);

systemTheme.addEventListener('click', () => {
  settings.userTheme = "system";
  sendSettingsJSON();
}, false);

lightTheme.addEventListener('click', () => {
  settings.userTheme = "light";
  sendSettingsJSON();
}, false);

darkTheme.addEventListener('click', () => {
  settings.userTheme = "dark";
  sendSettingsJSON(); 
}, false);

deleteGameProgress.addEventListener('click', () => {
  console.log("deleteGameProgress");
}, false);


/**
 * Update the interface by checking or unchecking the input elements.
 */
function updateDisplayedSettings() {
  setDisplayedValue(showSuggestions, settings.showSuggestions);
  setDisplayedValue(readMessages, settings.readMessages);
  setDisplayedValue(gpt2Output, settings.gpt2Output);
  setDisplayedValue(document.getElementById(settings.userTheme), settings.userTheme);
}

/**
 * Check or uncheck the specified setting in the interface
 * @param setting the setting to be updated
 * @param value new value
 */
function setDisplayedValue(setting, value) {
  setting.checked = value;
}

function getSettingValue(name) {
  return settings[name] ? settings[name] : null;
}

function getSetttingsJSON(json) {
  // parse JSON String into JS object
  let obj = JSON.parse(json);
  console.log('received settings JSON: ' + JSON.stringify(obj));

  if(obj) {
    // update settings from database
    settings.username = obj.username;
    settings.showSuggestions = obj.showSuggestions;
    settings.readMessages = obj.readMessages;
    settings.gpt2Output = obj.gpt2Output;
    settings.userTheme = obj.userTheme;

    console.log(settings);
    console.log('settings updated from database');
  } else{
    // new account default settings 
    settings.showSuggestions = true;
    settings.readMessages = false;
    settings.gpt2Output = true;
    settings.userTheme = 'system';
  }
  updateDisplayedSettings();
  console.log(settings);
}


function sendSettingsJSON() {
  let xhr = new XMLHttpRequest(), url = '/settings';

  xhr.open('POST', url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.addEventListener('readystatechange', () => {
    // if DONE and OK
    if(xhr.readyState === 4 && xhr.readyState === 200) {
      let json = JSON.parse(xhr.responseText);
      getSetttingsJSON(json);
    }
  });
  let settingsJSON = JSON.stringify(settings); 
  xhr.send(settingsJSON);
}

export { getSettingValue }