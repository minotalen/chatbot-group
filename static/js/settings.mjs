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
    showSuggestions: true, // TODO default settings can be changed here 
    readMessages: false,
    gpt2Output: true,
    userTheme: 'system'
  },
  settingsUrl = '/settings';

// TODO rework this function to get username from server
function getUsernameFromURL() {
  let current_url = window.location.href, 
  url = new URL(current_url);
  return url.searchParams.get('username');
}

settings.username = getUsernameFromURL();

// get from database or set initially
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
  console.log(setting);
  
  setting.checked = value;
}

function getSettingValue(name) {
  return settings[name] ? settings[name] : null;
}

function getSettingsJSON() {  
  let xhttp = new XMLHttpRequest(), obj; 

  xhttp.open('GET', settingsUrl, true);
  xhttp.addEventListener('readystatechange', () => {
    if(xhttp.readyState === 4 ) {
      obj = JSON.parse(xhttp.responseText);
      console.log(obj);
      console.log(xhttp.responseText);
      
      updateSettingsObj(obj);
    }
  });
  xhttp.send();
}

let o = {username: "f", showSuggestions: false, readMessages: false, userTheme: "system", gpt2Output: true};
document.addEventListener('DOMContentLoaded', function() {
  console.log("DOM fully loaded and parsed");
  // updateSettingsObj(o);
}); 

function updateSettingsObj(obj) {
  // let obj = JSON.parse(json);
  // console.log('received settings JSON: ' + JSON.stringify(obj));

  if(obj.username != undefined) { // TODO replace
    // update settings from database
    settings.username = document.getElementById('username').innerText; //obj.username;
    console.log(settings.username);
    
    settings.showSuggestions = obj.showSuggestions;
    settings.readMessages = obj.readMessages;
    settings.gpt2Output = obj.gpt2Output;
    settings.userTheme = obj.userTheme;

    console.log(settings);
    console.log('settings updated from database');
  } 
  updateDisplayedSettings();
  console.log(settings);
}


function sendSettingsJSON() {
  let xhr = new XMLHttpRequest(), obj, settingsJSON;
  console.log(settings);

  xhr.open('POST', settingsUrl, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.addEventListener('readystatechange', () => {
    // if DONE and OK
    if(xhr.readyState === 4 && xhr.readyState === 200) {
      obj = JSON.parse(xhr.responseText);
      console.log(obj);
      
      // TODO reactivate this when database is working
      updateSettingsObj(obj);
    }
  });
  settingsJSON = JSON.stringify(settings); 
  xhr.send(settingsJSON);
}

export { getSettingValue }