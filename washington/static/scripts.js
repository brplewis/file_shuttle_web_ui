$(document).ready(function(){
    var socket = io();
    socket.on('my response', function(msg) {
        $('#log').append(msg.data);
    });
