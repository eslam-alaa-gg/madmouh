(()=>{
const KEY='mamdouh.tasbeeh.v1',$=s=>document.getElementById(s);
let D,all,S,last=0;
const find=id=>all.find(x=>x.id===id);
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const fresh=()=>({id:D.adhkar[0].id,count:0,goal:0,combo:false,step:0,done:false});
const restore=()=>{
  try{
    const s=JSON.parse(localStorage.getItem(KEY));
    if(s&&Number.isInteger(s.count)&&s.count>=0&&(s.combo?Number.isInteger(s.step)&&D.combo.steps[s.step]:find(s.id))){
      s.goal=Number.isInteger(s.goal)&&s.goal>0?s.goal:0;return s;
    }
  }catch(e){}
  return fresh();
};
const item=()=>find(S.combo?D.combo.steps[S.step].ref:S.id);
const goal=()=>S.combo?D.combo.steps[S.step].n:S.goal;
const render=()=>{
  const g=goal(),st=D.combo.steps;
  $('t-text').textContent=item().text;
  $('t-count').textContent=S.count;
  $('t-of').textContent=g?'من '+g:'بدون هدف';
  const p=g?Math.min(100,S.count/g*100):0;
  $('t-bar').style.width=p+'%';$('t-bar').parentElement.setAttribute('aria-valuenow',Math.round(p));
  const c=$('t-combo');c.hidden=!S.combo;
  if(S.combo){const before=st.slice(0,S.step).reduce((a,x)=>a+x.n,0),tot=st.reduce((a,x)=>a+x.n,0);
    c.textContent='الذكر '+(S.step+1)+' من '+st.length+'، المجموع '+(before+S.count)+' من '+tot}
  $('t-note').textContent=(S.combo?S.done:g&&S.count>=g)?'أتممت العدد، تقبّل الله منك':'';
  const gp=$('t-goals');gp.hidden=S.combo;
  if(!S.combo)[...gp.children].forEach(b=>{const v=+b.dataset.g;b.setAttribute('aria-pressed',b.dataset.g==='c'?(S.goal>0&&!D.goals.includes(S.goal)):v===S.goal)});
};
const tap=()=>{
  if(S.combo&&S.done)return;
  const n=performance.now();if(n-last<35)return;last=n;
  if(S.count>=999999)return;
  S.count++;
  if(S.combo&&!S.done){
    const st=D.combo.steps;
    if(S.count>=st[S.step].n){
      if(S.step<st.length-1){S.step++;S.count=0;toast('التالي: '+item().text)}
      else{S.done=true;toast('أتممت 100 تسبيحة')}
    }
  }else if(!S.combo&&S.goal&&S.count===S.goal)toast('بلغت هدفك: '+S.goal);
  save();render();
};
const pop=()=>{const b=$('t-tap');b.classList.remove('pop');void b.offsetWidth;b.classList.add('pop');if(navigator.vibrate)navigator.vibrate(10)};
const setGoal=g=>{S.goal=g;save();render()};
const sheet=()=>{
  const body=$('s-body');body.textContent='';
  const grp=t=>{const h=document.createElement('p');h.className='grp';h.textContent=t;body.appendChild(h)};
  const opt=(t,sm,cur,fn)=>{const b=document.createElement('button');b.className='opt';b.textContent=t;if(sm){const s=document.createElement('small');s.textContent=sm;b.appendChild(s)}
    if(cur)b.setAttribute('aria-current','true');b.onclick=()=>{fn();save();render();$('sheet').close()};body.appendChild(b)};
  grp('الأذكار');
  D.adhkar.forEach(x=>opt(x.text,'',!S.combo&&S.id===x.id,()=>Object.assign(S,{id:x.id,combo:false,count:0,step:0,done:false})));
  grp('أذكار التسبيح المأثورة');
  opt(D.combo.title,'33 + 33 + 34 = 100',S.combo,()=>Object.assign(S,{combo:true,count:0,step:0,done:false}));
  D.masnoon.forEach(x=>opt(x.text,x.goal+' مرة',!S.combo&&S.id===x.id,()=>Object.assign(S,{id:x.id,combo:false,count:0,step:0,done:false,goal:x.goal})));
  $('sheet').showModal();
};
const init=async()=>{
  try{D=await loadData('tasbeeh','data/tasbeeh.json');all=[...D.adhkar,...D.masnoon]}
  catch(e){$('t-text').textContent='تعذّر تحميل الأذكار. أعد تحميل الصفحة.';return}
  S=restore();
  const gp=$('t-goals');
  const chip=(t,g)=>{const b=document.createElement('button');b.className='chip';b.textContent=t;b.dataset.g=g;gp.appendChild(b);return b};
  chip('بدون هدف',0).onclick=()=>{$('t-custom').hidden=true;setGoal(0)};
  D.goals.forEach(g=>chip(g,g).onclick=()=>{$('t-custom').hidden=true;setGoal(g)});
  chip('مخصص','c').onclick=()=>{const c=$('t-custom');c.hidden=!c.hidden;if(!c.hidden)$('t-cin').focus()};
  $('t-cset').onclick=()=>{const v=parseInt($('t-cin').value,10);if(v>=1&&v<=100000){$('t-custom').hidden=true;setGoal(v)}else toast('أدخل عددًا بين 1 و 100000')};
  const b=$('t-tap');
  b.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;e.preventDefault();tap();pop()});
  b.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&!e.repeat){e.preventDefault();tap();pop()}});
  b.addEventListener('click',e=>e.preventDefault());
  $('t-reset').onclick=()=>{S.count=0;S.step=0;S.done=false;save();render();toast('تمت إعادة التعيين')};
  $('t-pick').onclick=sheet;
  $('s-close').onclick=()=>$('sheet').close();
  $('sheet').addEventListener('click',e=>{if(e.target.id==='sheet')e.target.close()});
  render();
};
init();
})();
