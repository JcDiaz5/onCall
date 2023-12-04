const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Dummy data for demonstration
const dummyMessages = [
    { user: 'Clinic', content: 'Hello User!' },
    { user: 'User', content: 'Hi Clinic! How can I help you?' },
    { user: 'Clinic', content: 'We have an appointment scheduled for you tomorrow.' }
// Add more messages as needed
];

// Display dummy messages on page load
dummyMessages.forEach(message => displayMessage(message));

// Function to display a message in the chat
function displayMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `${message.user}: ${message.content}`;
    messagesContainer.appendChild(messageElement);
}

// Function to send a new message
function sendMessage() {
    const userMessage = messageInput.value;
    if (userMessage.trim() !== '') {
    // For demonstration, assume the user is sending the message
        const newMessage = { user: 'User', content: userMessage };
        displayMessage(newMessage);

    // Clear the input field
        messageInput.value = '';
    }
}

// Event listener for the send button
sendButton.addEventListener('click', sendMessage);