const submitButton = document.getElementById("submit-button");
const startButton = document.getElementById("start-button");
const downloadButton = document.getElementById("download-conversation");
const darkModeToggle = document.getElementById("dark-mode-toggle");

function submitAnswer() {
  // Submit answer logic here
  const answerInput = document.getElementById("answer-input").value;
  console.log("Submitted answer:", answerInput);
}

function startAssessment() {
  // Start assessment logic here
  console.log("Assessment started");
}

function downloadConversation() {
  // Download conversation logic here
  console.log("Conversation downloaded");
}

function toggleDarkMode() {
  // Toggle dark mode logic here
  console.log("Dark mode toggled");
}

submitButton.addEventListener("click", submitAnswer);
startButton.addEventListener("click", startAssessment);
downloadButton.addEventListener("click", downloadConversation);
darkModeToggle.addEventListener("click", toggleDarkMode);
