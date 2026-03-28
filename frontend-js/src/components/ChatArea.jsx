import { useState } from "react"

export default function ChatArea({ chat, sendMessage }) {
  const [input,setInput]=useState("")

  return (
    <div style={{
      display:"flex",
      flexDirection:"column",
      height:"100%"
    }}>

      {/* HEADER */}
      <div style={{
        padding:"12px 20px",
        borderBottom:"1px solid #eee",
        fontWeight:"bold"
      }}>
        WritePal-Edu
      </div>

      {/* CHAT BODY */}
      <div style={{
        flex:1,
        overflowY:"auto",
        padding:"20px",
        display:"flex",
        flexDirection:"column",
        gap:"12px"
      }}>
        {(chat.messages || []).map((m,i)=>(
          <div
            key={i}
            style={{
              display:"flex",
              justifyContent: m.role==="user" ? "flex-end" : "flex-start"
            }}
          >
            <div style={{
              maxWidth:"70%",
              padding:"12px 14px",
              borderRadius:"16px",
              background: m.role==="user" ? "#4f8cff" : "#f1f1f1",
              color: m.role==="user" ? "white" : "black",
              whiteSpace:"pre-wrap",
              wordBreak:"break-word",
              lineHeight:1.5
            }}>
              {m.content}
            </div>
          </div>
        ))}
      </div>

      {/* INPUT */}
      <div style={{
        display:"flex",
        padding:"12px",
        borderTop:"1px solid #eee"
      }}>
        <input
          value={input}
          onChange={(e)=>setInput(e.target.value)}
          onKeyDown={(e)=>{
            if(e.key==="Enter" && input.trim()){
              sendMessage(input)
              setInput("")
            }
          }}
          placeholder="Write your paragraph..."
          style={{
            flex:1,
            padding:"12px",
            borderRadius:"12px",
            border:"1px solid #ddd",
            outline:"none"
          }}
        />

        <button
          onClick={()=>{
            if(!input.trim()) return
            sendMessage(input)
            setInput("")
          }}
          style={{
            marginLeft:"10px",
            padding:"12px 18px",
            borderRadius:"12px",
            background:"#4f8cff",
            color:"white",
            border:"none",
            cursor:"pointer"
          }}
        >
          Send
        </button>
      </div>

    </div>
  )
}