/**
 * Client-side script to receive, send and display messages.
 * Authors: Katja Schneider, Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modified: 21.07.2020
 */

import { closeSuggestions, userInput } from './suggestions.mjs';
import { getSettingValue } from './settings.mjs';


let socket = io.connect("http://127.0.0.1:5000"),
  sendButton = document.getElementById('send-button'),
  typeIndicator = document.getElementById('type-indicator'),
  userName, 
  levelID,
  senderName,
  roomName,
  modeName,
  msg,
  messageQueue = [],
  userMessageSendingAllowed = true,
  botMessagePrintingAllowed = true;


socket.on('connect', function () {
  console.log('connected client');
  userName = getSettingValue('username'); 
  socket.emit('username', userName);
});


/**
 * Display received message from socket in chat interface.
 */
socket.on('json', (json) => {
  console.log('message received');

  messageQueue.push(json);
  printMessageQueueHead();
});


/**
 * Handle send button click event.
 */
sendButton.addEventListener('click', sendMessage, false);

/**
 * Sends the message from the chat input to the socket.
 */
function sendMessage() {
  let json, evt = 'json';

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
 * Prints message at the head the queue if allowed and the queue is not empty.
 */
function printMessageQueueHead() {
  if (botMessagePrintingAllowed && messageQueue.length > 0) {
    let json = messageQueue.shift();

    botMessagePrintingAllowed = false;
    userMessageSendingAllowed = false;

    msg = readJSON(json);

    updateMode();
    updateRoomName();
    updateCurrentLevel(levelID);
    printMessage(msg);
  } else if (messageQueue.length <= 0) {
    userMessageSendingAllowed = true;
  }
}


/**
 * Prints the message into the chat.
 * @param {String} msg the message to print 
 */
function printMessage(msg) {
  let chat = document.getElementById('chat-content-container'),
    elem = window.document.createElement('li');

  // set message type depending on sender 
  switch (senderName) {

    case 'inventory':
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
      break;

    case 'bot':
      elem.className = 'chat-message-bot';
      typeIndicator.style.visibility = 'hidden';

      // remove bottom margin since element size works as bottom spacing when visiblity is set to hidden
      typeIndicator.style.marginBottom = '0';
      break;

    default:
      elem.className = 'chat-message-user';
      typeIndicator.style.visibility = 'visible';

      // add margin equal to element size for consistent bottom spacing
      typeIndicator.style.marginBottom = typeIndicator.getBoundingClientRect().height + 'px';
      break;
  }

  chat.insertBefore(elem, typeIndicator);

  if (elem.className == 'chat-message-user') {
    elem.innerHTML = msg;
  } else {
    // print message character by character
    writeEachChar(elem, msg, function () {
      botMessagePrintingAllowed = true;
      printMessageQueueHead();
    });
  }

  // scroll to bottom
  chat.scrollTop = chat.scrollHeight - chat.clientHeight;
}


/**
 * Writes each char of the message individually into the element.
 * @param {HTML element} elem The HTML element where the message shall be added.
 * @param {String} msg The message to be written. 
 * @param {Function} callback Function to call after message has been written.
 * @param {String} tag Storage for the tag currently being parsed
 * @param {Int} reverseIndex Index from the end of the string to insert content inbetween tags
 */
function writeEachChar(elem, msg, callback, tag = '', reverseIndex = 0) {
  if (msg.length > 0) {
    let c = msg.charAt(0), html, speed = 30;

    if (c == '<') {
      // begin of HTML tag -> start parsing tag
      tag = '<';
      msg = msg.slice(1, msg.length);

      writeEachChar(elem, msg, callback, tag, reverseIndex);
    } else if (c == '>') {
      // end of HTML tag -> apply tag depending on cases
      tag += '>';
      msg = msg.slice(1, msg.length);

      if (tag == '<br>') {
        // insert <br> without further action
        elem.innerHTML += tag;
        tag = '';

        writeEachChar(elem, msg, callback, tag, reverseIndex);
      } else if (tag.includes('/')) {
        // closing tag parsed -> remove it
        // jump behind closing tag
        reverseIndex -= tag.length;
        tag = '';

        writeEachChar(elem, msg, callback, tag, reverseIndex);
      } else {
        html = elem.innerHTML;

        // opening tag parsed -> insert opening and closing tag and jump inbetween the tags
        elem.innerHTML = html.substring(0, html.length - reverseIndex)
          + tag + '</' + tag.slice(1, tag.length)
          + html.substring(html.length - reverseIndex, html.length);

        // jump before closing tag
        reverseIndex += tag.length + 1;
        tag = '';

        writeEachChar(elem, msg, callback, tag, reverseIndex);
      }

    } else if (tag != '') {
      // parse tag type (between '<' and '>')
      tag += c;
      msg = msg.slice(1, msg.length);

      writeEachChar(elem, msg, callback, tag, reverseIndex);
    } else {
      html = elem.innerHTML;
      msg = msg.slice(1, msg.length);

      // add non-tag character inbetween tags 
      // -> if reverseIndex == 0, the character is appended
      elem.innerHTML = html.substring(0, html.length - reverseIndex)
        + c
        + html.substring(html.length - reverseIndex, html.length);

      setTimeout(() => {
        writeEachChar(elem, msg, callback, tag, reverseIndex);
      }, speed);
    }
  } else {
    callback();
  }
}


/**
 * Updates the new game mode for the interface.
 */
function updateMode() {
  if (modeName != 'riddle' && modeName != 'phone' && mode != 'gps') {
    document.documentElement.setAttribute('data-mode', '');
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
  let levelLabel = document.getElementById('level');
  levelLabel.innerHTML = 'Lvl. ' + level;
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
 * Close input field suggestions on click outside of input field.
 */
window.addEventListener('click', (evt) => {
  if (evt.target.id != 'input-user') closeSuggestions();
}, false);


window.addEventListener('keyup', (evt) => {
  evt.preventDefault(); // ???????
});


export {
  sendButton
}