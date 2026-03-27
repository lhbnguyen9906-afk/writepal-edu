import { useState } from "react"

export default function ChatArea({ chat, sendMessage }) {
  const [input,setInput]=useState("")

  return (
    <div style={{
      display:"flex",
      flexDirection:"column",
      height:"100vh"
    }}>

      {/* HEADER */}
      <div style={{
        padding:"10px 20px",
        borderBottom:"1px solid #ddd",
        fontWeight:"bold"
      }}>
        WritePal-Edu
      </div>

      {/* CHAT */}
      <div style={{
        flex:1,
        overflowY:"auto",
        padding:20
      }}>
        {(chat.messages || []).map((m,i)=>(
          <div key={i} style={{marginBottom:10}}>
            <b>{m.role==="user"?"You":"WritePal"}:</b>
            <div style={{whiteSpace:"pre-wrap"}}>
              {m.content}
            </div>
          </div>
        ))}
      </div>

      {/* INPUT */}
      <div style={{
        display:"flex",
        padding:10,
        borderTop:"1px solid #ddd"
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
          style={{
            flex:1,
            padding:10,
            borderRadius:8,
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
            marginLeft:10,
            padding:"10px 16px",
            borderRadius:8
          }}
        >
          Send
        </button>
      </div>

    </div>
  )
}