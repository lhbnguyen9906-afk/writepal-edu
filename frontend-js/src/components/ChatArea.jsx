import { useState } from "react"

export default function ChatArea({ chat, sendMessage }) {
  const [input,setInput]=useState("")

  return (
    <div style={{padding:20}}>

      {/* MESSAGES */}
      {chat.messages.map((m,i)=>(
        <div key={i}>
          <b>{m.role==="user"?"You":"Bot"}:</b> {m.content}
        </div>
      ))}

      {/* INPUT */}
      <input
        value={input}
        onChange={(e)=>setInput(e.target.value)}
        onKeyDown={(e)=>{
          if(e.key==="Enter"){
            sendMessage(input)
            setInput("")
          }
        }}
      />

      <button onClick={()=>{
        sendMessage(input)
        setInput("")
      }}>
        Send
      </button>

    </div>
  )
}