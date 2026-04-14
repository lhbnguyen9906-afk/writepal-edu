import { API } from "../config"
import { useState,useEffect,useRef   } from "react"

export default function Sidebar({
  chats,
  activeChatId,
  setActiveChatId,
  createChat,
  setChats
}) {
  const menuRef = useRef(null)
  const [menu, setMenu] = useState(null) 
  // { id, x, y }
  useEffect(() => {
    const handleClickOutside = () => {
      setMenu(null)
    }

    window.addEventListener("click", handleClickOutside)

    return () => window.removeEventListener("click", handleClickOutside)
  }, [])

  // useEffect(() => {
  //   const handleClickOutside = () => {
  //     setMenu(null)
  //   }

  //   window.addEventListener("mousedown", handleClickOutside)

  //   return () => window.removeEventListener("mousedown", handleClickOutside)
  // }, [])
useEffect(() => {
  const handleClickOutside = (e) => {
    if (menuRef.current && !menuRef.current.contains(e.target)) {
      setMenu(null)
    }
  }

  window.addEventListener("mousedown", handleClickOutside)

  return () => window.removeEventListener("mousedown", handleClickOutside)
}, [])

useEffect(() => {
  const handleScroll = () => setMenu(null)
  window.addEventListener("scroll", handleScroll)

  return () => window.removeEventListener("scroll", handleScroll)
}, [])

  return (
    <div className="sidebar">

      <button className="new-chat-btn" onClick={createChat}>
        + New Chat
      </button>

      {chats.map((c, index) => (
        <div
          key={c.id}
          className={`chat-item ${c.id === activeChatId ? "active" : ""}`}
          onClick={() => {
            setActiveChatId(Number(c.id))
            setMenu(null)   // 🔥 đóng menu
          }}
        >

          <div className="chat-left">
            {index + 1}. {c.title}
          </div>

          <div
            className="menu-trigger"
            onClick={(e) => {
              e.stopPropagation()

              const rect = e.currentTarget.getBoundingClientRect()

              setMenu({
                id: c.id,
                x: rect.right,
                y: rect.bottom
              })
            }}
          >
            ⋯
          </div>

        </div>
      ))}

      {/* MENU GLOBAL */}
      {menu && (
        <div
          ref={menuRef}
          className="menu-floating"
          style={{
            top: menu.y,
            left: menu.x
          }}
          onClick={(e) => e.stopPropagation()}   // 🔥 QUAN TRỌNG
        >

          <div
            className="menu-item"
            onClick={async (e) => {
              e.stopPropagation()   // 🔥 THÊM DÒNG NÀY
              setMenu(null)   // 🔥 đóng menu
              const currentChat = chats.find(c => c.id === menu.id)
             
              const newTitle = prompt("Rename chat:", currentChat?.title || "")
              if (newTitle === null) return

              await fetch(`${API}/conversations/${menu.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: newTitle })
              })

              setChats(prev =>
                prev.map(c =>
                  c.id === menu.id ? { ...c, title: newTitle } : c
                )
              )

              
            }}
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg> Rename
          </div>

          <div
            className="menu-item delete"
            onClick={async (e) => {
              e.stopPropagation()   // 🔥 THÊM DÒNG NÀY
              setMenu(null)   // 🔥 đóng menu
              const ok = confirm("Delete this chat?")
              if (!ok) return

              await fetch(`${API}/conversations/${menu.id}`, {
                method: "DELETE"
              })

              setChats(prev => {
                const updated = prev.filter(c => c.id !== menu.id)

                if (menu.id === activeChatId) {
                  setActiveChatId(updated.length ? updated[0].id : null)
                }

                return updated
              })

              
            }}
          >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="3 6 5 6 21 6"/>
          <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
          <path d="M10 11v6M14 11v6"/>
          <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
        </svg> Delete
          </div>

        </div>
      )}

    </div>
  )
}