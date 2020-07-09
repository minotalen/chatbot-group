/**
 * Settings implementation.
 * Authors: Kevin Katzkowski, Jeffrey Pillmann, Cedric Nering
 * Last modified: 09.07.2020
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
    username: undefined,
    showSuggestions: undefined, 
    readMessages: undefined,
    gpt2Output: undefined,
    userTheme: undefined
  },
  settingsUrl = '/settings';

// get settings from database
getSettingsJSON();


if(changeUsername) {
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
}

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
  if (setting) setting.checked = value;
}

function getSettingValue(name) {
  return settings[name] ? settings[name] : null;
}

function getSettingsJSON() {  
  let xhttp = new XMLHttpRequest(), obj; 

  xhttp.open('GET', settingsUrl, true);
  xhttp.addEventListener('readystatechange', () => {
    if(xhttp.readyState === 4) {
      try {
        obj = JSON.parse(xhttp.responseText);
      
        updateSettingsObj(obj);
        sendSettingsJSON();
      }
      catch(e){
        updateDisplayedSettings();
        console.log(e);
      }
    }
  });
  xhttp.send();
}

function updateSettingsObj(obj) {
  // update settings from database
  settings.username = obj.username;
  settings.showSuggestions = obj.showSuggestions;
  settings.readMessages = obj.readMessages;
  settings.gpt2Output = obj.gpt2Output;
  settings.userTheme = obj.userTheme;

  console.log('settings updated from database');
  updateDisplayedSettings();
}


function sendSettingsJSON() {
  let xhr = new XMLHttpRequest(), obj, settingsJSON;

  xhr.open('POST', settingsUrl, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.addEventListener('readystatechange', () => {
    if(xhr.readyState === 4) {
      obj = JSON.parse(xhr.responseText);
      
      updateSettingsObj(obj);
    }
  });
  settingsJSON = JSON.stringify(settings); 
  xhr.send(settingsJSON);
}

export { getSettingValue }