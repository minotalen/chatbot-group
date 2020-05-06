/**
 * Client-side script to receive, send and display messages.
 * Authors: ?, Katja Schneider, Kevin Katzkowski
 * Last modfidied: 06.05.2020
 */


var socket = io.connect("http://127.0.0.1:5000");


socket.on('connect', function () {
    console.log("connected client");
});



/**
 * Display received message from server in chat interface.
 */
socket.on('message', function(msg) {
  let chat = document.getElementById('chat-content-container');
  chat.append('<li>'+msg+'</li>');
});