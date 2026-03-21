function Sidebar({ chats, activeChatId, setActiveChatId, createChat, deleteChat }) {

  return (
    <div className="sidebar">

      <button className="new-chat-btn" onClick={createChat}>
        + New Chat
      </button>

      {chats.map(chat => (
        <div
          key={chat.id}
          className={`chat-item ${chat.id === activeChatId ? "active" : ""}`}
          onClick={() => setActiveChatId(chat.id)}
        >
          <span className="chat-title">{chat.title}</span>

          <button
            className="delete-btn"
            onClick={(e)=>{
              e.stopPropagation()
              deleteChat(chat.id)
            }}
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  )
}

export default Sidebar