const socket = new WebSocket('ws://localhost:8000/ws/notify/');

// Set custom headers before opening the connection
socket.onbeforeopen = function(event) {
  socket.setRequestHeader('authorization', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2MTY0NjYwLCJqdGkiOiI4Y2ZmYWRiN2NkYTA0NmZmYmYxNjNhMzcwODQ2MDQxZiIsInVzZXJfaWQiOjN9.WEq6ngxMKmg5SN-E_IOjFRLx314q7zOqyvLVaH2pOxY');
};

socket.onopen = function() {
  console.log('WebSocket connection established.');
};

socket.onmessage = function(event) {
  const message = event.data;
  updateMessageContainer(message);
};

socket.onclose = function(event) {
  console.log('WebSocket connection closed:', event);
};

socket.onerror = function(error) {
  console.error('WebSocket error:', error);
};

function updateMessageContainer(message) {
  const messageContainer = document.getElementById('message-container');
  messageContainer.innerHTML += `<p>${message}</p>`;
}