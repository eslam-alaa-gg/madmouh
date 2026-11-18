(()=>{
const $=s=>document.getElementById(s);
let list=[],queue=[],cur=-1;
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const draw=()=>{
  if(!queue.length){
    queue=shuffle(list.map((_,i)=>i));
    const l=queue.length-1;
    if(l>0&&queue[l]===cur)[queue[0],queue[l]]=[queue[l],queue[0]];
  }
  return queue.pop();
};
const fill=()=>{const d=list[cur];$('d-text').textContent=d.text;$('d-src').textContent=d.source||'';$('d-idx').textContent='الدعاء '+(cur+1)+' من '+list.length};
const next=()=>{
  if(!list.length)return;
  cur=draw();
  const c=$('d-card');c.classList.add('out');
  setTimeout(()=>{fill();c.classList.remove('out')},180);
};
const copy=async t=>{
  try{await navigator.clipboard.writeText(t);return true}catch(e){}
  try{const a=document.createElement('textarea');a.value=t;a.style.cssText='position:fixed;opacity:0';document.body.appendChild(a);a.select();const ok=document.execCommand('copy');a.remove();return ok}catch(e){return false}
};
const txt=()=>{const d=list[cur];return d.text+(d.source?'\n('+d.source+')':'')};
const fail=()=>{$('d-card').hidden=true;$('d-next').parentElement.hidden=true;$('d-err').hidden=false};
const init=async()=>{
  try{
    const d=await loadData('duas','data/duas.json');
    list=Array.isArray(d)?d.filter(x=>x&&typeof x.text==='string'&&x.text.trim()):[];
    if(!list.length)throw new Error('empty');
    $('d-card').hidden=false;$('d-next').parentElement.hidden=false;$('d-err').hidden=true;
    queue=[];cur=-1;cur=draw();fill();
  }catch(e){fail()}
};
$('d-next').onclick=next;
$('d-retry').onclick=init;
$('d-copy').onclick=async()=>{if(list.length)toast(await copy(txt())?'تم نسخ الدعاء':'تعذّر النسخ')};
$('d-share').onclick=async()=>{
  if(!list.length)return;
  if(navigator.share){try{await navigator.share({text:txt()})}catch(e){}return}
  toast(await copy(txt())?'تم نسخ الدعاء، يمكنك لصقه ومشاركته':'تعذّرت المشاركة');
};
init();
})();
