import { useState, useEffect } from "react"
import Sidebar from "./components/Sidebar"
import ChatArea from "./components/ChatArea"

const API = import.meta.env.VITE_API

function App(){

  const [chats,setChats] = useState([])
  const [activeChatId,setActiveChatId] = useState(null)

  const activeChat = chats.find(c=>c.id===activeChatId)

  // =========================
  // LOAD ALL CHATS
  // =========================
  const fetchChats = async ()=>{
    try{
      const res = await fetch(`${API}/conversations`)
      const data = await res.json()

      console.log("🔥 chats:", data)

      if(!Array.isArray(data)) return

      const formatted = data.map(c=>({
        ...c,
        messages:[]
      }))

      setChats(formatted)

      if(formatted.length>0){
        setActiveChatId(formatted[0].id)
        loadMessages(formatted[0].id)
      }

    }catch(err){
      console.error("❌ fetchChats error:", err)
    }
  }

  // =========================
  // LOAD MESSAGES
  // =========================
  const loadMessages = async (id)=>{
    try{
      const res = await fetch(`${API}/conversations/${id}/messages`)
      const data = await res.json()

      console.log("📥 messages:", data)

      if(!Array.isArray(data)) return

      setChats(prev =>
        prev.map(c =>
          c.id===id ? {...c, messages:data} : c
        )
      )

    }catch(err){
      console.error("❌ loadMessages error:", err)
    }
  }

  // =========================
  // CREATE CHAT
  // =========================
  const createChat = async ()=>{
    try{
      const res = await fetch(`${API}/conversations`,{
        method:"POST"
      })

      const data = await res.json()

      console.log("🆕 new chat:", data)

      const newChat={
        ...data,
        messages:[]
      }

      setChats(prev=>[newChat,...prev])
      setActiveChatId(data.id)

    }catch(err){
      console.error("❌ createChat error:", err)
    }
  }

  // =========================
  // DELETE CHAT
  // =========================
  const deleteChat = async (id)=>{
    try{
      await fetch(`${API}/conversations/${id}`,{
        method:"DELETE"
      })

      setChats(prev=>{
        const updated = prev.filter(c=>c.id!==id)

        if(activeChatId===id){
          setActiveChatId(updated.length ? updated[0].id : null)
        }

        return updated
      })

    }catch(err){
      console.error("❌ delete error:", err)
    }
  }

  // =========================
  // SEND MESSAGE
  // =========================
  const sendMessage = async (text)=>{
    console.log("📨 sendMessage", text, activeChatId)

    if(!text || !activeChatId){
      console.log("❌ blocked")
      return
    }

    try{
      const res = await fetch(`${API}/chat`,{
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({
          conversation_id: activeChatId,
          message: text,
          mode:"vi_en"
        })
      })

      const data = await res.json()

      console.log("🤖 AI:", data)

      const newMessages=[
        ...(activeChat?.messages || []),
        {role:"user",content:text},
        {role:"assistant",content:data.response}
      ]

      setChats(prev =>
        prev.map(c =>
          c.id===activeChatId ? {...c, messages:newMessages} : c
        )
      )

    }catch(err){
      console.error("❌ chat error:", err)
    }
  }

  useEffect(()=>{
    fetchChats()
  },[])

  return(
    <div className="app">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        setActiveChatId={(id)=>{
          setActiveChatId(id)
          loadMessages(id)
        }}
        createChat={createChat}
        deleteChat={deleteChat}
      />

      <div className="main">
        {activeChat ? (
          <ChatArea chat={activeChat} sendMessage={sendMessage}/>
        ) : (
          <div style={{padding:40}}>Click New Chat</div>
        )}
      </div>
    </div>
  )
}

export default App