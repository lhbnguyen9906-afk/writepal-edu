import { useState, useEffect, useRef } from "react"

export default function ChatArea({ chat, sendMessage, isTyping }) {
  const [input,setInput]=useState("")
  const bottomRef = useRef(null)

  // 🔥 AUTO SCROLL
  useEffect(()=>{
    bottomRef.current?.scrollIntoView({behavior:"smooth"})
  },[chat.messages, isTyping])

  return (
    <div className="chat-area">

      {/* HEADER */}
      <div className="header">
        WritePal-Edu ✨
      </div>

      {/* MESSAGES */}
      <div className="messages">

        {(chat.messages || []).map((m,i)=>(
          <div key={i} className={`bubble-wrapper ${m.role}`}>
            <div className={m.role==="user" ? "user-bubble" : "ai-bubble"}>
              {m.content}
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

      {/* INPUT */}
      <div className="input-container">
        <textarea
          value={input}
          onChange={(e)=>setInput(e.target.value)}
          onKeyDown={(e)=>{
            if(e.key==="Enter" && !e.shiftKey){
              e.preventDefault()
              if(input.trim()){
                sendMessage(input)
                setInput("")
              }
            }
          }}
          placeholder="Write your paragraph..."
        />

        <button onClick={()=>{
          if(!input.trim()) return
          sendMessage(input)
          setInput("")
        }}>
          Send
        </button>
      </div>

    </div>
  )
}