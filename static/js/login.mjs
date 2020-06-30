
let signUpLink= document.getElementById('sign-up'),
  loginHeading = document.getElementById('login-heading'),
  loginText = document.getElementById('login-text'),
  form = document.getElementById('login-form'),
  loginButton = document.getElementById('login-button'),
  repeatPassword,
  passwordResetHint;


signUpLink.addEventListener('click', () => {
  repeatPassword ? showLoginMask() : showSignUpMask();
}, false);


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