const WA="919354561001";
const $=s=>document.querySelector(s);
let cart={};try{cart=JSON.parse(localStorage.getItem("yzcart")||"{}")}catch(e){}
const qs={};
const save=()=>{try{localStorage.setItem("yzcart",JSON.stringify(cart))}catch(e){}};
const prod=id=>PRODUCTS.find(p=>p.id==id);
const rs=n=>"₹"+Number(n).toLocaleString("en-IN");
const off=p=>p.mrp&&p.price&&p.mrp>p.price?Math.round((p.mrp-p.price)/p.mrp*100):0;
const priceH=p=>!p.price?"Price on WhatsApp":off(p)?`<span class="now">${rs(p.price)}</span><s class="old">${rs(p.mrp)}</s><span class="pct">${off(p)}% off</span>`:rs(p.price);
function card(p){return `<article class="p rv in"><a class="pi" href="${ROOT}medicine/${p.slug}.html" aria-label="${p.name}">${off(p)?`<span class="rib">${off(p)}% OFF</span>`:""}${p.images&&p.images.length?`<img src="${ROOT}images/${p.images[0]}" alt="${p.name}" loading="lazy">`:p.icon}</a><div class="pb">
<h3><a href="${ROOT}medicine/${p.slug}.html">${p.name}</a></h3><small>${p.info}</small><small>Pack: ${p.pack}</small>
${p.rx?'<span class="rx">Prescription required</span>':''}<div class="price">${priceH(p)}</div>
<div class="row"><div class="qty"><button onclick="qty(${p.id},-1)" aria-label="Decrease">−</button><span id="q${p.id}">1</span><button onclick="qty(${p.id},1)" aria-label="Increase">+</button></div>
<button class="add" onclick="add(${p.id})">Add to Cart</button></div><button class="buy" onclick="buyNow(${p.id})"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg> Buy Now</button></div></article>`}
function grid(){const g=$("#grid");if(!g)return;const t=($("#q")?$("#q").value:"").toLowerCase(),lim=+g.dataset.limit||999;
g.innerHTML=PRODUCTS.filter(p=>(p.name+p.info).toLowerCase().includes(t)).slice(0,lim).map(card).join("")||'<p class="empty" style="grid-column:1/-1">No medicine found. Message us on WhatsApp.</p>'}
function qty(id,d){qs[id]=Math.max(1,(qs[id]||1)+d);const e=$("#q"+id);if(e)e.textContent=qs[id]}
function toast(m){let t=$("#toast");if(!t){document.body.insertAdjacentHTML("beforeend",'<div id="toast" role="status"></div>');t=$("#toast")}t.innerHTML=m;t.classList.add("show");clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove("show"),2600)}
function add(id){const n=qs[id]||1;cart[id]=(cart[id]||0)+n;qs[id]=1;const e=$("#q"+id);if(e)e.textContent=1;save();upd();const b=$("#cb");b.classList.remove("bump");void b.offsetWidth;b.classList.add("bump");toast(`✓ ${n} × ${prod(id).name} added <a onclick="openCart()">View cart</a>`)}
function chg(id,d){cart[id]+=d;if(cart[id]<=0)delete cart[id];save();upd()}
function upd(){const ids=Object.keys(cart).filter(prod);$("#cc").textContent=ids.reduce((a,i)=>a+cart[i],0);
$("#items").innerHTML=ids.length?ids.map(i=>{const p=prod(i);return `<div class="it"><div><b>${p.name}</b><small>${p.pack}${p.price?' · '+rs(p.price):''}${off(p)?' <s class="old">'+rs(p.mrp)+'</s>':''}</small></div><div class="qty"><button onclick="chg(${i},-1)">−</button><span>${cart[i]}</span><button onclick="chg(${i},1)">+</button></div></div>`}).join(""):'<p class="empty">Your cart is empty</p>'}
function openCart(){$("#drawer").classList.add("open");$("#ov").classList.add("open")}
function closeCart(){$("#drawer").classList.remove("open");$("#ov").classList.remove("open")}
const cust={get(){try{return JSON.parse(localStorage.getItem("yzcust")||"{}")}catch(e){return{}}},set(d){try{localStorage.setItem("yzcust",JSON.stringify(d))}catch(e){}}};
function valid(n,ph,ad,er){const bad=m=>{er.textContent=m;return false};
 if(n.length<2)return bad("Please enter your name.");
 if(!/^[+]?[0-9 ]{10,14}$/.test(ph))return bad("Please enter a valid mobile number.");
 if(ad.length<8)return bad("Please enter your full delivery address with PIN code.");
 er.textContent="";return true}
