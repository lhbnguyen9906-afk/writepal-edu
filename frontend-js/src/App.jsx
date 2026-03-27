import { useState, useEffect } from "react"
import Sidebar from "./components/Sidebar"
import ChatArea from "./components/ChatArea"
import "./App.css"

const API = import.meta.env.VITE_API

function App(){

  const [chats,setChats] = useState([])
  const [activeChatId,setActiveChatId] = useState(null)

  const activeChat = chats.find(c=>c.id===activeChatId)

  // LOAD CHAT LIST
  const fetchChats = async ()=>{
    const res = await fetch(`${API}/conversations`)
    const data = await res.json()

    const formatted = data.map(c=>({
      ...c,
      messages:[]
    }))

    setChats(formatted)

    if(formatted.length>0){
      setActiveChatId(formatted[0].id)
      loadMessages(formatted[0].id)
    }
  }

  // LOAD MESSAGES
  const loadMessages = async (id)=>{
    const res = await fetch(`${API}/conversations/${id}/messages`)
    const data = await res.json()

    setChats(prev =>
      prev.map(c =>
        c.id===id ? {...c, messages:data} : c
      )
    )
  }

  // CREATE CHAT
  const createChat = async ()=>{
    const res = await fetch(`${API}/conversations`,{
      method:"POST"
    })

    const data = await res.json()

    const newChat={
      ...data,
      messages:[]
    }

    setChats(prev=>[newChat,...prev])
    setActiveChatId(data.id)
  }

  // SEND MESSAGE
  const sendMessage = async (text)=>{
    if(!text || !activeChatId){
      alert("Missing conversation_id ❌")
      return
    }

    const res = await fetch(`${API}/chat`,{
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({
        conversation_id: Number(activeChatId),
        message: text,
        mode:"vi_en"
      })
    })

    const data = await res.json()

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
  }

  useEffect(()=>{
    fetchChats()
  },[])

  return(
    <div className="app">

      {/* ✅ HEADER */}
      <div style={{
        padding: "10px 20px",
        borderBottom: "1px solid #ddd",
        fontWeight: "bold"
      }}>
        WritePal-Edu
      </div>

      <div style={{display:"flex", flex:1}}>

        <Sidebar
          chats={chats}
          activeChatId={activeChatId}
          setActiveChatId={(id)=>{
            setActiveChatId(id)
            loadMessages(id)
          }}
          createChat={createChat}
        />

        <div className="main">
          {activeChat ? (
            <ChatArea chat={activeChat} sendMessage={sendMessage}/>
          ) : (
            <div style={{padding:40}}>Click New Chat</div>
          )}
        </div>

      </div>
    </div>
  )
}

export default App