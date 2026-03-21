import { useState,useEffect } from "react"

function ThemeToggle(){

const [dark,setDark]=useState(false)

useEffect(()=>{
document.body.classList.toggle("dark",dark)
},[dark])

return(

<button
className="theme-toggle"
onClick={()=>setDark(!dark)}
>

{dark?"☀ Light":"🌙 Dark"}

</button>

)

}

export default ThemeToggle