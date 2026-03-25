export default function Sidebar({ chats, activeChatId, setActiveChatId, createChat, deleteChat }) {
  return (
    <div style={{
      width:220,
      background:"#f5f5f5",
      padding:10
    }}>

      <button
        onClick={createChat}
        style={{
          width:"100%",
          padding:10,
          marginBottom:10
        }}
      >
        + New Chat
      </button>

      {chats.map(c=>(
        <div key={c.id}
          style={{
            padding:8,
            background: c.id===activeChatId ? "#4a90e2" : "white",
            color: c.id===activeChatId ? "white" : "black",
            marginBottom:5,
            borderRadius:6,
            display:"flex",
            justifyContent:"space-between",
            cursor:"pointer"
          }}
        >
          <span onClick={()=>setActiveChatId(c.id)}>
            {c.title}
          </span>

          <span onClick={()=>deleteChat(c.id)}>x</span>
        </div>
      ))}
    </div>
  )
}