

const chat = document.getElementById('chat-demo-container'),
  messageQueue = [];

let demoMsg1 = {
  sender: "bot",
  message:"Hello user and welcome!"
},
  demoMsg2 = {
    sender: "user",
    message:"How can you help me?"
  },
  demoMsg3 = {
    sender: "bot",
    message:"Lets play a game!"
  },
  demoMsg4 = {
    sender: "user",
    message:"Amazing idea!"
  };


function printDemo() {
  messageQueue.push(demoMsg1);
  messageQueue.push(demoMsg2);
  messageQueue.push(demoMsg3);
  messageQueue.push(demoMsg4);
  printMessageQueueHead();
}

// setTimeout(printDemo, 1000);
printDemo();

/**
 * Prints message at the head the queue if allowed and the queue is not empty.
 */
function printMessageQueueHead() {
  console.log(messageQueue.length );
  if (messageQueue.length > 0) {
    let json = messageQueue.shift(),
      msg = json.message,
      sender = json.sender;
    
    printMessage(msg,sender);
  } else {
    let playButton = document.getElementById('play-cta');
    playButton.className += ' visible';
  }
}

/**
 * Prints the message into the chat.
 * @param {String} msg the message to print 
 */
function printMessage(msg,senderName) {
  let elem = window.document.createElement('li');

  // set message type depending on sender 
  switch (senderName) {

    case 'bot':
      elem.className = 'chat-message-bot';
      break;

    default:
      elem.className = 'chat-message-user';
      break;
  }

  

  // if (elem.className == 'chat-message-user') {
  //   elem.innerHTML = msg;
  //   printMessageQueueHead();
  // } else {
  setTimeout(() => {
    chat.appendChild(elem);
    // print message character by character
    writeEachChar(elem, msg, function () {
      printMessageQueueHead();
      console.log('test');
    });
  }, 750);
}


/**
 * Writes each char of the message individually into the element.
 * @param {HTML element} elem The HTML element where the message shall be added.
 * @param {String} msg The message to be written. 
 * @param {Function} callback Function to call after message has been written.
 * @param {String} tag Storage for the tag currently being parsed
 * @param {Int} reverseIndex Index from the end of the string to insert content inbetween tags
 * @param {Int} height // TODO
 */
function writeEachChar(elem, msg, callback, tag = '', reverseIndex = 0, height) { 
  // initially set height to element height
  if(height == undefined) {
    height = elem.getBoundingClientRect().height;
  }

  if (msg.length > 0) {
    let c = msg.charAt(0), html, speed = 30;

    if(elem.getBoundingClientRect().height - height > 0) {
      // scroll to bottom on line break
      chat.scrollTop = chat.scrollHeight - chat.clientHeight;
      height = elem.getBoundingClientRect().height;
    }
    

    if (c == '<') {
      // begin of HTML tag -> start parsing tag
      tag = '<';
      msg = msg.slice(1, msg.length);

      writeEachChar(elem, msg, callback, tag, reverseIndex, height);
    } else if (c == '>') {
      // end of HTML tag -> apply tag depending on cases
      tag += '>';
      msg = msg.slice(1, msg.length);

      if (tag == '<br>') {
        // insert <br> without further action
        elem.innerHTML += tag;
        tag = '';

        writeEachChar(elem, msg, callback, tag, reverseIndex, height);
      } else if (tag.includes('/')) {
        // closing tag parsed -> remove it
        // jump behind closing tag
        reverseIndex -= tag.length;
        tag = '';

        writeEachChar(elem, msg, callback, tag, reverseIndex, height);
      } else {
        html = elem.innerHTML;

        // opening tag parsed -> insert opening and closing tag and jump inbetween the tags
        elem.innerHTML = html.substring(0, html.length - reverseIndex)
          + tag + '</' + tag.slice(1, tag.length)
          + html.substring(html.length - reverseIndex, html.length);

        // jump before closing tag
        reverseIndex += tag.length + 1;
        tag = '';

        writeEachChar(elem, msg, callback, tag, reverseIndex, height);
      }

    } else if (tag != '') {
      // parse tag type (between '<' and '>')
      tag += c;
      msg = msg.slice(1, msg.length);

      writeEachChar(elem, msg, callback, tag, reverseIndex, height);
    } else {
      html = elem.innerHTML;
      msg = msg.slice(1, msg.length);

      // add non-tag character inbetween tags 
      // -> if reverseIndex == 0, the character is appended
      elem.innerHTML = html.substring(0, html.length - reverseIndex)
        + c
        + html.substring(html.length - reverseIndex, html.length);

      setTimeout(() => {
        writeEachChar(elem, msg, callback, tag, reverseIndex, height);
      }, speed);
    }
  } else {
    callback();
  }
}