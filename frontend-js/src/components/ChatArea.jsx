import { useState } from "react"

export default function ChatArea({ chat, sendMessage }) {
  const [input,setInput]=useState("")

  return (
    <div style={{padding:20}}>

      {(chat.messages || []).map((m,i)=>(
        <div key={i}>
          <b>{m.role==="user"?"You":"Bot"}:</b> {m.content}
        </div>
      ))}

      <input
        value={input}
        onChange={(e)=>setInput(e.target.value)}
        onKeyDown={(e)=>{
          if(e.key==="Enter" && input.trim()){
            sendMessage(input)
            setInput("")
          }
        }}
      />

      <button onClick={()=>{
        if(!input.trim()) return
        sendMessage(input)
        setInput("")
      }}>
        Send
      </button>

    </div>
  )
}