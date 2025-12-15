document.addEventListener("DOMContentLoaded", () => {

  const chatBox = document.getElementById("chat-box");
  const inputField = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  let history = [];

  sendBtn.addEventListener("click", sendMessage);
  inputField.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  async function sendMessage() {
    const message = inputField.value.trim();
    if (!message) return;

    appendMessage("user", message);
    inputField.value = "";

    const payload = {
      message: message,
      history: history
    };

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      appendMessage("bot", data.reply);

      history.push({ role: "user", content: message });
      history.push({ role: "assistant", content: data.reply });

    } catch (err) {
      appendMessage("bot", "⚠️ Error connecting to server.");
      console.error(err);
    }
  }

  function appendMessage(role, text) {
    const msg = document.createElement("div");
    msg.className = role;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

});
