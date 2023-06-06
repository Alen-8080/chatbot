document.addEventListener("DOMContentLoaded", function() {
  // Get references to the chat area and the prompt input field
  const chatArea = document.getElementById('chat-area');
  const promptInput = document.getElementById('prompt-input');

  // Function to display a user message in the chat area
  function displayUserMessage(message) {
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.innerHTML = `
      <div class="avatar">
        <img src="user-logo.png" alt="User Avatar" class="logo">
      </div>
      <p> ${message} </p>`;
    chatArea.appendChild(userMessage);
  }

  // Function to display the relevant information in the chat area
  function displayRelevantInfo(relevantInfo) {
    const infoMessage = document.createElement('div');
    infoMessage.classList.add('message', 'bot-message');
    infoMessage.innerHTML = `
      <div class="avatar">
        <img src="ktu-logo.png" alt="Chatbot Avatar" class="logo">
      </div>
      <p> ${relevantInfo} </p>`;
    chatArea.appendChild(infoMessage);
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
      .then((response) => response.json())
      .then((data) => {
        // Display the relevant information in the chat area
        displayRelevantInfo(data.relevant_info);
      })
      .catch((error) => {
        console.error('Error:', error);
      });

    promptInput.value = ''; // Clear the input field
  }

  // Attach the form submission handler to the submit button
  document.getElementById('submit-button').addEventListener('click', handleFormSubmit);
});
