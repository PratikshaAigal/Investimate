const form = document.getElementById('chat-form');
const chatbox = document.getElementById('chatbox');
const input = document.getElementById('userInput');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, 'user-message');
  input.value = '';

  // Send to backend
  try {
    const res = await fetch('http://localhost:8000/api/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    appendMessage(data.reply, 'bot-message');
  } catch (err) {
    appendMessage("❗ Error connecting to Investimate server.", 'bot-message');
  }
});

function appendMessage(text, className) {
  const msg = document.createElement('div');
  msg.className = className;
  msg.textContent = text;
  chatbox.appendChild(msg);
  chatbox.scrollTop = chatbox.scrollHeight;
}
