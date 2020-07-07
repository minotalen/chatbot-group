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


changeUsername.addEventListener('click', () => {
  console.log("changeUsername");
}, false);

deleteAccount.addEventListener('click', () => {
  console.log("deleteAccount");
}, false);

showSuggestions.addEventListener('click', () => {
  settings.showSuggestions = showSuggestions.checked;
}, false);

readMessages.addEventListener('click', () => {
  settings.readMessages = readMessages.checked;
}, false);

gpt2Output.addEventListener('click', () => {
  settings.gpt2Output = gpt2Output.checked;
}, false);

systemTheme.addEventListener('click', () => {
  settings.userTheme = "system";
}, false);

lightTheme.addEventListener('click', () => {
  settings.userTheme = "light";
}, false);

darkTheme.addEventListener('click', () => {
  settings.userTheme = "dark";
}, false);

deleteGameProgress.addEventListener('click', () => {
  console.log("deleteGameProgress");
}, false);


function setValue(setting, value) {
  setting.checked = value;
}