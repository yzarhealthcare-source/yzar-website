import json,re,os,shutil,html
DOMAIN="https://yzarhealthcare.com";OUT="site";PH="+91 93151 61042";WA="+91 93545 61001"
LIC="[ADD YOUR DRUG LICENCE NUMBER]"
EMAIL="yzarhealthcare@gmail.com"
prods=json.load(open("products.json",encoding="utf-8"))
def rs(n):return "₹"+format(n,",.0f" if float(n)==int(n) else ",.2f")
def off(p):return round((p["mrp"]-p["price"])/p["mrp"]*100) if p.get("mrp") and p.get("price") and p["mrp"]>p["price"] else 0
def priceh(p):
    if not p.get("price"):return "Price on WhatsApp"
    return f'<span class="now">{rs(p["price"])}</span><s class="old">{rs(p["mrp"])}</s><span class="pct">{off(p)}% off</span>' if off(p) else rs(p["price"])
for i,p in enumerate(prods,1):
    # flexible pricing: only "mrp" -> normal price; mrp <= price -> ignore mrp
    if not p.get("price") and p.get("mrp"):p["price"]=p["mrp"]
    if p.get("mrp") and p.get("price") and p["mrp"]<=p["price"]:p["mrp"]=None
    p["id"]=i;p["slug"]=re.sub(r"[^a-z0-9]+","-",p["name"].lower()).strip("-")
shutil.rmtree(OUT,ignore_errors=True);os.makedirs(OUT+"/medicine");os.makedirs(OUT+"/assets")
if os.path.isdir("images"):shutil.copytree("images",OUT+"/images")
shutil.copy("style.css",OUT+"/assets/style.css");shutil.copy("app.js",OUT+"/assets/app.js")
open(OUT+"/assets/products.js","w",encoding="utf-8").write("const PRODUCTS="+json.dumps(prods,ensure_ascii=False)+";")
NAV=[("index.html","Home"),("medicines.html","Medicines"),("how-to-order.html","How to Order"),("about.html","About"),("faq.html","FAQ"),("contact.html","Contact")]
urls=[]
def page(fn,title,desc,body,active="",sub=False,ld="",hero=None,og=""):
    r="../" if sub else ""
    nav="".join(f'<li><a href="{r}{h}"{" class=on" if h==active else ""}>{t}</a></li>' for h,t in NAV)
    canon=DOMAIN+"/"+fn if fn!="index.html" else DOMAIN+"/"
    urls.append(canon)
    ph=f'<div class="phead"><div class="wrap"><div class="crumb"><a href="{r}index.html">Home</a> › {hero[0]}</div><h1>{hero[0]}</h1><p>{hero[1]}</p></div></div>' if hero else ""
    h=f'''<!DOCTYPE html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{canon}"><meta name="theme-color" content="#1d5fd1">
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canon}">{og}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E💊%3C/text%3E%3C/svg%3E">
<script>(function(){{try{{var t=localStorage.getItem("yztheme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");document.documentElement.dataset.theme=t}}catch(e){{}}}})()</script><link rel="stylesheet" href="{r}assets/style.css">{ld}</head><body>
<header><div class="wrap nav"><a class="logo" href="{r}index.html">Yzar<span> Healthcare</span></a><nav id="nav"><ul>{nav}</ul></nav>
<div class="acts"><button class="ib" id="tt" type="button" aria-label="Switch dark / light theme"><svg class="mo" width="19" height="19" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="su" width="19" height="19" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button><button class="cartbtn" id="cb" type="button" onclick="openCart()" aria-label="Open cart"><svg width="20" height="20" viewBox="0 0 24 24"><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6"/></svg><span id="cc">0</span></button><button class="hb" type="button" onclick="document.getElementById('nav').classList.toggle('open')" aria-label="Menu">☰</button></div></div></header>
<main>{ph}{body}</main>
<footer><div class="wrap"><div><h4>Yzar Healthcare</h4><p>Genuine medicines, easy WhatsApp ordering.</p></div>
<div><h4>Pages</h4>{"".join(f'<a href="{r}{h}">{t}</a>' for h,t in NAV)}</div>
<div><h4>Legal</h4><a href="{r}privacy-policy.html">Privacy Policy</a><a href="{r}terms-disclaimer.html">Terms &amp; Disclaimer</a></div>
<div><h4>Contact</h4><a href="tel:+919315161042">{PH}</a><a href="https://wa.me/919354561001">WhatsApp: {WA}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
<div class="disc"><b>Disclaimer:</b> Information on this site is not medical advice. Consult a registered doctor before using any medicine. Prescription medicines are sold only against a valid prescription. Drug Licence No.: {LIC} · © 2026 Yzar Healthcare.</div></div></footer>
<script src="{r}assets/products.js"></script><script>const ROOT="{r}";</script><script src="{r}assets/app.js"></script></body></html>'''
    fp=OUT+"/"+fn;open(fp,"w",encoding="utf-8").write(h)
