import { useState, useEffect, useRef } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

export default function ChatArea({ chat, sendMessage, isTyping }) {
  const [input,setInput]=useState("")
  const bottomRef = useRef(null)
  

  // 🔥 AUTO SCROLL
  useEffect(()=>{
    bottomRef.current?.scrollIntoView({behavior:"smooth"})
  },[chat.messages, isTyping])

  useEffect(() => {
    const el = document.querySelector("textarea")
    if (!el) return

    el.style.height = "auto"
    el.style.height = el.scrollHeight + "px"
  }, [input])

  return (
    <div className="chat-area">

      {/* HEADER */}
      <div className="header">
        <img src="/logo - WritePal-Edu.png" alt="Logo" style={{ height: '60px', width: '200px', margin: '0 20px 0 0' }} /> 
        {/* WritePal-Edu ✨ */}
        <span style={{
          fontSize: '20px',
          fontWeight: '500',
          color: '#64748b',           /* 🔥 màu xám slate nhẹ */
          borderLeft: '1px solid #e5e7eb',  /* 🔥 đường kẻ ngăn cách */
          paddingLeft: '20px',
          letterSpacing: '0.01em'
        }}>
          {chat.title}
        </span>
      </div>



      {/* MESSAGES */}
      <div className="messages">

        {chat.messages.length === 0 && (
          <div className="empty">
            <h2>How can I help you today?</h2>
          </div>
        )}

        {(chat.messages || []).map((m,i)=>(
          <div key={i} className={`bubble-wrapper ${m.role}`}>
            <div className={m.role==="user" ? "user-bubble" : "ai-bubble"}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {m.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}

        {/* 🔥 TYPING ANIMATION */}
        {isTyping && (
          <div className="bubble-wrapper assistant">
            <div className="ai-bubble typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        <div ref={bottomRef}></div>
      </div>

    <div className="input-container">
  <div className="input-box">
    <textarea
      value={input}
      onChange={(e) => {
        setInput(e.target.value)
        e.target.style.height = "auto"
        e.target.style.height = e.target.scrollHeight + "px"
      }}
      onKeyDown={(e) => {
        if (isTyping) return
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault()
          if (input.trim()) {
            sendMessage(input)
            setInput("")
            e.target.style.height = "auto"
          }
        }
      }}
      style={{ opacity: isTyping ? 0.6 : 1 }}
      placeholder="Ask anything..."
      rows={1}
    />
    <button
      className="send-btn"
      onClick={() => {
        if (!input.trim()) return
        sendMessage(input)
        setInput("")
      }}
      disabled={isTyping}
      style={{
        opacity: isTyping ? 0.6 : 1,
        cursor: isTyping ? 'not-allowed' : 'pointer'
      }}
    >
      {isTyping ? '⏳' : '➤'}
    </button>
  </div>
</div>

 

    </div>
  )
}