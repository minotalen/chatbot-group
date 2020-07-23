/**
 * Settings implementation.
 * Authors: Kevin Katzkowski, Jeffrey Pillmann, Cedric Nering
 * Last modified: 14.07.2020
 */

import { updateDisplayedSettings } from './profile.mjs';


const settings = {
  username: undefined,
  showSuggestions: undefined,
  readMessages: undefined,
  gpt2Output: undefined,
  userTheme: undefined
},
  settingsUrl = '/settings';

// get settings from database
getSettingsJSON(updateTheme);


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
async function getSettingsJSON(callback = undefined) {
  let xhttp = new XMLHttpRequest(), obj;

  xhttp.open('GET', settingsUrl, true);
  xhttp.addEventListener('readystatechange', () => {
    if (xhttp.readyState === 4) {
      try {
        obj = JSON.parse(xhttp.responseText);

        updateSettingsObj(obj);
        sendSettingsJSON();
      }
      catch (e) {
        updateDisplayedSettings();
        console.log(e);
      }
      callback != undefined && callback(); 
    }
  });
  xhttp.send();
}

/**
 * Send the client's stored settings as json to the database
 */
async function sendSettingsJSON() {
  let xhr = new XMLHttpRequest(), obj, settingsJSON;

  xhr.open('POST', settingsUrl, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.addEventListener('readystatechange', () => {
    if (xhr.readyState === 4) {
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

/**
 * Update UI theme from database or from local storage (user logged in or not). 
 */
function updateTheme() {
  let theme = getSettingValue('userTheme');
  const localStorageTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : 'system';
  console.log('local storage theme: ' + localStorageTheme);
  theme = theme != undefined ? theme : localStorageTheme;


  if (theme == 'system' && window.matchMedia) {
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
      document.documentElement.setAttribute('data-theme', 'light')
    } 
  } else if (theme == 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');

    if (theme == 'system') {
      console.log('system theme preference not supported.');
    }
  }
  localStorage.setItem('theme', theme);
  console.log(`theme was set to ${theme}`);
}


export { getSettingValue, setSettingValue, updateTheme }