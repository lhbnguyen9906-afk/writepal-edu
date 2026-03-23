export default function Sidebar({ chats, activeChatId, setActiveChatId, createChat, deleteChat }) {
  return (
    <div style={{width:200, background:"#eee", padding:10}}>

      <button onClick={createChat}>+ New Chat</button>

      {chats.map(c=>(
        <div key={c.id} style={{marginTop:10}}>
          <span onClick={()=>setActiveChatId(c.id)}>
            {c.title}
          </span>

          <button onClick={()=>deleteChat(c.id)}>x</button>
        </div>
      ))}

    </div>
  )
}