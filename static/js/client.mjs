/**
 * Client-side script to receive, send and display messages.
 * Authors: ?, Katja Schneider, Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modified: 18.06.2020
 */

import {
  closeSuggestions,
  userInput
} from './suggestions.mjs';


let socket = io.connect("http://127.0.0.1:5000"),
  sendButton = document.getElementById('send-button'),
  userName = undefined,
  levelID = 'test_level_ID',
  senderName = 'test_sender_name',
  roomName = 'test_room_name',
  modeName = 'test_mode',
  msg,
  typeIndicator = document.getElementById('type-indicator'),
  userMessageSendingAllowed = true;


socket.on('connect', function () {
  console.log('connected client');
  userName = document.getElementById('username').innerText;
  console.log(userName);
  socket.emit('username', userName);
});


/**
 * Display received message from socket in chat interface.
 */
socket.on('json', (json) => {
  console.log('message received');
  msg = readJSON(json);
  userMessageSendingAllowed = true;

  updateMode();
  updateRoomName();
  // updateCurrentLevel(levelID);
  printMessage(msg);
});


/**
 * Handle send button click event.
 */
sendButton.addEventListener('click', () => {
  sendMessage();
}, false);


/**
 * Sends the message from the chat input to the socket.
 */
function sendMessage(evt = 'json') {
  let json;

  if (!userMessageSendingAllowed) {
    console.log('message sending forbidden, no message sent!');
    return;
  }

  msg = userInput.value;

  // set user as sender on outgoing messages
  senderName = 'user';

  // send JSON String to socket
  if (msg.trim() != '') {
    json = createJSON(msg);
    socket.emit(evt, json);
    console.log('message ' + msg + ' has been sent!');
    userInput.value = null;
    closeSuggestions();

    printMessage(msg);
    userInput.focus();
    userMessageSendingAllowed = false;
  } else {
    console.log('no message to send!');
  }
}


/**
 * Prints the message into the chat.
 * @param {String} msg the message to print 
 */
function printMessage(msg) {
  let chat = document.getElementById('chat-content-container'),
    elem = window.document.createElement('li');

  elem.innerHTML = msg;

  // set message type depending on sender 
  switch (senderName) {

    case 'bot': // zum testen auf 'bot' setzen, solange kein inventory sender name vorhanden ist
      elem.className = 'chat-message-inventory';

      // p for sender name
      let p = document.createElement('p');
      p.className = 'chat-message-inventory';
      p.className = 'chat-message-sender-name';
      p.innerHTML = senderName;
      elem.prepend(p);

      typeIndicator.style.visibility = 'hidden';

      // remove bottom margin since element size works as bottom spacing when visiblity is set to hidden
      typeIndicator.style.marginBottom = '0';

      // typewriter effect  
      // writeEachChar(elem, msg);
      break;

    case 'bot':
      elem.className = 'chat-message-bot';
      typeIndicator.style.visibility = 'hidden';

      // remove bottom margin since element size works as bottom spacing when visiblity is set to hidden
      typeIndicator.style.marginBottom = '0';

      // typewriter effect  
      // writeEachChar(elem, msg);
      break;

    default:
      elem.className = 'chat-message-user';
      typeIndicator.style.visibility = 'visible';

      // add margin equal to element size for consistent bottom spacing
      typeIndicator.style.marginBottom = typeIndicator.getBoundingClientRect().height + 'px';
      // elem.innerHTML = msg;
      break;
  }

  chat.insertBefore(elem, typeIndicator);

  // scroll to bottom
  chat.scrollTop = chat.scrollHeight - chat.clientHeight;
}


/**
 * Updates the new game mode for the interface.
 */
function updateMode() {
  if (modeName != 'riddle' && modeName != 'phone') {
    document.documentElement.setAttribute('data-mode', '')
  } else {
    document.documentElement.setAttribute('data-mode', modeName);
  }
}


/**
 * Updates the room name.
 */
function updateRoomName() {
  let rName = document.getElementById('room-name');
  rName.innerHTML = roomName;
}


/**
 * Updates the currently level.
 * @param {String} level new level
 */
function updateCurrentLevel(level) {
  let currentLevel = document.getElementById('level');
  console.log(currentLevel);

  currentLevel.innerHTML = level;
}


/**
 * Creates a new JSON String using the data from client variables and the specified message.
 * @param {String} msg the message to be transported in the JSON String
 * @returns {JSON String} the generated JSON String 
 */
function createJSON(msg) {
  let obj, json;

  // create object to parse into JSON
  obj = {
    level: levelID,
    sender: senderName,
    room: roomName,
    mode: modeName,
    message: msg
  };

  // parse object into JSON String
  json = JSON.stringify(obj);
  console.log('parsed JSON String: ' + json);

  return json;
}


/**
 * Reads a JSON String, stores its data in client variables and returns the message.
 * @param {JSON String} json the JSON String
 * @returns {String} the message transported in the JSON String 
 */
function readJSON(json) {
  // parse JSON String into JS object
  let message, obj = JSON.parse(json);
  console.log('received JSON String: ' + JSON.stringify(obj));

  // update client variables
  levelID = obj.level;
  senderName = obj.sender;
  roomName = obj.room;
  modeName = obj.mode;
  message = obj.message;

  console.log('received message: ' + message);
  return message;
}


/**
 * Writes each char of the message individually into the element.
 * @param {HTML element} elem The HTML element where the message shall be added.
 * @param {String} msg The message to be written. 
 */
function writeEachChar(elem, msg) {
  if (msg.length > 0) {
    elem.innerHTML += msg.charAt(0);
    msg = msg.slice(1, msg.length)

    setTimeout(() => {
      writeEachChar(elem, msg)
    }, 30);
  }
}


/**
 * Close input field suggestions on click outside of input field.
 */
window.addEventListener('click', (evt) => {
  // console.log(evt.target);

  // console.log('window click');
  if (evt.target.id != 'input-user') closeSuggestions();
  // if (!document.getElementById('settings-window').contains(evt.target) && !evt.path.includes(document.getElementById('settings'))) closeSettings();
}, false);


window.addEventListener('keyup', (evt) => {
  evt.preventDefault(); // ???????
});


export {
  sendButton
}