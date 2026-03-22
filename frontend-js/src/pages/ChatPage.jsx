import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;
// ví dụ: https://writepal-edu-production.up.railway.app

function ChatPage() {
  const [userId, setUserId] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // 🔥 LOGIN (tạo user)
  useEffect(() => {
    async function login() {
      const res = await fetch(`${API_URL}/login?username=test`, {
        method: "POST"
      });

      const data = await res.json();
      setUserId(data.user_id);
    }

    login();
  }, []);

  // 🔥 TẠO CONVERSATION
  useEffect(() => {
    if (!userId) return;

    async function createConversation() {
      const res = await fetch(
        `${API_URL}/conversations?user_id=${userId}`,
        {
          method: "POST"
        }
      );

      const data = await res.json();
      setConversationId(data.conversation_id);
    }

    createConversation();
  }, [userId]);

  // 🔥 LOAD HISTORY
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

  // 🔥 SEND MESSAGE
  async function sendMessage() {
    if (!input.trim()) return;

    // show user message ngay
    setMessages(prev => [
      ...prev,
      { role: "user", content: input }
    ]);

    const res = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        conversation_id: conversationId,
        text: input,
        user_id: userId,
        mode: "tutor",
        language: "en"
      })
    });

    const data = await res.json();

    // 🔥 FIX QUAN TRỌNG: response (không phải reply)
    setMessages(prev => [
      ...prev,
      { role: "assistant", content: data.response }
    ]);

    setInput("");
  }

  return (
    <div style={{ padding: 40 }}>
      <h2>WritePal Chat</h2>

      <div style={{ marginBottom: 20 }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: 10 }}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        style={{ width: "60%", marginRight: 10 }}
        placeholder="Type something..."
      />

      <button onClick={sendMessage}>
        Send
      </button>
    </div>
  );
}

export default ChatPage;