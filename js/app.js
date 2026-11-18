window.loadData=async(k,p)=>{
  if(window.__DATA__&&window.__DATA__[k])return window.__DATA__[k];
  const r=await fetch(p);if(!r.ok)throw new Error(r.status);return r.json();
};
let tt;
window.toast=m=>{const t=document.getElementById('toast');t.textContent=m;t.classList.add('on');clearTimeout(tt);tt=setTimeout(()=>t.classList.remove('on'),2200)};
(()=>{
  const views=[...document.querySelectorAll('.view')],links=[...document.querySelectorAll('.nav a')];
  const go=()=>{
    let v=location.hash.slice(1);if(!views.some(e=>e.id===v))v='home';
    views.forEach(e=>e.classList.toggle('on',e.id===v));
    links.forEach(a=>a.dataset.v===v?a.setAttribute('aria-current','page'):a.removeAttribute('aria-current'));
    window.scrollTo(0,0);
  };
  addEventListener('hashchange',go);go();
})();
