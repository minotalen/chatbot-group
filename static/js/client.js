/**
 * Client-side script to receive, send and display messages.
 * Authors: ?, Katja Schneider, Kevin Katzkowski, mon janssen, Jeffrey Pillmann
 * Last modfidied: 07.05.2020
 */


let socket = io.connect("http://127.0.0.1:5000"),
  sendButton = document.getElementById('send-button'),
  userInput = document.getElementById('input-user'),
  chatForm = document.getElementById('chat-input-form'),
  levelID = 'test_level_ID', 
  senderName = 'test_sender_name',
  roomName = 'test_room_name', 
  itemList = [{item:'test_item_name1', action:'test_item_action1'},{item: 'test_item_name2', action: 'test_item_action2'}];


socket.on('connect', function () {
  console.log('connected client');
});

/**
 * Display received message from socket in chat interface.
 */
socket.on('json', (json) => {
  console.log('message received');
  msg = readJSON(json);

  printMessage(msg);
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
  let json, msg = userInput.value;  

  // TODO set senderName == 'user'  per default on outgoing messages

  // send JSON String to socket
  if(msg.trim() != '') {
    json = createJSON(msg);
    socket.emit('json',json);
    console.log('message ' + msg + ' has been sent!');
    userInput.value = null;

    printMessage(msg);
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
  
  // TODO set senderName == 'user'  per default on outgoing messages
  // set message type depending on sender 
  switch (senderName) {
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
    items: itemList,
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
  itemList = obj.items;
  message = obj.message;

  console.log('received message: ' + message);
  
  return message;
}