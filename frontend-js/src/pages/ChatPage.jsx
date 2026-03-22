import { useState, useEffect } from "react";

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [conversationId, setConversationId] = useState(null);

  const API = "https://writepal-edu-production.up.railway.app";

  // 🔥 tạo conversation khi load
  useEffect(() => {
    fetch(`${API}/conversations`, { method: "POST" })
      .then(res => res.json())
      .then(data => setConversationId(data.conversation_id));
  }, []);

  const sendMessage = async () => {
    if (!message) return;

    const res = await fetch(`${API}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        conversation_id: conversationId,
        message,
        mode: "vi_en",
      }),
    });

    const data = await res.json();

    setChat([...chat, { user: message, bot: data.response }]);
    setMessage("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>WritePal-Edu</h2>

      <div>
        {chat.map((c, i) => (
          <div key={i}>
            <p><b>You:</b> {c.user}</p>
            <p><b>Bot:</b> {c.bot}</p>
          </div>
        ))}
      </div>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type..."
      />

      <button onClick={sendMessage}>Send</button>
    </div>
  );
}