def faqld():
    qa=[("How do I order medicines?","Add medicines to your cart, choose quantity, enter your name and address and tap Order on WhatsApp. Our team will confirm your order."),
    ("Do I need a prescription?","Prescription medicines are supplied only against a valid prescription from a registered doctor. Share it with us on WhatsApp."),
    ("How is payment done?","Payment and delivery details are confirmed with you on WhatsApp after you place your order."),
    ("Can I ask about a medicine before buying?","Yes. Call or message us and we will help. For medical advice, always consult your doctor.")]
    return qa,'<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qa]})+'</script>'
org='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Pharmacy","name":"Yzar Healthcare","url":DOMAIN+"/","telephone":"+919315161042","email":EMAIL,"areaServed":"IN"})+'</script>'
# HOME
slides=[("s1","Genuine Medicines, Delivered to Your Door","Quality-checked healthcare products from Yzar Healthcare. Order in a minute, directly on WhatsApp.","medicines.html","Shop Medicines","💊"),
("s2","Order on WhatsApp in 3 Taps","Select medicines, set quantity, and your order goes straight to our team.","how-to-order.html","How It Works","💬"),
("s3","Your Health, Our Priority","Questions about a product? Call or message us, we are happy to help.","contact.html","Contact Us","🩺")]
sh="".join(f'<div class="slide {c}"><div class="wrap"><div><{"h1" if c=="s1" else "h2"} class="hd">{t}</{"h1" if c=="s1" else "h2"}><p>{d}</p><a class="btn" href="{l}">{b}</a></div><div class="big" aria-hidden="true">{i}</div></div></div>' for c,t,d,l,b,i in slides)
home=f'''<div class="slider" id="hero"><div class="slides" id="slides">{sh}</div><button class="arr l" onclick="go(-1)" aria-label="Previous">‹</button><button class="arr r" onclick="go(1)" aria-label="Next">›</button><div class="dots" id="dots"></div></div>
<div class="wrap"><div class="trust"><div class="card rv"><i>✅</i><b>100% Genuine</b><small>Trusted suppliers</small></div><div class="card rv"><i>🚚</i><b>Fast Delivery</b><small>Across India</small></div><div class="card rv"><i>💬</i><b>Easy WhatsApp Order</b><small>No signup needed</small></div><div class="card rv"><i>📞</i><b>Support</b><small>Call in business hours</small></div></div></div>
<section><div class="wrap"><h2 class="rv">Our Medicines</h2><p class="sub rv">Select quantity and add to cart</p><div class="grid" id="grid" data-limit="8"></div><p style="text-align:center;margin-top:28px"><a class="btn g" href="medicines.html">View All Medicines</a></p></div></section>
<section class="alt"><div class="wrap two"><div class="rv"><h2>Why Yzar Healthcare?</h2><ul class="tick"><li>Genuine, quality-checked products</li><li>Simple ordering on WhatsApp</li><li>Personal support by phone</li><li>New medicines added regularly</li></ul><p style="margin-top:18px"><a class="btn g" href="about.html">About Us</a></p></div><div class="card rv" style="font-size:6rem;padding:40px">🏥</div></div></section>'''
page("index.html","Yzar Healthcare – Buy Genuine Medicines Online | Order on WhatsApp","Yzar Healthcare – genuine, quality-checked medicines delivered across India. Choose medicines, set quantity and order instantly on WhatsApp.",home,"index.html",ld=org)
# MEDICINES
page("medicines.html","Buy Medicines Online – Yzar Healthcare","Browse all medicines available at Yzar Healthcare. Select quantity and order directly on WhatsApp.",
 '<section><div class="wrap"><div class="tools"><input id="q" type="search" placeholder="🔍 Search medicine…" aria-label="Search medicines"></div><div class="grid" id="grid"></div></div></section>',"medicines.html",hero=("Our Medicines","Genuine medicines, easy ordering"))
