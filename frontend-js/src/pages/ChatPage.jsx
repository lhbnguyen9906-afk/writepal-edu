import { useState, useEffect } from "react";

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [conversationId, setConversationId] = useState(null);

  const API = import.meta.env.VITE_API;

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

        console.log("🔥 conversation created:", data);   // 👈 CHECK 1

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
    console.log("📨 sending...");
    console.log("message:", message);              // 👈 CHECK 2
    console.log("conversationId:", conversationId); // 👈 CHECK 3

    if (!message || !conversationId) {
      console.log("❌ blocked (missing data)");
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
          message,
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
        {chat.map((m, i) => (
          <div key={i}>
            <b>{m.role === "user" ? "You" : "Bot"}:</b> {m.content}
          </div>
        ))}
      </div>

      {/* INPUT */}
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") sendMessage(); // 👈 FIX ENTER
        }}
        placeholder="Type..."
        style={{ width: "70%", marginRight: 10 }}
      />

      {/* BUTTON */}
      <button onClick={sendMessage} disabled={!conversationId}>
        Send
      </button>
    </div>
  );
}