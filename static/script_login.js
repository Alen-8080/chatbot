var loginForm = document.getElementById("login-form");
loginForm.addEventListener("submit", function(event) {
  event.preventDefault();
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  if (username === "student" && password === "ktu123") {
    window.location.href = "/static/chatbot.html";
  } else {
    document.getElementById("error").innerHTML = "Invalid username or password. Please try again.";
  }
});
