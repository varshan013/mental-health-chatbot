document.addEventListener("DOMContentLoaded", () => {
  const landingScreen = document.getElementById("landing-screen");
  const chatScreen = document.getElementById("chat-screen");
  const chatBoxInner = document.getElementById("chat-box-inner");
  const chatBox = document.getElementById("chat-box");
  const inputField = document.getElementById("user-input");
  const landingInput = document.getElementById("landing-input");
  const landingSendBtn = document.getElementById("landing-send-btn");
  const sendBtn = document.getElementById("send-btn");
  const newChatBtn = document.getElementById("new-chat-btn");
  const suggestionCards = document.querySelectorAll(".suggestion-card");

  let history = [];
  let isLoading = false;

  suggestionCards.forEach((card) => {
    card.addEventListener("click", () => {
      const prompt = card.dataset.prompt;
      if (prompt) startChat(prompt);
    });
  });
    
    landingSendBtn.addEventListener("click", sendLandingMessage);
    landingInput.addEventListener("keydown", (e) => {if (e.key === "Enter") {e.preventDefault();sendLandingMessage();
  }
});

  newChatBtn.addEventListener("click", resetChat);
  sendBtn.addEventListener("click", sendMessage);
  inputField.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  function startChat(initialMessage) {
    showChatScreen();
    sendMessageText(initialMessage);
  }

  function sendLandingMessage() {
  const message = landingInput.value.trim();

  if (!message || isLoading) return;

  landingInput.value = "";

  showChatScreen();

  sendMessageText(message);
}

  function showChatScreen() {
    landingScreen.classList.add("hidden");
    chatScreen.classList.remove("hidden");
    inputField.focus();
  }

  function showLandingScreen() {
    chatScreen.classList.add("hidden");
    landingScreen.classList.remove("hidden");
  }

  function resetChat() {
    history = [];
    chatBoxInner.innerHTML = "";
    inputField.value = "";
    if (landingInput) {
        landingInput.value = "";
    }
    isLoading = false;
    setInputEnabled(true);
    showLandingScreen();
  }

  async function sendMessage() {
    const message = inputField.value.trim();
    if (!message || isLoading) return;
    inputField.value = "";
    await sendMessageText(message);
  }

  async function sendMessageText(message) {
    if (isLoading) return;

    appendMessage("user", message);
    setInputEnabled(false);
    showTypingIndicator();

    const payload = { message, history };

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      removeTypingIndicator();
      appendMessage("assistant", data.reply, data.sources || []);

      history.push({ role: "user", content: message });
      history.push({ role: "assistant", content: data.reply });
    } catch (err) {
      removeTypingIndicator();
      appendMessage("assistant", "Sorry, I couldn't connect to the server. Please try again in a moment.");
      console.error(err);
    } finally {
      setInputEnabled(true);
      inputField.focus();
    }
  }

  function setInputEnabled(enabled) {
    isLoading = !enabled;
    inputField.disabled = !enabled;
    sendBtn.disabled = !enabled;
  }

  function appendMessage(role, text, sources = []) {
    const messageEl = document.createElement("div");
    messageEl.className = `message ${role}`;

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = role === "user" ? "You" : "Companion";
    messageEl.appendChild(label);

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;
    messageEl.appendChild(bubble);

    if (role === "assistant" && sources.length > 0) {
      messageEl.appendChild(buildSourcesBlock(sources));
    }

    chatBoxInner.appendChild(messageEl);
    scrollToBottom();
  }

  function buildSourcesBlock(sources) {
    const wrapper = document.createElement("div");
    wrapper.className = "message-sources";

    const toggle = document.createElement("button");
    toggle.className = "sources-toggle";
    toggle.type = "button";
    toggle.innerHTML = `<span class="sources-toggle-icon">▶</span> ${sources.length} source${sources.length > 1 ? "s" : ""} referenced`;

    const list = document.createElement("div");
    list.className = "sources-list";

    sources.forEach((src) => {
      const item = document.createElement("div");
      item.className = "source-item";

      const name = document.createElement("span");
      name.className = "source-item-name";
      name.textContent = src.source;

      const content = document.createElement("span");
      content.textContent = src.content;

      item.appendChild(name);
      item.appendChild(content);
      list.appendChild(item);
    });

    toggle.addEventListener("click", () => {
      const isOpen = list.classList.toggle("open");
      toggle.classList.toggle("open", isOpen);
    });

    wrapper.appendChild(toggle);
    wrapper.appendChild(list);
    return wrapper;
  }

  function showTypingIndicator() {
    const indicator = document.createElement("div");
    indicator.className = "typing-indicator";
    indicator.id = "typing-indicator";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = "Companion";
    indicator.appendChild(label);

    const bubble = document.createElement("div");
    bubble.className = "typing-bubble";
    bubble.setAttribute("aria-label", "Companion is typing");
    bubble.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
    indicator.appendChild(bubble);

    chatBoxInner.appendChild(indicator);
    scrollToBottom();
  }

  function removeTypingIndicator() {
    const indicator = document.getElementById("typing-indicator");
    if (indicator) indicator.remove();
  }

  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
