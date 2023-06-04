document.addEventListener("DOMContentLoaded", function() {
  // Get references to the chat area and the prompt input field
  const chatArea = document.getElementById('chat-area');
  const promptInput = document.getElementById('prompt-input');

  // Function to display a user message in the chat area
  function displayUserMessage(message) {
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.innerHTML = `<p>${message}</p>`;
    chatArea.appendChild(userMessage);
  }

  // Function to display a bot message in the chat area
  function displayBotMessage(message) {
    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot-message');
    botMessage.innerHTML = `
      <img src="ktu-logo.png" alt="KTU Logo" class="logo">
      <p>${message}</p>`;
    chatArea.appendChild(botMessage);
  }

  // Function to handle the form submission
  function handleFormSubmit(event) {
    event.preventDefault(); // Prevent form submission

    const userInput = promptInput.value.trim();
    if (userInput === '') {
      return; // Ignore empty user input
    }

    displayUserMessage(userInput); // Display user message in the chat area

    // Send user query to the Python file
    fetch('/', {
      method: 'POST',
      body: new URLSearchParams({ user_input: userInput }),
    })
      .then((response) => response.text())
      .then((data) => {
        // Display the Python reply in the chat area
        displayBotMessage(data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });

    promptInput.value = ''; // Clear the input field
  }

  // Attach the form submission handler to the submit button
  document.getElementById('submit-button').addEventListener('click', handleFormSubmit);
});
