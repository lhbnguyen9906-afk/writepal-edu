import { useState } from "react"

export default function ChatArea({ chat, sendMessage }) {
  const [input,setInput]=useState("")

  return (
    <div style={{
      padding:20,
      display:"flex",
      flexDirection:"column",
      height:"100%"
    }}>

      {/* MESSAGES */}
      <div style={{flex:1, overflowY:"auto"}}>
        {(chat.messages || []).map((m,i)=>(
          <div key={i}
            style={{
              marginBottom:10,
              display:"flex",
              justifyContent: m.role==="user" ? "flex-end" : "flex-start"
            }}
          >
            <div style={{
              background: m.role==="user" ? "#4a90e2" : "#eee",
              color: m.role==="user" ? "white" : "black",
              padding:"10px 14px",
              borderRadius:12,
              maxWidth:"70%"
            }}>
              {m.content}
            </div>
          </div>
        ))}
      </div>

      {/* INPUT */}
      <div style={{display:"flex", gap:10}}>
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
            padding:12,
            borderRadius:10,
            border:"1px solid #ccc"
          }}
        />

        <button
          onClick={()=>{
            if(!input.trim()) return
            sendMessage(input)
            setInput("")
          }}
          style={{
            padding:"10px 20px",
            borderRadius:10,
            background:"#4a90e2",
            color:"white",
            border:"none"
          }}
        >
          Send
        </button>
      </div>
    </div>
  )
}