# PRODUCT PAGES
def gallery(p):
    im=p.get("images") or []
    if not im:return f'<div class="pi" aria-hidden="true">{p["icon"]}</div>'
    n=html.escape(p["name"])
    sl="".join(f'<div class="sl"><img src="../images/{f}" alt="{n} image {k+1}" {"" if k==0 else "loading=lazy"}></div>' for k,f in enumerate(im))
    if len(im)==1:return f'<div class="car"><div class="vp"><div class="tr">{sl}</div></div></div>'
    dots="".join(f'<button type="button" onclick="cs({k})" aria-label="Image {k+1}"></button>' for k in range(len(im)))
    th="".join(f'<button type="button" onclick="cs({k})" aria-label="Image {k+1}"><img src="../images/{f}" alt="" loading="lazy"></button>' for k,f in enumerate(im))
    return f'''<div class="car" id="car"><div class="vp"><div class="tr" id="ctr">{sl}</div></div><button class="ar l" type="button" onclick="cg(-1)" aria-label="Previous">‹</button><button class="ar r" type="button" onclick="cg(1)" aria-label="Next">›</button><span class="cn" id="ccn"></span><div class="cd" id="cdt">{dots}</div></div><div class="thumbs" id="cth">{th}</div>
<script>(function(){{var i=0,N={len(im)},t=document.getElementById("ctr"),d=document.getElementById("cdt").children,h=document.getElementById("cth").children,a;
window.cs=function(k){{i=(k+N)%N;t.style.transform="translateX(-"+i*100+"%)";for(var j=0;j<N;j++){{d[j].classList.toggle("on",j==i);h[j].classList.toggle("on",j==i)}}document.getElementById("ccn").textContent=(i+1)+" / "+N;clearTimeout(a);a=setTimeout(function(){{cs(i+1)}},6000)}};
window.cg=function(x){{cs(i+x)}};var sx=0,c=document.getElementById("car");c.addEventListener("touchstart",function(e){{sx=e.touches[0].clientX}},{{passive:true}});c.addEventListener("touchend",function(e){{var x=e.changedTouches[0].clientX-sx;if(Math.abs(x)>40)cg(x<0?1:-1)}});cs(0)}})();</script>'''
def lst(v):
    if not v:return ""
    if isinstance(v,list):return "<ul>"+"".join(f"<li>{html.escape(x)}</li>" for x in v)+"</ul>"
    return "<p>"+html.escape(v).replace("\n","</p><p>")+"</p>"
def details(p):
    secs=[("Composition","composition"),("Uses &amp; Benefits","uses"),("How to Use","how_to_use"),("Side Effects","side_effects"),("Warnings &amp; Precautions","warnings"),("Storage","storage")]
    out=""
    if p.get("long_desc"):out+=f'<details open><summary>About {html.escape(p["name"])}</summary><div class="bd">{lst(p["long_desc"])}</div></details>'
    for k,(t,key) in enumerate(secs):
        if p.get(key):out+=f'<details{" open" if k==0 and not p.get("long_desc") else ""}><summary>{t}</summary><div class="bd">{lst(p[key])}</div></details>'
    rows=[("Composition",p.get("info")),("Pack size",p.get("pack")),("Manufacturer",p.get("manufacturer")),("Prescription","Required" if p.get("rx") else "Not required")]
    out+='<details><summary>Product Information</summary><div class="bd"><table>'+"".join(f"<tr><td>{a}</td><td>{html.escape(str(v))}</td></tr>" for a,v in rows if v)+"</table></div></details>"
    return f'<div class="pdet"><h2>Product Details</h2>{out}</div>'
