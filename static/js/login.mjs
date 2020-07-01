/**
 * Client-side authentication with login and signup
 * Authors: Kevin Katzkowski
 * Last modified: 30.06.2020
 */

let socket = io.connect("http://127.0.0.1:5000"),
  signUpLink= document.getElementById('sign-up'),
  loginHeading = document.getElementById('login-heading'),
  loginText = document.getElementById('login-text'),
  form = document.getElementById('login-form'),
  loginButton = document.getElementById('login-button'),
  repeatPassword,
  passwordResetHint;

socket.on('connect', function () {
  console.log('connected client');
});

socket.on('user_auth', (json) => {
  let obj = JSON.parse(json);


  console.log('user authorized');
  window.location = 'http://localhost:5000/play/' + obj.username;
});

signUpLink.addEventListener('click', () => {
  repeatPassword ? showLoginMask() : showSignUpMask();
}, false);

loginButton.addEventListener('click', (evt) => {
  evt.preventDefault();

  let username, password, type;

  username = document.getElementById('user-name').value;
  password = document.getElementById('user-password').value;
  type = repeatPassword ? "signup" :  "login";
  console.log(username + ', ' + password + ', ' + type);
  
  sendAuthenticationRequest(username,password,type)
})


function showSignUpMask() {
  // change displayed text contents
  loginHeading.innerHTML = 'Sign Up';
  loginText.innerHTML = 'for free, no email required';
  signUpLink.innerHTML = 'log in instead';
  loginButton.innerHTML = 'Sign Up';

  // create repeat password field
  repeatPassword = document.createElement('input');
  repeatPassword.id = 'repeat-password';
  repeatPassword.type = 'password';
  repeatPassword.placeholder = 'repeat password';

  passwordResetHint = document.createElement('label');
  passwordResetHint.for = 'repear-password';
  passwordResetHint.innerHTML = 'You cannot reset your password.'

  form.insertBefore(repeatPassword, loginButton);
  form.insertBefore(passwordResetHint, loginButton);
}


function showLoginMask() {
  // change displayed text contents
  loginHeading.innerHTML = 'Log in';
  loginText.innerHTML = 'to load your game progress';
  signUpLink.innerHTML = 'sign up instead';
  loginButton.innerHTML = 'Log in';

  // remove repeat password field
  if(passwordResetHint) passwordResetHint.parentNode.removeChild(passwordResetHint);
  repeatPassword.parentNode.removeChild(repeatPassword);
  repeatPassword = undefined;
}

function sendAuthenticationRequest(username, password, type) {
  let obj, json;

  obj = {
    username: username,
    password: password,
    type: type
  }

  json = JSON.stringify(obj);

  socket.emit('user_auth', json);
}