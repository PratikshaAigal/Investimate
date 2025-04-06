// === Constants ===
const BOT_NAME = "Investimate";
const PERSON_NAME = "You";
const BOT_IMG = "/static/img/self-love.png";
const PERSON_IMG = "/static/img/person.png";

// === DOM Elements ===
const chatbox = document.getElementById('chatbox');
const chatbot = document.getElementById('chatbot');
const toggleBtn = document.getElementById('chatbot_toggle');
const msgInput = document.querySelector('.msger-input');
const msgForm = document.querySelector('.msger-inputarea');
const clock = document.getElementById('clock');


// === Utility Functions ===
function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function get(selector, root = document) {
  return root.querySelector(selector);
}

function updateClock() {
  if (clock) {
    const now = new Date();
    clock.textContent = formatDate(now);
  }
}
setInterval(updateClock, 1000);

// === Toggle Button Logic ===
toggleBtn.onclick = () => {
  const icons = toggleBtn.querySelectorAll('svg');
  const label = document.getElementById("chat-label");

  chatbot.classList.toggle('collapsed');

  // Toggle SVG icon visibility
  icons.forEach(icon => icon.style.display = icon.style.display === 'none' ? '' : 'none');
//  label.style.display = icon.style.display === 'none' ? '' : 'none'

  // Optional greeting on open
  if (!chatbot.classList.contains('collapsed')) {
   // Chat is OPEN: hide label + greet
    if (label) label.style.display = 'none';
    setTimeout(() => {
      appendMessage(BOT_NAME, BOT_IMG, "left", "Hi! I'm here to help with your investments.");
    }, 500);
  }
  else{
    // Chat is CLOSED: show label
        if (label) label.style.display = 'block';
    }
};





// === Chat Logic ===
msgForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const msgText = msgInput.value.trim();
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgInput.value = "";

  try {
    const response = await fetch('/api/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msgText })
    });

    const data = await response.json();
    if (Array.isArray(data.responses)) {
      data.responses.forEach(msg => appendMessage(BOT_NAME, BOT_IMG, "left", msg));
    } else {
      appendMessage(BOT_NAME, BOT_IMG, "left", data.reply || "Sorry, I didn’t understand that.");
    }
  } catch (error) {
    appendMessage(BOT_NAME, BOT_IMG, "left", "⚠️ Could not reach server.");
  }
});

// === Message Rendering ===
function appendMessage(name, img, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  chatbox.insertAdjacentHTML("beforeend", msgHTML);
  chatbox.scrollTop = chatbox.scrollHeight;
}
