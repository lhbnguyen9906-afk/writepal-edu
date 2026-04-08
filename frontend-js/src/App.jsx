import { useState, useEffect } from "react"
import Sidebar from "./components/Sidebar"
import ChatArea from "./components/ChatArea"
import "./App.css"

const API = import.meta.env.VITE_API_URL

function App(){

  const [chats,setChats] = useState([])
  const [activeChatId,setActiveChatId] = useState(null)
  const [isTyping, setIsTyping] = useState(false)

  const activeChat = chats.find(c=>c.id===activeChatId)

  console.log("API:", API)
  console.log("API:", `${API}/conversations`)
  // =========================
  // LOAD CHAT LIST
  // =========================
  const fetchChats = async ()=>{
    try{
      const res = await fetch(`${API}/conversations`)
      const data = await res.json()

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
      console.error("fetchChats error:", err)
    }
  }

  // =========================
  // LOAD MESSAGES
  // =========================
  const loadMessages = async (id)=>{
    try{
      const res = await fetch(`${API}/conversations/${id}/messages`)
      const data = await res.json()

      if(!Array.isArray(data)) return

      setChats(prev =>
        prev.map(c =>
          c.id===id ? {...c, messages:data} : c
        )
      )

    }catch(err){
      console.error("loadMessages error:", err)
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

      const newChat={
        ...data,
        messages:[]
      }

      setChats(prev=>[newChat,...prev])
      setActiveChatId(data.id)

    }catch(err){
      console.error("createChat error:", err)
    }
  }

  // =========================
  // SEND MESSAGE (🔥 FINAL)
  // =========================
  const sendMessage = async (text)=>{
    if(!text || !activeChatId){
      alert("Missing conversation_id ❌")
      return
    }

    // 👇 show user message ngay
    setChats(prev =>
      prev.map(c =>
        c.id===activeChatId
          ? {
              ...c,
              messages:[
                ...(c.messages || []),
                {role:"user",content:text}
              ]
            }
          : c
      )
    )

    setIsTyping(true)

    try{
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

      // 🔥 delay tự nhiên
      const delay = Math.min(1200, 200 + text.length * 20)

      setTimeout(()=>{

        setIsTyping(false)

        setChats(prev =>
          prev.map(c =>
            c.id===activeChatId
              ? {
                  ...c,
                  messages:[
                    ...(c.messages || []),
                    {role:"assistant",content:data.response}
                  ]
                }
              : c
          )
        )

      }, delay)

    }catch(err){
      console.error("chat error:", err)
      setIsTyping(false)
    }
  }

  useEffect(()=>{
    fetchChats()
  },[])

  return(
    <div className="app">

      <div className="layout">

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
            <ChatArea 
              chat={activeChat} 
              sendMessage={sendMessage}
              isTyping={isTyping}
            />
          ) : (
            <div style={{padding:40}}>Click New Chat</div>
          )}
        </div>

      </div>
    </div>
  )
}

export default App