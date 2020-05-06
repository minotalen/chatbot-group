/**
 * Client-side script to receive, send and display messages.
 * Authors: ?, Katja Schneider, Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modfidied: 06.05.2020
 */


let socket = io.connect("http://127.0.0.1:5000"),
  sendButton = document.getElementById('send-button'),
  userInput = document.getElementById('input-user'),
  chatForm = document.getElementById('chat-input-form');


socket.on('connect', function () {
  console.log('connected client');
});

/**
 * Display received message from socket in chat interface.
 */
socket.on('message', (msg) => {
  console.log('message received');
  printMessage(msg, 'bot');
});


sendButton.addEventListener('click', sendMessage, false);

chatForm.addEventListener('submit', (evt) => {
  // prevents default reloading on submit
  evt.preventDefault();
  sendMessage();
});


/**
 * Sends the message from the chat input to the socket.
 */
function sendMessage() {
  let msg = userInput.value;

  // send message to socket
  if(msg != '') {
    socket.send(msg);
    userInput.value = null;
    console.log('message ' + msg + ' has been sent!');
    
    printMessage(msg, 'user');
  } else {
    console.log('no message to send!');
  }
}


/**
 * Prints the message into the chat.
 * @param {String} msg the message to print 
 * @param {String} msgType 'bot' or 'user'; defines which CSS class is added to the <li> element
 */
function printMessage(msg, msgType) {
  let chat = document.getElementById('chat-content-container'),
    elem = window.document.createElement('li');

  elem.innerHTML = msg;

  // set message type
  switch (msgType) {
    case 'bot':
      elem.className = 'chat-message-bot';
      break;
  
    default:
      elem.className = 'chat-message-user';
      break;
    }

  chat.appendChild(elem);

  // scroll to bottom
  chat.scrollTop = chat.scrollHeight - chat.clientHeight;
}