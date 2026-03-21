import { useState, useEffect } from "react"
import Sidebar from "./components/Sidebar"
import ChatArea from "./components/ChatArea"

function App(){

  const [chats,setChats] = useState([])
  const [activeChatId,setActiveChatId] = useState(null)

  const activeChat = chats.find(c=>c.id===activeChatId)

  const loadMessages = async (id)=>{
    const res = await fetch(`http://127.0.0.1:8000/conversations/${id}/messages`)
    const data = await res.json()

    setChats(prev =>
      prev.map(c =>
        c.id===id ? {...c, messages:data} : c
      )
    )
  }

  const handleSelectChat = (id)=>{
    setActiveChatId(id)
    loadMessages(id)
  }

  const createChat = async ()=>{
    const res = await fetch("http://127.0.0.1:8000/conversations",{method:"POST"})
    const data = await res.json()

    const newChat={
      id:data.id,
      title:data.title,
      messages:[]
    }

    setChats(prev=>[newChat,...prev])
    setActiveChatId(data.id)
  }

  const deleteChat = async (id)=>{
    try{
      await fetch(`http://127.0.0.1:8000/conversations/${id}`,{
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
      console.error("Delete failed",err)
    }
  }

  useEffect(()=>{
    const fetchChats = async ()=>{
      const res = await fetch("http://127.0.0.1:8000/conversations")
      const data = await res.json()

      const formatted = data.map(c=>({
        id:c.id,
        title:c.title,
        messages:[]
      }))

      setChats(formatted)

      if(formatted.length>0){
        setActiveChatId(formatted[0].id)
        loadMessages(formatted[0].id)
      }
    }

    fetchChats()
  },[])

  const updateMessages = (messages)=>{
    setChats(prev =>
      prev.map(c =>
        c.id===activeChatId ? {...c,messages} : c
      )
    )
  }

  return(
    <div className="app">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        setActiveChatId={handleSelectChat}
        createChat={createChat}
        deleteChat={deleteChat}
      />

      <div className="main">
        {activeChat ? (
          <ChatArea chat={activeChat} updateMessages={updateMessages}/>
        ) : (
          <div style={{padding:40}}>Click New Chat</div>
        )}
      </div>
    </div>
  )
}

export default App