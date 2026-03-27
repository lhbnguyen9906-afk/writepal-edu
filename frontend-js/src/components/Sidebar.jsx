export default function Sidebar({ chats, activeChatId, setActiveChatId, createChat }) {
  return (
    <div style={{width:200}}>

      <button onClick={createChat}>+ New Chat</button>

      {chats.map(c=>(
        <div key={c.id}
          onClick={()=>setActiveChatId(c.id)}
          style={{
            padding:5,
            background: c.id===activeChatId ? "#ddd" : "white"
          }}
        >
          {c.title}
        </div>
      ))}
    </div>
  )
}