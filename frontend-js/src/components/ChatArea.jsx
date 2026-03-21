import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkBreaks from "remark-breaks";

function ChatArea({ chat, updateMessages }) {

  const [input,setInput] = useState("")
  const [loading,setLoading] = useState(false)
  const [language,setLanguage] = useState(localStorage.getItem("lang") || "en")
  const [mode,setMode] = useState("tutor")

  const bottomRef = useRef(null)

  useEffect(()=>{
    bottomRef.current?.scrollIntoView({behavior:"smooth"})
  },[chat?.messages])

  const sendMessage = async ()=>{
    if(!input.trim() || !chat?.id || loading) return

    const newMessages = [
      ...(chat.messages || []),
      {sender:"user",text:input}
    ]

    updateMessages(newMessages)
    setInput("")
    setLoading(true)

    try{
      const res = await fetch("http://127.0.0.1:8000/chat",{
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body:JSON.stringify({
          conversation_id:chat.id,
          text:input,
          language,
          mode
        })
      })

      const data = await res.json()

      updateMessages([
        ...newMessages,
        {sender:"bot",text:data.response}
      ])

    }catch(err){
      updateMessages([
        ...newMessages,
        {sender:"bot",text:"⚠️ Server error"}
      ])
    }

    setLoading(false)
  }

  return (
    <>
      <div className="toolbar">
        <span>💬 WritePal-Edu</span>

        <select value={language} onChange={e=>{
          setLanguage(e.target.value)
          localStorage.setItem("lang",e.target.value)
        }}>
          <option value="en">English</option>
          <option value="vi">Tiếng Việt</option>
        </select>

        <select value={mode} onChange={e=>setMode(e.target.value)}>
          <option value="tutor">Tutor</option>
          <option value="rewrite">Rewrite</option>
          <option value="structure">Structure</option>
        </select>
      </div>

      <div className="messages">
        {(chat?.messages || []).map((m,i)=>(
          <div key={i} className={`bubble ${m.sender}`}>
            <ReactMarkdown remarkPlugins={[remarkBreaks]}>
              {m.text}
            </ReactMarkdown>
          </div>
        ))}

        {loading && <div className="bubble bot typing">...</div>}

        <div ref={bottomRef}/>
      </div>

      <div className="input-container">
        <textarea
          value={input}
          onChange={e=>setInput(e.target.value)}
          placeholder="Write your paragraph..."
          onKeyDown={(e)=>{
            if(e.key==="Enter" && !e.shiftKey){
              e.preventDefault()
              sendMessage()
            }
          }}
        />

        <button onClick={sendMessage} className="send-btn">
          Send
        </button>
      </div>
    </>
  )
}

export default ChatArea