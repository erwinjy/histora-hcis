import React,{useState} from "react";
const pages=["Home","Sources","Datasets","Jobs","Entities","Events","Claims & Evidence","Conflicts & Variants","Timeline","Graph","Research","Acquisition","Models","Audit","Settings"];
export function App(){
 const [page,setPage]=useState("Home");
 return <div className="shell">
  <nav><h2>HCIS</h2>{pages.map(p=><div key={p}><button onClick={()=>setPage(p)}>{p}</button></div>)}</nav>
  <main><h1>{page}</h1><div className="card">
    {page==="Home" ? <>拖入历史资料 / 搜索人物、事件、Claim、原文</> : <>Code-Locked page shell: {page}</>}
  </div></main>
 </div>
}