for p in prods:
    ld={"@context":"https://schema.org","@type":"Product","name":p["name"],"description":(p["desc"]+" "+(p.get("long_desc") or "")).strip(),"brand":{"@type":"Brand","name":"Yzar Healthcare"}}
    if p.get("images"):ld["image"]=[f'{DOMAIN}/images/{f}' for f in p["images"]]
    if p["price"]:ld["offers"]={"@type":"Offer","priceCurrency":"INR","price":str(p["price"]),"availability":"https://schema.org/InStock","url":f'{DOMAIN}/medicine/{p["slug"]}.html'}
    b=f'''<section><div class="wrap"><div class="crumb" style="color:var(--mu)"><a href="../index.html">Home</a> › <a href="../medicines.html">Medicines</a> › {html.escape(p["name"])}</div>
<div class="pd"><div style="min-width:0">{gallery(p)}</div><div><h1>{html.escape(p["name"])}</h1><p>{html.escape(p["info"])} · Pack: {html.escape(p["pack"])}</p>
{'<span class="rx">Prescription required</span>' if p["rx"] else ''}<div class="price">{priceh(p)}</div><p>{html.escape(p["desc"])}</p>
<div class="cta"><div class="qty"><button onclick="qty({p["id"]},-1)" aria-label="Decrease">−</button><span id="q{p["id"]}">1</span><button onclick="qty({p["id"]},1)" aria-label="Increase">+</button></div><button class="btn g" onclick="add({p["id"]})">Add to Cart</button>
<a class="btn wa" target="_blank" rel="noopener" href="https://wa.me/919354561001?text=Hello%2C%20I%20want%20to%20order%20{p["name"].replace(" ","%20")}">Ask on WhatsApp</a></div>
<p style="font-size:.85rem;margin-top:18px">Consult your doctor before use. Read the label and leaflet carefully.</p></div></div>{details(p)}</div></section>'''
    page(f'medicine/{p["slug"]}.html',f'{p["name"]} – Buy Online | Yzar Healthcare',f'Buy {p["name"]} ({p["info"]}, {p["pack"]}) online from Yzar Healthcare and order on WhatsApp.',b,"medicines.html",True,'<script type="application/ld+json">'+json.dumps(ld)+'</script>',og=(f'<meta property="og:image" content="{DOMAIN}/images/{p["images"][0]}">' if p.get("images") else ""))
# HOW
page("how-to-order.html","How to Order Medicines Online – Yzar Healthcare","Order medicines in 4 easy steps: choose, add details, send on WhatsApp, we confirm and deliver.",
 '<section><div class="wrap"><div class="steps"><div class="card rv"><b>Choose medicines</b><small>Browse the list and set the quantity you need.</small></div><div class="card rv"><b>Add details</b><small>Open the cart, enter your name and delivery address.</small></div><div class="card rv"><b>Send on WhatsApp</b><small>Tap “Order on WhatsApp”. Your order reaches us instantly.</small></div><div class="card rv"><b>We confirm &amp; deliver</b><small>We confirm price and payment details, then dispatch.</small></div></div><p style="text-align:center;margin-top:36px"><a class="btn g" href="medicines.html">Start Ordering</a></p></div></section>',"how-to-order.html",hero=("How to Order","Simple, fast and secure"))
# ABOUT
page("about.html","About Yzar Healthcare – Genuine Medicines","Learn about Yzar Healthcare, our commitment to genuine medicines and simple WhatsApp ordering.",
 '<section><div class="wrap two"><div class="rv"><h2>Who We Are</h2><p style="color:var(--mu);margin-top:10px">Yzar Healthcare makes quality medicines easy to reach. We focus on genuine products, transparent ordering and quick personal support, so you do not have to hunt for the medicines you need.</p><ul class="tick"><li>Genuine, quality-checked products</li><li>Simple ordering on WhatsApp</li><li>Personal support by phone</li><li>New medicines added regularly</li></ul></div><div class="card rv" style="font-size:6rem;padding:40px">🏥</div></div></section>',"about.html",hero=("About Us","Your trusted healthcare partner"))
