import { useState } from "react";

function ChatInput({ conversationId, setMessages }) {
  const [text, setText] = useState("");

  const send = async () => {
    if (!text.trim()) return;

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        conversation_id: conversationId,
        text
      })
    });

    const data = await res.json();

    setMessages(prev => [
      ...prev,
      { role: "user", content: text },
      { role: "assistant", content: data.reply }
    ]);

    setText("");
  };

  return (
    <div>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
      />
      <button onClick={send}>Send</button>
    </div>
  );
}

export default ChatInput;