function wa(items,n,ph,a,tag){let tot=0,all=true,m="*New Order – Yzar Healthcare*"+(tag?" ("+tag+")":"")+"\n\n";
 items.forEach(([i,q],k)=>{const p=prod(i);m+=`${k+1}. ${p.name} (${p.pack}) × ${q}${p.price?" @ "+rs(p.price):""}\n`;if(p.price)tot+=p.price*q;else all=false});
 if(tot)m+=`\nEstimated total: ${rs(tot)}${all?"":" + items with price to be confirmed"}\n`;
 m+=`\n*Name:* ${n}\n*Mobile:* ${ph}\n*Address:* ${a}`;
 const u=`https://wa.me/${WA}?text=${encodeURIComponent(m)}`;if(!window.open(u,"_blank"))location.href=u}
function order(){const ids=Object.keys(cart).filter(prod),er=$("#derr");if(!ids.length){er.textContent="Your cart is empty. Please add a medicine first.";return}
 const n=$("#nm").value.trim(),ph=$("#ph").value.trim(),ad=$("#ad").value.trim();if(!valid(n,ph,ad,er))return;
 cust.set({n,p:ph,a:ad});wa(ids.map(i=>[i,cart[i]]),n,ph,ad)}
/* Buy Now – quick order popup */
let bn={id:0,q:1};
function renderBN(){const p=prod(bn.id);
 $("#bn-i").innerHTML=`<div class="th">${p.images&&p.images.length?`<img src="${ROOT}images/${p.images[0]}" alt="${p.name}">`:p.icon}</div><div class="mt"><b>${p.name}</b><small>${p.pack}</small><div class="price" style="font-size:1rem">${priceH(p)}</div>
 <div class="tt"><div class="qty"><button type="button" onclick="bq(-1)" aria-label="Decrease">−</button><span>${bn.q}</span><button type="button" onclick="bq(1)" aria-label="Increase">+</button></div><small><b style="display:inline;color:var(--tx)">${p.price?"Total "+rs(p.price*bn.q):"Price confirmed on WhatsApp"}</b></small></div></div>`}
function bq(d){bn.q=Math.max(1,bn.q+d);renderBN()}
function buyNow(id){bn={id,q:qs[id]||1};renderBN();const c=cust.get();$("#bn-n").value=c.n||"";$("#bn-m").value=c.p||"";$("#bn-a").value=c.a||"";$("#bn-e").textContent="";
 $("#qm").classList.add("open");$("#qov").classList.add("open");document.body.style.overflow="hidden";setTimeout(()=>$(c.n?"#bn-a":"#bn-n").focus({preventScroll:true}),120)}
function closeBN(){$("#qm").classList.remove("open");$("#qov").classList.remove("open");document.body.style.overflow=""}
function bnOrder(){const n=$("#bn-n").value.trim(),ph=$("#bn-m").value.trim(),ad=$("#bn-a").value.trim();if(!valid(n,ph,ad,$("#bn-e")))return;
 cust.set({n,p:ph,a:ad});wa([[bn.id,bn.q]],n,ph,ad,"Buy Now");qs[bn.id]=1;const e=$("#q"+bn.id);if(e)e.textContent=1;closeBN()}
