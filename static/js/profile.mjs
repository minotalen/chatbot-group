/**
 * Proile page implementation.
 * Authors: Kevin Katzkowski, Jeffrey Pillmann
 * Last modified: 14.07.2020
 */

import { getSettingValue, setSettingValue, updateTheme } from './settings.mjs';


const changeUsername = document.getElementById('change-username'),
deleteAccount = document.getElementById('delete-account'),
showSuggestions = document.getElementById('show-suggestion'),
readMessages = document.getElementById('read-messages'),
systemTheme = document.getElementById('system'),
lightTheme = document.getElementById('light'),
darkTheme = document.getElementById('dark'),
deleteGameProgress = document.getElementById('delete-game-progress'),
gpt2Output = document.getElementById('gpt2-output');


if(changeUsername) {
  changeUsername.addEventListener('click', () => {
    console.log("changeUsername");
  }, false);

  deleteAccount.addEventListener('click', () => {
    console.log("deleteAccount");
  }, false);

  showSuggestions.addEventListener('click', () => {
    setSettingValue('showSuggestions', showSuggestions.checked);
  }, false);

  readMessages.addEventListener('click', () => {
    setSettingValue('readMessages', readMessages.checked);
  }, false);

  gpt2Output.addEventListener('click', () => {
    setSettingValue('gpt2Output', gpt2Output.checked);
  }, false);

  systemTheme.addEventListener('click', () => {
    setSettingValue('userTheme', 'system');
    updateTheme();
  }, false);

  lightTheme.addEventListener('click', () => {
    setSettingValue('userTheme', 'light');
    updateTheme();
  }, false);

  darkTheme.addEventListener('click', () => {
    setSettingValue('userTheme', 'dark');
    updateTheme();
  }, false);

  deleteGameProgress.addEventListener('click', () => {
    console.log("deleteGameProgress");
  }, false);
}

/**
 * Update the interface by checking or unchecking the input elements.
 */
function updateDisplayedSettings() {
  setDisplayedValue(showSuggestions, getSettingValue('showSuggestions'));
  setDisplayedValue(readMessages, getSettingValue('readMessages'));
  setDisplayedValue(gpt2Output, getSettingValue('gpt2Output'));
  setDisplayedValue(
    document.getElementById(getSettingValue('userTheme')), 
    getSettingValue('userTheme')
  );
}

/**
 * Check or uncheck the specified setting in the interface
 * @param name the name of the setting to be updated
 * @param value new value
 */
function setDisplayedValue(name, value) {
  if (name) name.checked = value;
}

export { updateDisplayedSettings }