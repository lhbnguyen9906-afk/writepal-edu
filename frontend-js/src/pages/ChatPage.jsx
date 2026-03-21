import { useEffect, useState } from "react";

const API_URL = "https://writepal-edu-production.up.railway.app";

function ChatPage() {
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // tạo conversation
  useEffect(() => {
    async function createConversation() {
      const res = await fetch(`${API_URL}/conversations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: 1 })
      });

      const data = await res.json();
      setConversationId(data.conversation_id);
    }

    createConversation();
  }, []);

  // load messages
  useEffect(() => {
    if (!conversationId) return;

    async function loadMessages() {
      const res = await fetch(
        `${API_URL}/messages?conversation_id=${conversationId}`
      );

      const data = await res.json();
      setMessages(data || []);
    }

    loadMessages();
  }, [conversationId]);

  // send message
  async function sendMessage() {
    if (!input.trim()) return;

    const res = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        conversation_id: conversationId,
        text: input
      })
    });

    const data = await res.json();

    setMessages(prev => [
      ...prev,
      { role: "user", content: input },
      { role: "assistant", content: data.reply }
    ]);

    setInput("");
  }

  return (
    <div style={{ padding: 40 }}>
      <h2>WritePal Chat</h2>

      <div style={{ marginBottom: 20 }}>
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={e => setInput(e.target.value)}
      />

      <button onClick={sendMessage}>
        Send
      </button>
    </div>
  );
}

export default ChatPage;