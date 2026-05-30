import { useState, 
  useEffect

 } from "react"

import Sidebar from "./components/Sidebar"
import ChatArea from "./components/ChatArea"
import "./App.css"

const API = import.meta.env.VITE_API_URL

function App(){

  const [chats,setChats] = useState([])
  const [activeChatId,setActiveChatId] = useState(null)
  const [isTyping, setIsTyping] = useState(false)

  //const activeChat = chats.find(c=>c.id===activeChatId)

  //const [initialized, setInitialized] = useState(false)

  const activeChat = chats.find(c => Number(c.id) === Number(activeChatId))

  //console.log("API:", API)
  //console.log("API:", `${API}/conversations`)
  // =========================
  const createChat = async ()=>{
    const title = prompt("Enter chat title:")

    // ❌ nếu cancel → không tạo
    if (title === null) return

    const res = await fetch(`${API}/conversations`,{
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({
        title: title || "New Chat"
      })
    })

    const data = await res.json()

    const newChat = {
      ...data,
      messages:[]
    }
    const saved = JSON.parse(localStorage.getItem("chats") || "[]")
    const updated = [newChat, ...saved]
    localStorage.setItem("chats", JSON.stringify(updated))

    setChats(updated)
    setActiveChatId(data.id)
  }

  // =========================
  // SEND MESSAGE (🔥 FINAL)
  // =========================
const sendMessage = async (text) => {
    if (!text || !activeChatId) {
      alert("Missing conversation_id ❌")
      return
    }

    // 🔥 Nếu ID là UUID (không phải số) → xóa localStorage và reload
    if (isNaN(Number(activeChatId))) {
      console.error("Invalid conversation_id, clearing localStorage...")
      localStorage.removeItem("chats")
      window.location.reload()
      return
    }

    setChats(prev => {
      const updated = prev.map(c =>
        c.id === activeChatId
          ? { ...c, messages: [...(c.messages || []), { role: "user", content: text }] }
          : c
      )
      localStorage.setItem("chats", JSON.stringify(updated))
      return updated
    })

    setIsTyping(true)

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: activeChatId,
          message: text,
          mode: "vi_en"
        })
      })

      // 🔥 Check lỗi từ backend
      if (!res.ok) {
        console.error("Chat failed:", res.status)
        setIsTyping(false)
        alert("Lỗi kết nối, vui lòng tạo chat mới!")
        return
      }

      const data = await res.json()
      const delay = Math.min(1200, 200 + text.length * 20)

      setTimeout(() => {
        setIsTyping(false)
        setChats(prev => {
          const updated = prev.map(c =>
            c.id === activeChatId
              ? { ...c, messages: [...(c.messages || []), { role: "assistant", content: data.response }] }
              : c
          )
          localStorage.setItem("chats", JSON.stringify(updated))
          return updated
        })
      }, delay)

    } catch (err) {
      console.error("chat error:", err)
      setIsTyping(false)
    }
  }

  // =========================
  useEffect(() => {
  const saved = JSON.parse(localStorage.getItem("chats") || "[]")

  if (saved.length > 0) {
    setChats(saved)
    setActiveChatId(saved[0].id)
  } else {
    // Tạo conversation từ backend thay vì UUID
    fetch(`${API}/conversations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "New Chat" })
    })
      .then(res => res.json())
      .then(data => {
        const newChat = { ...data, messages: [] }
        setChats([newChat])
        setActiveChatId(data.id)
        localStorage.setItem("chats", JSON.stringify([newChat]))
      })
      .catch(err => console.error("Failed to create chat:", err))
  }
}, [])

/*
useEffect(() => {
  if (!activeChatId) return
  let ignore = false
  const run = async () => {
    try {
      const res = await fetch(`${API}/conversations/${activeChatId}/messages`)
      const data = await res.json()
      if (ignore) return
      setChats(prev =>
        prev.map(c =>
          c.id === activeChatId
            ? { ...c, messages: data }
            : c
        )
      )
    } catch (err) {
      console.error(err)
    }
  }
  run()
  return () => {
    ignore = true
  }
}, [activeChatId])
*/

  return(
    <div className="app">

      <div className="layout">

        <Sidebar
          chats={chats}
          activeChatId={activeChatId}
          setActiveChatId={(id)=>{
            setActiveChatId(id)
            // loadMessages(id)
          }}
          createChat={createChat}
          setChats={setChats}   // 🔥 thêm dòng này
        />

        <div className="main">
          {activeChat ? (
            <ChatArea 
              chat={activeChat} 
              sendMessage={sendMessage}
              isTyping={isTyping}
            />
          ) : (
            // <div style={{padding:40}}>Click New Chat</div>
            <div className="empty">
              <h2>Select or create a chat</h2>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

export default App