document.addEventListener("keydown",e=>{if(e.key==="Escape"){closeBN();closeCart()}});
document.addEventListener("input",e=>{if(e.target.closest&&e.target.closest("#qm"))$("#bn-e").textContent="";else if(e.target.closest&&e.target.closest(".df"))$("#derr").textContent=""});
document.body.insertAdjacentHTML("beforeend",`<div class="fab"><a class="w" href="https://wa.me/${WA}?text=Hello%20Yzar%20Healthcare" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">💬</a><a class="c" href="tel:+919315161042" aria-label="Call us">📞</a></div>
<div class="ov" id="ov" onclick="closeCart()"></div><aside class="drawer" id="drawer" aria-label="Cart"><div class="dh"><b>Your Cart</b><button onclick="closeCart()" aria-label="Close">×</button></div><div class="items" id="items"></div>
<div class="df"><input id="nm" placeholder="Your name" autocomplete="name"><input id="ph" placeholder="Your mobile number" inputmode="tel" autocomplete="tel"><textarea id="ad" rows="2" placeholder="Delivery address with PIN code" autocomplete="street-address"></textarea><p class="cerr" id="derr" role="alert"></p><button class="btn wa" onclick="order()">Order on WhatsApp</button></div></aside>
<div class="qov" id="qov" onclick="closeBN()"></div>
<div class="qm" id="qm" role="dialog" aria-modal="true" aria-labelledby="qt"><div class="qh"><b id="qt">Quick Order</b><button type="button" onclick="closeBN()" aria-label="Close">×</button></div>
<div class="qb"><div class="qi" id="bn-i"></div>
<div class="fr"><label for="bn-n">Your name</label><input id="bn-n" autocomplete="name"></div>
<div class="fr"><label for="bn-m">Mobile number</label><input id="bn-m" type="tel" inputmode="tel" autocomplete="tel" placeholder="10-digit mobile number"></div>
<div class="fr"><label for="bn-a">Delivery address</label><textarea id="bn-a" rows="2" autocomplete="street-address" placeholder="House no, area, city, PIN code"></textarea></div>
<p class="cerr" id="bn-e" role="alert"></p><button class="btn wa" type="button" onclick="bnOrder()">Order on WhatsApp</button>
<p class="qn">🔒 Your details are used only to process this order. WhatsApp opens with your order ready to send.</p></div></div>`);
{const c=cust.get();if(c.n)$("#nm").value=c.n;if(c.p)$("#ph").value=c.p;if(c.a)$("#ad").value=c.a}
const sl=$("#slides");let cur=0,tm;
if(sl){const N=sl.children.length;$("#dots").innerHTML=[...Array(N)].map((_,i)=>`<button onclick="to(${i})" aria-label="Slide ${i+1}"></button>`).join("");
window.to=i=>{cur=(i+N)%N;sl.style.transform=`translateX(-${cur*100}%)`;[...$("#dots").children].forEach((d,k)=>d.classList.toggle("on",k==cur));[...sl.children].forEach((s,k)=>s.classList.toggle("act",k==cur));clearInterval(tm);tm=setInterval(()=>to(cur+1),5000)};
window.go=d=>to(cur+d);let sx=0;const h=$("#hero");h.addEventListener("touchstart",e=>sx=e.touches[0].clientX,{passive:true});
h.addEventListener("touchend",e=>{const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>50)go(d<0?1:-1)});to(0)}
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll(".rv").forEach(el=>io.observe(el));
if($("#q"))$("#q").addEventListener("input",grid);
grid();upd();
const tt=$("#tt");if(tt)tt.onclick=()=>{const d=document.documentElement,n=d.dataset.theme==="dark"?"light":"dark";d.dataset.theme=n;try{localStorage.setItem("yztheme",n)}catch(e){}};
document.body.insertAdjacentHTML("afterbegin",'<div class="prog" id="prog"></div>');
const hd=$("header");addEventListener("scroll",()=>{const y=scrollY,h=document.documentElement.scrollHeight-innerHeight;$("#prog").style.width=(h>0?y/h*100:0)+"%";hd.classList.toggle("sc",y>8)},{passive:true});

const cf=$("#cf");if(cf){
 const get=()=>{const f=cf.elements,v=k=>f[k].value.trim();return{n:v("name"),p:v("phone"),e:v("email"),t:v("topic"),m:v("message")}};
 const check=()=>{const d=get(),er=$("#cerr");cf.querySelectorAll(".bad").forEach(x=>x.classList.remove("bad"));
  const bad=(k,msg)=>{cf.elements[k].classList.add("bad");er.textContent=msg;cf.elements[k].focus();return false};
  if(d.n.length<2)return bad("name","Please enter your name.");
  if(!/^[+]?[0-9 ]{10,14}$/.test(d.p))return bad("phone","Please enter a valid mobile number.");
  if(d.e&&!/^\S+@\S+\.\S+$/.test(d.e))return bad("email","Please enter a valid email address.");
  if(d.m.length<5)return bad("message","Please write your message.");
  er.textContent="";return d};
 const body=d=>`Name: ${d.n}\nMobile: ${d.p}${d.e?"\nEmail: "+d.e:""}\nTopic: ${d.t}\n\nMessage:\n${d.m}`;
 cf.addEventListener("submit",ev=>{ev.preventDefault();const d=check();if(!d)return;
  const u=`https://wa.me/${WA}?text=${encodeURIComponent("*New Enquiry – Yzar Healthcare*\n\n"+body(d))}`;
  if(!window.open(u,"_blank"))location.href=u;toast("✓ Opening WhatsApp… tap send to deliver your message")});
 $("#cmail").addEventListener("click",()=>{const d=check();if(!d)return;
  location.href=`mailto:yzarhealthcare@gmail.com?subject=${encodeURIComponent("Enquiry: "+d.t)}&body=${encodeURIComponent(body(d))}`});
}