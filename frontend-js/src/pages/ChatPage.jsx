import { useState, useEffect } from "react";

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [conversationId, setConversationId] = useState(null);

  // 🔥 lấy API từ .env
  const API = import.meta.env.VITE_API;

  console.log("🔥 API:", API);

  // =========================
  // INIT CONVERSATION
  // =========================
  useEffect(() => {
    const init = async () => {
      try {
        const res = await fetch(`${API}/conversations`, {
          method: "POST",
        });

        const data = await res.json();

        console.log("🔥 conversation:", data);

        setConversationId(data.conversation_id);
      } catch (err) {
        console.error("❌ create conversation error:", err);
      }
    };

    init();
  }, []);

  // =========================
  // SEND MESSAGE
  // =========================
  const sendMessage = async () => {
    if (!message || !conversationId) {
      console.log("❌ missing data");
      return;
    }

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: message,
          mode: "vi_en",
        }),
      });

      const data = await res.json();

      console.log("🤖 response:", data);

      setChat((prev) => [
        ...prev,
        { role: "user", content: message },
        { role: "assistant", content: data.response },
      ]);

      setMessage("");
    } catch (err) {
      console.error("❌ chat error:", err);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>WritePal-Edu 🚀</h2>

      {/* CHAT */}
      <div style={{ marginBottom: 20 }}>
        {chat.map((msg, index) => (
          <div key={index}>
            <b>{msg.role === "user" ? "You" : "Bot"}:</b> {msg.content}
          </div>
        ))}
      </div>

      {/* INPUT */}
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your sentence..."
        style={{ width: "70%", marginRight: 10 }}
      />

      <button onClick={sendMessage}>Send</button>
    </div>
  );
}