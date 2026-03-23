import { useState, useEffect } from "react";

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [conversationId, setConversationId] = useState(null);

  const API = import.meta.env.VITE_API;

  useEffect(() => {
    const init = async () => {
      const res = await fetch(`${API}/conversations`, {
        method: "POST",
      });
      const data = await res.json();
      setConversationId(data.conversation_id);
    };

    init();
  }, []);

  const sendMessage = async () => {
    if (!message || !conversationId) return;

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

    setChat((prev) => [
      ...prev,
      { role: "user", content: message },
      { role: "assistant", content: data.response },
    ]);

    setMessage("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>WritePal-Edu</h2>

      {chat.map((m, i) => (
        <div key={i}>
          <b>{m.role}:</b> {m.content}
        </div>
      ))}

      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}