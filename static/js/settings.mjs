/**
 * Settings implementation.
 * Authors: Kevin Katzkowski, Jeffrey Pillmann, Cedric Nering
 * Last modified: 09.07.2020
 */

import { updateDisplayedSettings } from './profile.js';


const settings = {
    username: undefined,
    showSuggestions: undefined, 
    readMessages: undefined,
    gpt2Output: undefined,
    userTheme: undefined
  },
  settingsUrl = '/settings';

// get settings from database
getSettingsJSON();


function getSettingValue(name) {  
  return settings[name];
}


function setSettingValue(name, value) {
  settings[name] = value;
  sendSettingsJSON();
}

/**
 * Get setting json from database and update the client's settings.
 */
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

/**
 * Send the client's stored settings as json to the database
 */
function sendSettingsJSON() {
  let xhr = new XMLHttpRequest(), obj, settingsJSON;

  xhr.open('POST', settingsUrl, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.addEventListener('readystatechange', () => {
    if(xhr.readyState === 4) {
      obj = JSON.parse(xhr.responseText);
      console.log(obj);
      
      updateSettingsObj(obj);
    }
  });
  settingsJSON = JSON.stringify(settings); 
  xhr.send(settingsJSON);
}


/**
 * Update the client's stored settings from the specified object. 
 * @param obj object with new settings
 */
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

export { getSettingValue, setSettingValue }