# FAQ
qa,fld=faqld()
page("faq.html","FAQ – Yzar Healthcare","Answers to common questions about ordering medicines, prescriptions and payment at Yzar Healthcare.",
 '<section><div class="wrap" style="max-width:760px">'+"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in qa)+'</div></section>',"faq.html",ld=fld,hero=("FAQ","Quick answers"))
# CONTACT
page("contact.html","Contact Yzar Healthcare – Call, WhatsApp or Email","Contact Yzar Healthcare: call +91 93151 61042, WhatsApp +91 93545 61001 or email yzarhealthcare@gmail.com. Send an enquiry from the form.",
 f'''<section><div class="wrap"><div class="contact"><a class="card rv" href="tel:+919315161042"><i>📞</i><b>Call Us</b><small>{PH}</small></a><a class="card rv" href="https://wa.me/919354561001" target="_blank" rel="noopener"><i>💬</i><b>WhatsApp</b><small>{WA}</small></a><a class="card rv" href="mailto:{EMAIL}"><i>✉️</i><b>Email</b><small>{EMAIL}</small></a></div></div></section>
<section class="alt"><div class="wrap" style="max-width:720px"><h2 class="rv">Send Us an Enquiry</h2><p class="sub rv">Fill the form and tap send. Your message opens in WhatsApp, ready to send to our team.</p>
<form id="cf" class="cform rv" novalidate>
<div class="fr"><label for="cn">Your name *</label><input id="cn" name="name" autocomplete="name" required></div>
<div class="fr"><label for="cp">Mobile number *</label><input id="cp" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="10-digit mobile number"></div>
<div class="fr"><label for="ce">Email (optional)</label><input id="ce" name="email" type="email" autocomplete="email"></div>
<div class="fr"><label for="ct">Topic</label><select id="ct" name="topic"><option>Medicine enquiry</option><option>Order help</option><option>Prescription medicine</option><option>Bulk / wholesale</option><option>Other</option></select></div>
<div class="fr"><label for="cm">Your message *</label><textarea id="cm" name="message" rows="5" required></textarea></div>
<p id="cerr" class="cerr" role="alert"></p>
<div class="cta"><button class="btn wa" type="submit">Send on WhatsApp</button><button class="btn g" type="button" id="cmail">Send by Email</button></div>
</form></div></section>''',"contact.html",hero=("Contact Us","We are here to help"))
# LEGAL
page("privacy-policy.html","Privacy Policy – Yzar Healthcare","How Yzar Healthcare uses your name, phone number and address to process orders.",
 '<section><div class="wrap doc"><h2>Information we collect</h2><p>When you order, you share your name, mobile number, delivery address and the medicines you want. This is sent to us via WhatsApp.</p><h2>How we use it</h2><p>We use it only to confirm, process and deliver your order and to answer your questions.</p><h2>Sharing</h2><p>We do not sell your information. It may be shared with delivery partners only as needed to deliver your order.</p><h2>Cart data</h2><p>Your cart is saved only in your own browser.</p><h2>Contact</h2><p>Questions? Call '+PH+'.</p></div></section>',hero=("Privacy Policy","Your data, handled with care"))
page("terms-disclaimer.html","Terms &amp; Medical Disclaimer – Yzar Healthcare","Terms of use and medical disclaimer for Yzar Healthcare.",
 '<section><div class="wrap doc"><h2>Medical disclaimer</h2><p>Content on this website is for general information and is not medical advice. Always consult a registered doctor before using any medicine.</p><h2>Prescriptions</h2><p>Prescription medicines are supplied only against a valid prescription.</p><h2>Orders &amp; prices</h2><p>Orders are confirmed only after our team replies on WhatsApp. Prices and availability may change.</p><h2>Returns</h2><p>Medicines cannot be returned once delivered, except for wrong or damaged products reported at delivery.</p></div></section>',hero=("Terms &amp; Disclaimer","Please read carefully"))
h4=open(OUT+"/index.html",encoding="utf-8").read().replace("<title>","<title>Page not found – ",1)
h4=re.sub(r"<title>.*?</title>","<title>Page not found – Yzar Healthcare</title>",h4,flags=re.S)
h4=re.sub(r'<link rel="canonical"[^>]*>','<meta name="robots" content="noindex">',h4)
open(OUT+"/404.html","w",encoding="utf-8").write(h4)
open(OUT+"/.htaccess","w").write("ErrorDocument 404 /404.html\nOptions -Indexes\n<IfModule mod_deflate.c>\nAddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml\n</IfModule>\n<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType image/jpeg \"access plus 1 month\"\nExpiresByType image/png \"access plus 1 month\"\nExpiresByType image/webp \"access plus 1 month\"\nExpiresByType image/svg+xml \"access plus 1 month\"\nExpiresByType text/css \"access plus 1 week\"\nExpiresByType application/javascript \"access plus 1 week\"\n</IfModule>\n")
open(OUT+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc></url>" for u in urls)+"</urlset>")
open(OUT+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built",len(urls),"pages")
