(function(){
var $=function(s){return document.querySelector(s)},ROOT=(window.SITE&&window.SITE.root)||"",RM=matchMedia("(prefers-reduced-motion:reduce)").matches,R0=document.documentElement;
function CALM(){return R0.classList.contains("calm")||RM}
function toast(t){var e=$("#toast");e.textContent=t;e.classList.add("show");clearTimeout(toast.t);toast.t=setTimeout(function(){e.classList.remove("show")},2800)}
function rain(em){for(var i=0;i<26;i++){var s=document.createElement("span");s.className="rain";s.textContent=em[i%em.length];s.style.left=Math.random()*100+"vw";s.style.animationDuration=2+Math.random()*2+"s";document.body.appendChild(s);setTimeout(function(x){x.remove()},4200,s)}}
$("#th").onclick=function(){var r=document.documentElement,l=getComputedStyle(r).colorScheme==="light",n=l?"dark":"light";r.setAttribute("data-theme",n);try{localStorage.setItem("t",n)}catch(e){}};
try{var st=localStorage.getItem("t");if(st)document.documentElement.setAttribute("data-theme",st)}catch(e){}
function e(t){return String(t==null?"":t).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function u(x){return /^https?:\/\//.test(x||"")?e(x):"#"}
function fd(d){var x=new Date(d);return isNaN(x)?e(d):x.toLocaleDateString("en-GB",{day:"numeric",month:"short",year:"numeric"})}

var io=window.IntersectionObserver?new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){var el=x.target;el.classList.add("in");io.unobserve(el);setTimeout(function(){el.classList.remove("rv","in");el.style.removeProperty("--d")},1600)}})},{threshold:.12}):null;
function rv(){if(CALM()||!io)return;document.querySelectorAll(".bc,.card,.it,.plinks a,.pc,.vc,.er,.fcols>div,.ftop,.fh,.gc,.start a,.quote").forEach(function(el){if(el.dataset.o)return;el.dataset.o=1;el.classList.add("rv");var s=Array.prototype.indexOf.call(el.parentNode.children,el);el.style.setProperty("--d",s%6);io.observe(el)})}
document.querySelectorAll(".nm .w").forEach(function(w,k){var t=w.textContent;w.textContent="";w.setAttribute("aria-hidden","true");t.split("").forEach(function(c,i){var x=document.createElement("span");x.textContent=c;x.style.setProperty("--i",i+k*5);w.appendChild(x)})});
var PG=[["Home","home"],["About","about"],["Writing","writing"],["Videos","videos"],["Projects","projects"],["Now","now"],["Explore","explore"],["Games","games"],["Connect","connect"]],pi=0,DB={d:null,x:[]};
var PD={home:"Start here",about:"Background, education, journey",writing:"Articles sorted by subject",videos:"Two YouTube channels",projects:"Build log with status and lessons",now:"What I’m doing at the moment",explore:"Notes, books, experiences",games:"Mind games and a daily riddle",connect:"Email and every public profile"};
var SY={home:"start main",about:"bio who pramod education journey capgemini trader",writing:"articles blog essays posts medium substack read",videos:"youtube watch channel sevenlearn",projects:"build apps github code log",now:"current working learning reading goals",explore:"notes books experiences learning",games:"arcade play puzzle brain mind riddle memory fun",connect:"contact email hire social profiles links"};
var STOP=["latest","new","recent","the","a","my","what","is","about","show","me","pramod","his","of"];
function buildIdx(){var x=[],d=DB.d;
PG.forEach(function(p){x.push({t:p[0],k:"Page",d:PD[p[1]],h:p[1],s:p[0]+" "+PD[p[1]]+" "+SY[p[1]]})});
x.push({t:"Surprise me",k:"Page",d:"A random page",h:"?",s:"surprise random"});
[{t:"Toggle light or dark",d:"Switch theme",s:"theme dark light mode toggle",act:function(){$("#th").click()}},{t:"Calm mode",d:"Turn motion and cursor off or on",s:"calm motion animation cursor quiet",act:function(){var c=$("#calm");if(c)c.click()}},{t:"Copy email address",d:"pramodtidkework@gmail.com",s:"email copy contact mail",act:function(){try{navigator.clipboard.writeText("pramodtidkework@gmail.com");toast("Email copied")}catch(x){toast("pramodtidkework@gmail.com")}}},{t:"Open the assistant",d:"Ask about the site",s:"chat assistant ask help bot",act:function(){openChat()}}].forEach(function(a){a.k="Action";x.push(a)});
(typeof GM!=="undefined"?GM:[]).forEach(function(g){x.push({t:g.t,k:"Game",d:g.d,h:"games",g:g.id,s:g.t+" "+g.d+" game play mind brain puzzle"})});
if(!d)return x;
d.WR.forEach(function(i){x.push({t:i.title,k:"Article",d:i.platform+" · "+i.category,p:i.p,s:[i.title,i.platform,i.category,i.description,"article writing blog"].join(" ")})});
d.VD.forEach(function(i){x.push({t:i.title,k:"Video",d:i.channel,u:i.url,s:[i.title,i.channel,"video youtube watch"].join(" ")})});
d.PJ.forEach(function(i){x.push({t:i.name,k:"Project",d:i.status+" · "+i.problem,p:i.p,s:[i.name,i.status,i.problem,i.lesson,(i.tech||[]).join(" "),"project build"].join(" ")})});
d.EX.forEach(function(i){x.push({t:i.title,k:i.type,d:i.text,h:"explore",s:[i.title,i.type,i.text].join(" ")})});
d.PF.forEach(function(i){x.push({t:i.name,k:"Profile",d:i.note,u:i.url,s:[i.name,i.note,i.group,"profile social link"].join(" ")})});
[["Working on","working_on"],["Learning","learning"],["Reading","reading"],["Goals","goals"],["Next","next"]].forEach(function(n){(d.N[n[1]]||[]).forEach(function(t){x.push({t:t,k:"Now",d:n[0],h:"now",s:t+" "+n[0]+" now"})})});
return x}
DB.x=buildIdx();
function sc(x,q){var h=x.s.toLowerCase(),t=x.t.toLowerCase(),s=0;for(var i=0;i<q.length;i++){if(h.indexOf(q[i])<0)return 0;s+=t.indexOf(q[i])>-1?3:1}return s+(x.k==="Page"?.5:0)}
function search(v){var q=v.toLowerCase().split(/\s+/).filter(function(w){return w&&STOP.indexOf(w)<0});if(!q.length)return[];return DB.x.map(function(x){return[sc(x,q),x]}).filter(function(a){return a[0]}).sort(function(a,b){return b[0]-a[0]}).map(function(a){return a[1]})}
function pr(){var v=$("#pq").value.trim(),l=$("#pl"),f,head="";l.innerHTML="";
if(!v){head="Suggested";f=DB.x.filter(function(x){return x.k==="Page"&&x.h!=="?"}).concat(DB.x.filter(function(x){return x.k==="Article"||x.k==="Video"||x.k==="Project"}).slice(0,3))}
else{f=search(v).slice(0,7);f.push({t:"Ask the assistant: “"+v+"”",k:"Chat",ask:v})}
pi=Math.min(pi,Math.max(0,f.length-1));
if(head)l.insertAdjacentHTML("beforeend",'<li class="lb">'+head+'</li>');
f.forEach(function(x,i){var li=document.createElement("li");if(i===pi)li.className="on";li.innerHTML="<span><b>"+e(x.t)+"</b>"+(x.d?"<small>"+e(x.d)+"</small>":"")+'</span><em class="tg">'+e(x.k)+"</em>";li.onclick=function(){pick(x)};l.appendChild(li)});pr.f=f}
function closeP(){$("#pal").classList.remove("show")}
function openP(){$("#pal").classList.add("show");$("#pq").value="";pi=0;pr();$("#pq").focus()}
function pick(x){closeP();if(x.act){x.act();return}if(x.ask){openChat(x.ask);return}if(x.g){location.href=ROOT+"games/?g="+x.g;return}if(x.p){location.href=ROOT+x.p;return}if(x.u){window.open(x.u,"_blank","noopener");return}var h=x.h;if(h==="?"){var r=["about","writing","videos","projects","now","explore","games"];h=r[Math.floor(Math.random()*r.length)]}location.href=ROOT+(h==="home"?"":h+"/")}
$("#ph").innerHTML="Try:"+["devops","youtube","projects","contact","risk"].map(function(w){return"<span>"+w+"</span>"}).join("");
$("#ph").onclick=function(ev){if(ev.target.tagName==="SPAN"){$("#pq").value=ev.target.textContent;pi=0;pr();$("#pq").focus()}};
/* assistant */
var cm=$("#cm"),cs=$("#cs"),CD=["Who is Pramod?","Latest writing","What is he building?","How can I contact him?"],opened=false;
function bub(h,c){var d=document.createElement("div");d.className="mg "+c;d.innerHTML=h;cm.appendChild(d);cm.scrollTop=cm.scrollHeight;return d}
function chips(a){cs.innerHTML="";a.forEach(function(t){var b=document.createElement("button");b.textContent=t;b.onclick=function(){say(t)};cs.appendChild(b)})}
function openChat(q){$("#cp").classList.add("show");if(!opened){opened=true;bub("Hi, I’m the assistant for this site. Ask me about Pramod’s background, writing, videos, projects or how to reach him.","b");chips(CD)}$("#ci").focus();if(q)say(q)}
function say(t){t=String(t).trim();if(!t)return;bub(e(t),"u");$("#ci").value="";var w=bub("…","b");setTimeout(function(){var r=answer(t);w.innerHTML=r.h;chips(r.c||CD);cm.scrollTop=cm.scrollHeight},350)}
$("#cbt").onclick=function(){var p=$("#cp");if(p.classList.contains("show"))p.classList.remove("show");else openChat()};
$("#cx").onclick=function(){$("#cp").classList.remove("show")};
$("#cg").onclick=function(){say($("#ci").value)};
$("#ci").onkeydown=function(ev){if(ev.key==="Enter")say(this.value)};
addEventListener("keydown",function(ev){if(ev.key==="Escape")$("#cp").classList.remove("show")});
function LA(t,h){return'<a href="'+ROOT+(h==="home"?"":h+"/")+'">'+e(t)+"</a>"}
function LA2(t,p){return'<a href="'+ROOT+p+'">'+e(t)+"</a>"}
function LX(t,h){return'<a href="'+u(h)+'" target="_blank" rel="noopener">'+e(t)+"</a>"}
function UL(a){return"<ul>"+a.map(function(s){return"<li>"+s+"</li>"}).join("")+"</ul>"}
function ANY(l,w){return w.some(function(k){return new RegExp("\\b"+k).test(l)})}
function answer(q){var l=q.toLowerCase(),d=DB.d||{WR:[],VD:[],PJ:[],EX:[],PF:[],N:{},A:{}};
function R(h,c){return{h:h,c:c}}
function tag(i){return i.sample?" (sample)":""}
if(/^(hi|hello|hey|namaste|yo)\b/.test(l))return R("Hello! What would you like to know about Pramod or this site?");
if(ANY(l,["thank"]))return R("Anytime. Anything else?");
var pj=d.PJ.filter(function(p){return l.indexOf(p.name.toLowerCase())>-1})[0];
if(pj)return R("<b>"+e(pj.name)+"</b> ("+e(pj.status)+"): "+e(pj.problem)+(pj.tech&&pj.tech.length?"<br>Tech: "+e(pj.tech.join(", ")):"")+(pj.lesson?"<br>Lesson: "+e(pj.lesson):"")+(pj.github?"<br>"+LX("GitHub",pj.github):"")+(pj.live?" · "+LX("Live site",pj.live):""),["Show all projects","What is he learning now?"]);
if(ANY(l,["resume","cv\\b"]))return R("The resume is shared directly with recruiters rather than listed publicly. Email Pramod and ask for it: "+'<a href="mailto:pramodtidkework@gmail.com">pramodtidkework@gmail.com</a>',["How can I contact him?"]);
if(ANY(l,["contact","email","mail","reach","hire","hiring","collab","work with","phone","call"]))return R('The best way to reach Pramod is email: <a href="mailto:pramodtidkework@gmail.com">pramodtidkework@gmail.com</a>. Every public profile is on the '+LA("Connect page","connect")+".",["Show all social profiles","Who is Pramod?"]);
if(ANY(l,["game","play","puzzle","riddle","brain","mind"]))return R("There’s a small arcade on the "+LA("Games page","games")+":"+UL(GM.map(function(g){return"<b>"+e(g.t)+"</b> — "+e(g.d)})),["Who is Pramod?"]);
if(ANY(l,["notes","book","explore"]))return R(d.EX.length?"From Explore:"+UL(d.EX.slice(0,4).map(function(i){return e(i.title)+" ("+e(i.type)+")"+tag(i)}))+"More on the "+LA("Explore page","explore")+".":"Nothing in Explore yet.");
if(ANY(l,["now\\b","current","learning","reading","working on","goal","next","doing"])){var N=d.N,o=[];[["Working on","working_on"],["Learning","learning"],["Reading","reading"],["Goals","goals"],["Next","next"]].forEach(function(n){if((N[n[1]]||[]).length)o.push("<b>"+n[0]+":</b> "+e(N[n[1]].join("; ")))});return R(UL(o)+"Full snapshot on the "+LA("Now page","now")+".",["What is he building?","Latest writing"])}
if(ANY(l,["video","youtube","watch","channel"])){var v=d.VD.slice(0,3);return R("Two YouTube channels: "+LX("@thepramodtidke","https://www.youtube.com/@thepramodtidke")+" and "+LX("SevenLearn","https://www.youtube.com/@sevenlearnn")+"."+(v.length?"<br>Latest:"+UL(v.map(function(i){return LX(i.title,i.url)+" — "+e(i.channel)+tag(i)})):""),["Latest writing","Show all social profiles"])}
if(ANY(l,["article","writing","write","wrote","blog","essay","post","newsletter"])){var K={"Technology & AI":["ai\\b","tech"],"Business & Entrepreneurship":["business","entrepreneur"],"Finance & Economics":["finance","econom","money"],"Marketing & Creativity":["marketing","creativ"],"Personal Development":["personal","growth"],"Life & Experiences":["life"]},cat=Object.keys(K).filter(function(c){return ANY(l,K[c])})[0],w=d.WR.filter(function(i){return!cat||i.category===cat}).slice(0,3);return R(w.length?(cat?"Latest in "+e(cat)+":":"Latest writing:")+UL(w.map(function(i){return LA2(i.title,i.p)+" — "+e(i.platform)+", "+fd(i.date)+tag(i)}))+"Browse by subject on the "+LA("Writing page","writing")+".":"Nothing published in that subject yet. See the "+LA("Writing page","writing")+".",["Show all videos","What is he building?"])}
if(ANY(l,["project","build","built","app\\b","apps\\b","github","code"])&&!/github (profile|account)/.test(l)){return R(d.PJ.length?"Projects:"+UL(d.PJ.map(function(i){return"<b>"+e(i.name)+"</b> ("+e(i.status)+") — "+e(i.problem)+tag(i)}))+"Details on the "+LA("Projects page","projects")+".":"No projects listed yet.",["What is he learning now?","Which tech does he use?"])}
if(ANY(l,["study","studied","education","degree","college","universit","graduat","qualification"]))return R("Pramod has a BE in Computer Science from G. H. Raisoni Institute (2020).",["Tell me about his career","Who is Pramod?"]);
if(ANY(l,["capgemini","panasonic","experience","career","job","work history","worked","journey","background","devops engineer","ivi","timeline"]))return R(UL(["<b>2020:</b> BE in Computer Science, G. H. Raisoni Institute","<b>2020–2022:</b> Trader and investor","<b>Mar 2022 – Nov 2023:</b> DevOps Engineer at Capgemini, on the Panasonic Automotive Linux IVI platform","<b>2023–present:</b> Building independently across DevOps, Cloud and AI, and marketing"])+"See the "+LA("About page","about")+".",["Tell me about the agency","Which tech does he use?"]);
if(ANY(l,["trad","invest","stock"]))return R("From 2020 to 2022 Pramod was a trader and investor, which he says taught him how markets and risk really work.",["Tell me about his career"]);
if(ANY(l,["agency","digitomotive","dg2motive","markase","client","freelanc","marketing"]))return R("Alongside DevOps, Pramod runs a digital marketing agency (Digitomotive/DG2Motive) for US clients, and has a freelancing brand, "+LX("Markase","https://markase.com")+".",["Show all social profiles","How can I contact him?"]);
var m=d.PF.filter(function(p){var ws=p.name.toLowerCase().split(" ").filter(function(w){return w!=="on"&&w!=="x"});if(p.name==="X")return/\btwitter\b|\bon x\b/.test(l);return ws.some(function(w){return l.indexOf(w)>-1})});
if(m.length||ANY(l,["social","profile","platform","follow","link"]))return R((m.length?"Here:":"All public profiles:")+UL((m.length?m:d.PF).map(function(p){return LX(p.name,p.url)+" — "+e(p.note)})),["How can I contact him?"]);
if(ANY(l,["skill","stack","tool","technolog","devops","cloud","docker","kubernetes","ci/cd","ai\\b"])){var T=[];d.PJ.forEach(function(p){(p.tech||[]).forEach(function(t){if(T.indexOf(t)<0)T.push(t)})});return R("Pramod works across DevOps, Cloud and AI, plus marketing. Technologies in his project log: "+e(T.join(", "))+".",["What is he building?","Tell me about his career"])}
if(ANY(l,["site","website","purpose","this page"]))return R("This site is Pramod’s home on the internet, linking to everything he publishes. It covers five things:"+UL(["Think &amp; Write","Build &amp; Create","Learn &amp; Explore","Experience &amp; Share","Connect &amp; Publish"]));
if(ANY(l,["who","about","pramod","introduc","tell me","bio","yourself"]))return R(e(d.A.intro||"Computer science graduate, former trader and DevOps engineer, now building independently.")+" Tagline: <i>Building with technology. Exploring with curiosity.</i> More on the "+LA("About page","about")+".",["Tell me about his career","What is he building?"]);
var s=search(q).filter(function(x){return!x.act}).slice(0,3);
if(s.length)return R("I’m not sure I have that exactly, but these may help:"+UL(s.map(function(x){return x.p?LA2(x.t,x.p)+" ("+e(x.k)+")":x.u?LX(x.t,x.u)+" ("+e(x.k)+")":LA(x.t,x.h)+" ("+e(x.k)+")"})));
return R("I only know what is on this site. Try asking about his background, writing, videos, projects, or how to contact him.")}
$("#sb").onclick=openP;$("#pq").oninput=function(){pi=0;pr()};
$("#pq").onkeydown=function(e){if(e.key==="ArrowDown"){pi=Math.min(pi+1,pr.f.length-1);pr();e.preventDefault()}else if(e.key==="ArrowUp"){pi=Math.max(pi-1,0);pr();e.preventDefault()}else if(e.key==="Enter"&&pr.f[pi])pick(pr.f[pi])};
$("#pal").onclick=function(e){if(e.target===this)closeP()};
addEventListener("keydown",function(e){if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==="k"){e.preventDefault();openP()}if(e.key==="Escape")closeP()});

var nav=$("#nav"),mb=$("#mb"),mq=matchMedia("(max-width:820px)");
function closeDD(ex){nav.querySelectorAll(".dg.open").forEach(function(g){if(g!==ex){g.classList.remove("open");g.querySelector(".dd").setAttribute("aria-expanded","false")}})}
function closeAll(){closeDD();nav.classList.remove("open");if(mb)mb.setAttribute("aria-expanded","false")}
nav.querySelectorAll(".dd").forEach(function(b){b.addEventListener("click",function(){if(mq.matches&&b.closest(".nl"))return;var g=b.parentNode,o=!g.classList.contains("open");closeDD(g);g.classList.toggle("open",o);b.setAttribute("aria-expanded",o)})});
if(mb)mb.onclick=function(){closeDD();var o=nav.classList.toggle("open");mb.setAttribute("aria-expanded",o)};
nav.querySelectorAll(".nl a,.dm a").forEach(function(a){a.addEventListener("click",closeAll)});
document.addEventListener("click",function(ev){if(!nav.contains(ev.target))closeAll()});
addEventListener("keydown",function(ev){if(ev.key!=="Escape")return;var inside=nav.contains(document.activeElement),menu=nav.classList.contains("open"),dd=nav.querySelector(".dg.open>.dd");if(!menu&&!dd)return;closeAll();if(inside){var t=menu&&mb&&mq.matches?mb:dd;if(t)t.focus()}});
function syncNav(){nav.querySelectorAll(".nl .dd").forEach(function(b){if(mq.matches){b.tabIndex=-1;b.setAttribute("aria-expanded","true")}else{b.removeAttribute("tabindex");b.setAttribute("aria-expanded",b.parentNode.classList.contains("open"))}})}
syncNav();if(mq.addEventListener)mq.addEventListener("change",syncNav);else if(mq.addListener)mq.addListener(syncNav);
var cb=$("#calm");if(cb){cb.setAttribute("aria-pressed",R0.classList.contains("calm")||RM);cb.onclick=function(){var on=R0.classList.toggle("calm");try{localStorage.setItem("calm",on?"1":"0")}catch(x){}cb.setAttribute("aria-pressed",on);toast(on?"Calm mode on":"Calm mode off")}}
var hn=$(".nm"),hs=$("#hst");
function buildSt(){hs.innerHTML=hs.textContent.trim().split(/\s+/).map(function(w){return'<span class="sw">'+w+"</span>"}).join(" ")}
if(hs&&!CALM())buildSt();
function onscroll(){var y=scrollY,h=document.documentElement.scrollHeight-innerHeight;$("#bar").style.width=h>0?y/h*100+"%":"0";if(!hn||CALM())return;var k=Math.min(1,y/innerHeight);hn.style.transform="translateY("+y*.15+"px)";hn.style.opacity=String(1-k*.85);if(hs){var r=hs.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*.88-r.top)/(r.height+innerHeight*.3))),w=hs.children,n=w.length,a=p*n;for(var i=0;i<n;i++)w[i].classList.toggle("on",i<a)}}
addEventListener("scroll",onscroll,{passive:true});
var rot=$("#rot");if(rot&&!CALM()){var WORDS=[];try{WORDS=JSON.parse(rot.dataset.w)}catch(x){}if(WORDS.length>1){var wi=0;setInterval(function(){wi=(wi+1)%WORDS.length;rot.style.opacity=0;rot.style.transform="translateY(.3em)";setTimeout(function(){rot.textContent=WORDS[wi];rot.style.opacity=1;rot.style.transform="none"},250)},2200)}}
var ptEl=$(".pt");if(ptEl&&!CALM())addEventListener("pointermove",function(ev){var x=ev.clientX/innerWidth-.5,y=ev.clientY/innerHeight-.5;ptEl.style.transform="translate("+x*18+"px,"+y*18+"px) rotate("+x*4+"deg)"});
document.querySelectorAll("[data-filter]").forEach(function(bar){var tgt=$(bar.dataset.filter);bar.querySelectorAll(".fc").forEach(function(b){b.onclick=function(){bar.querySelectorAll(".fc").forEach(function(x){x.classList.remove("on")});b.classList.add("on");var v=b.dataset.v;tgt.querySelectorAll("[data-cat]").forEach(function(it){it.hidden=!(v==="All"||it.dataset.cat===v)})}})});
document.querySelectorAll("[data-copy]").forEach(function(b){b.onclick=function(){var t=b.dataset.copy;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){toast("Link copied")}).catch(function(){toast(t)})}});
document.querySelectorAll(".yt").forEach(function(b){b.onclick=function(){var f=document.createElement("iframe");f.src="https://www.youtube-nocookie.com/embed/"+b.dataset.id+"?autoplay=1";f.allow="autoplay; encrypted-media; picture-in-picture";f.allowFullscreen=true;f.title=b.getAttribute("aria-label")||"Video";f.style.cssText="width:100%;aspect-ratio:16/9;border:0;border-radius:20px";b.replaceWith(f)}});
if(/[?&]sent=1/.test(location.search))toast("Thanks! Your message was sent.");
var ot=document.title;document.addEventListener("visibilitychange",function(){document.title=document.hidden?"Come back, Pramod misses you 👀":ot});
var kc=[38,38,40,40,37,39,37,39,66,65],ki=0;addEventListener("keydown",function(ev){ki=ev.keyCode===kc[ki]?ki+1:0;if(ki===kc.length){ki=0;toast("Cheat code accepted: +1 coffee ☕");rain(["☕","🚀","✨","💡"])}});
function intro(){var el=$("#intro");if(!el){R0.classList.add("go");return}var seen=false;try{seen=localStorage.getItem("seen2")}catch(x){}
if(seen||CALM()){el.style.display="none";R0.classList.add("go");return}
scrollTo(0,0);R0.classList.add("il");var n=$("#icn"),bar=$("#ibar i"),t0=performance.now(),D=1100,done=false;
function fin(){if(done)return;done=true;n.textContent="100";bar.style.width="100%";setTimeout(function(){el.classList.add("out");R0.classList.remove("il");R0.classList.add("go");setTimeout(function(){el.style.display="none"},1100)},200);try{localStorage.setItem("seen2","1")}catch(x){}}
(function f(t){var k=Math.min(1,(t-t0)/D),q=1-Math.pow(1-k,3);n.textContent=Math.round(q*100);bar.style.width=q*100+"%";if(k<1&&!done)requestAnimationFrame(f);else fin()})(t0);el.onclick=fin}
var fine=matchMedia("(hover:hover) and (pointer:fine)").matches,mx=-100,my=-100,rx=-100,ry=-100,ring=$("#cr"),dot=$("#cd");
if(fine){R0.classList.add("cc");addEventListener("pointermove",function(ev){mx=ev.clientX;my=ev.clientY;R0.classList.add("cm");var t=ev.target.closest&&ev.target.closest("a,button,input,textarea");ring.className=t?"h":""});
(function lp(){if(!CALM()){rx+=(mx-rx)*.16;ry+=(my-ry)*.16;ring.style.transform="translate3d("+rx+"px,"+ry+"px,0)";dot.style.transform="translate3d("+mx+"px,"+my+"px,0)"}requestAnimationFrame(lp)})()}
if("serviceWorker" in navigator&&location.protocol==="https:")navigator.serviceWorker.register(ROOT+"sw.js").catch(function(){});
var cleanup=null;
function bs(id,v,low){var k="g_"+id,o=null;try{o=localStorage.getItem(k)}catch(x){}o=o==null?null:+o;if(v!=null&&(o==null||(low?v<o:v>o))){o=v;try{localStorage.setItem(k,o)}catch(x){}}return o}
function mk(t,c,h){var d=document.createElement(t);if(c)d.className=c;if(h!=null)d.innerHTML=h;return d}
function rnd(n){return Math.floor(Math.random()*n)}
var GM=[
{id:"mem",i:"🧩",t:"Memory match",d:"Flip cards and find all 8 pairs in the fewest moves.",low:1,u:" moves",f:function(b,A){var E=["🚀","☕","💡","🎯","🧩","🔧","🌍","📈"],c=E.concat(E).sort(function(){return Math.random()-.5}),g=mk("div","mcg"),o=[],mv=0,m=0,lock=0;b.appendChild(g);A.st("Moves: 0");
c.forEach(function(em){var x=mk("button","mc","");x.setAttribute("aria-label","Card");x.onclick=function(){if(lock||x.classList.contains("f")||x.classList.contains("m"))return;x.classList.add("f");x.textContent=em;o.push(x);if(o.length===2){mv++;A.st("Moves: "+mv);lock=1;var a=o[0],z=o[1];o=[];if(a.textContent===z.textContent){a.classList.add("m");z.classList.add("m");m++;lock=0;if(m===8)A.st("Done in "+mv+" moves. Best: "+A.best(mv))}else setTimeout(function(){a.classList.remove("f");z.classList.remove("f");a.textContent="";z.textContent="";lock=0},700)}};g.appendChild(x)})}},
{id:"ttt",i:"⭕",t:"Tic-tac-toe vs the machine",d:"The computer never loses. A draw is a win for you.",u:" pts",f:function(b,A){var s=Array(9).fill(""),r={w:0,d:0,l:0},g=mk("div","tg3"),cells=[],over=0,L=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];b.appendChild(g);A.st("Your move (X). Draw = 1 point, win = 2.");
function win(p){for(var i=0;i<8;i++){var l=L[i];if(p[l[0]]&&p[l[0]]===p[l[1]]&&p[l[1]]===p[l[2]])return p[l[0]]}return p.indexOf("")<0?"d":null}
function mm(p,t){var w=win(p);if(w)return w==="O"?1:w==="X"?-1:0;var v,bst=t==="O"?-9:9;for(var i=0;i<9;i++)if(!p[i]){p[i]=t;v=mm(p,t==="O"?"X":"O");p[i]="";bst=t==="O"?Math.max(bst,v):Math.min(bst,v)}return bst}
function ai(){var bv=-9,bi=-1,v;for(var i=0;i<9;i++)if(!s[i]){s[i]="O";v=mm(s,"X");s[i]="";if(v>bv){bv=v;bi=i}}if(bi>-1)s[bi]="O"}
function draw(){cells.forEach(function(c,i){c.textContent=s[i]})}
function end(w){over=1;if(w==="d")r.d++;else if(w==="X")r.w++;else r.l++;A.best(r.d+r.w*2);A.st((w==="d"?"Draw. ":w==="X"?"You won! ":"I won. ")+"Wins "+r.w+" · Draws "+r.d+" · Losses "+r.l+". Tap a square to go again.")}
for(var k=0;k<9;k++)(function(i){var x=mk("button","tc","");x.setAttribute("aria-label","Square "+(i+1));x.onclick=function(){if(over){s=Array(9).fill("");over=0;draw();A.st("Your move (X)");return}if(s[i])return;s[i]="X";var w=win(s);if(w){draw();end(w);return}ai();draw();w=win(s);if(w)end(w)};cells.push(x);g.appendChild(x)})(k)}},
{id:"rx",i:"⚡",t:"Reaction test",d:"Tap the moment the block turns green.",low:1,u:" ms",f:function(b,A){var bt=mk("button","rxb","Tap to start"),st=0,tm,state=0;b.appendChild(bt);A.st("Wait for green, then tap as fast as you can.");
bt.onclick=function(){if(state===0){state=1;bt.className="rxb wt";bt.textContent="Wait…";tm=setTimeout(function(){state=2;st=performance.now();bt.className="rxb go";bt.textContent="TAP!"},1500+Math.random()*2500)}else if(state===1){clearTimeout(tm);state=0;bt.className="rxb";bt.textContent="Too soon. Tap to retry"}else{var ms=Math.round(performance.now()-st);state=0;bt.className="rxb";bt.textContent=ms+" ms. Tap to retry";A.st("Last: "+ms+" ms · Best: "+A.best(ms)+" ms")}};
return function(){clearTimeout(tm)}}},
{id:"math",i:"➗",t:"Mental math sprint",d:"Solve as many sums as you can in 30 seconds.",u:" solved",f:function(b,A){var sc,t,iv,ans,q=mk("div","big",""),inp=mk("input","gin"),row=mk("div","grow"),again=mk("button","btn","Start");inp.inputMode="numeric";inp.placeholder="Answer, then Enter";inp.setAttribute("aria-label","Answer");inp.disabled=true;row.appendChild(again);b.append(q,inp,row);A.st("30 seconds. Ready?");q.textContent="–";
function nx(){var a=1+rnd(12+sc),c=1+rnd(12),o=rnd(3);if(o===0){q.textContent=a+" + "+c;ans=a+c}else if(o===1){var x=Math.max(a,c),y=Math.min(a,c);q.textContent=x+" − "+y;ans=x-y}else{a=2+rnd(11);q.textContent=a+" × "+c;ans=a*c}}
function start(){sc=0;t=30;again.hidden=true;inp.disabled=false;inp.value="";inp.focus();nx();A.st("Time 30s · Score 0");clearInterval(iv);iv=setInterval(function(){t--;A.st("Time "+t+"s · Score "+sc);if(t<=0){clearInterval(iv);inp.disabled=true;q.textContent="Time! Score "+sc;A.st("Best: "+A.best(sc));again.textContent="Play again";again.hidden=false}},1000)}
again.onclick=start;inp.onkeydown=function(e2){if(e2.key==="Enter"){if(+inp.value===ans){sc++;nx()}inp.value=""}};
return function(){clearInterval(iv)}}},
{id:"sim",i:"🎵",t:"Pattern memory",d:"Watch the lights, then repeat the pattern. It grows each round.",u:" levels",f:function(b,A){var C=["#E8431F","#F5B335","#19A974","#4C6FFF"],g=mk("div","smp"),sq=[],seq=[],pl=0,lv=0,lock=1,tms=[],go=mk("button","btn","Start");b.append(g,go);A.st("Press start.");
function lit(i){sq[i].classList.add("lit");tms.push(setTimeout(function(){sq[i].classList.remove("lit")},350))}
function play(){pl=0;lock=1;var i=0;A.st("Level "+lv+" · watch");(function s(){if(i<seq.length){lit(seq[i]);i++;tms.push(setTimeout(s,600))}else{lock=0;A.st("Level "+lv+" · your turn")}})()}
C.forEach(function(c,i){var x=mk("button","sp","");x.style.background=c;x.setAttribute("aria-label","Pad "+(i+1));x.onclick=function(){if(lock)return;lit(i);if(i!==seq[pl]){lock=1;A.st("Missed at level "+lv+". Best: "+A.best(lv-1)+" levels.");go.textContent="Try again";go.hidden=false;return}pl++;if(pl===seq.length){lv++;seq.push(rnd(4));lock=1;tms.push(setTimeout(play,800))}};sq.push(x);g.appendChild(x)});
go.onclick=function(){seq=[rnd(4)];lv=1;go.hidden=true;play()};
return function(){tms.forEach(clearTimeout)}}},
{id:"seq",i:"🔢",t:"What comes next?",d:"Spot the rule in each number sequence. One wrong answer ends your streak.",u:" streak",f:function(b,A){var streak=0,q=mk("div","big",""),o=mk("div","opt"),ans,tm;b.append(q,o);
function gen(){var t=rnd(5),a=1+rnd(9),d=2+rnd(6),s=[];for(var i=0;i<6;i++){s.push(t===0?a+i*d:t===1?a*Math.pow(2,i):t===2?(i+1)*(i+1)+a:t===3?(i<2?a+i:s[i-1]+s[i-2]):a+i*(i+1)/2*d)}return s}
function nx(){var s=gen();ans=s[5];q.textContent=s.slice(0,5).join(", ")+", ?";var op=[ans],offs=[1,2,3,4,-1,-2,-3,10].sort(function(){return Math.random()-.5});for(var i=0;op.length<4;i++)if(op.indexOf(ans+offs[i])<0)op.push(ans+offs[i]);op.sort(function(){return Math.random()-.5});o.innerHTML="";op.forEach(function(v){var x=mk("button","",String(v));x.onclick=function(){if(v===ans){streak++;A.st("Correct! Streak "+streak);nx()}else{A.st("Not quite, it was "+ans+". Streak "+streak+" · Best "+A.best(streak));streak=0;o.innerHTML="";tm=setTimeout(nx,1600)}};o.appendChild(x)})}
A.st("Streak 0");nx();return function(){clearTimeout(tm)}}},
{id:"rid",i:"💭",t:"Riddle of the day",d:"A new riddle every day. No scores, just thinking.",nb:1,f:function(b,A){var R=DB.R&&DB.R.length?DB.R:[{question:"I am always coming, but I never arrive. What am I?",answer:"tomorrow",hint:"It follows today."}],r=R[Math.floor(Date.now()/864e5)%R.length],ok=String(r.answer).toLowerCase().split("|").map(function(x){return x.trim()}),q=mk("div","big",e(r.question)),inp=mk("input","gin"),row=mk("div","grow"),hb=mk("button","btn","Hint"),rb=mk("button","btn","Reveal answer"),msg=mk("p","gst","");inp.placeholder="Your answer, then Enter";inp.setAttribute("aria-label","Answer");row.append(hb,rb);b.append(q,inp,row,msg);A.st("Today’s riddle");
inp.onkeydown=function(ev){if(ev.key!=="Enter")return;var v=inp.value.trim().toLowerCase();if(ok.indexOf(v)>-1)msg.textContent="Correct! Come back tomorrow for a new one.";else{msg.textContent="Not quite. Try again or ask for a hint.";inp.value=""}};
hb.onclick=function(){msg.textContent=r.hint?"Hint: "+r.hint:"No hint for this one."};rb.onclick=function(){msg.textContent="Answer: "+ok[0]}}}
];
function renderGL(){var gl=$("#gl");gl.innerHTML="";GM.forEach(function(g){var v=g.nb?null:bs(g.id),x=mk("button","gc",'<i>'+g.i+'</i><h3>'+e(g.t)+'</h3><p>'+e(g.d)+'</p><small>'+(g.nb?"New every day":v!=null?"Best: "+v+g.u:"No score yet")+'</small>');x.onclick=function(){openGame(g)};gl.appendChild(x)});rv()}
function openGame(g){if(!g)return;if(cleanup){cleanup();cleanup=null}var p=$("#gp");p.hidden=false;p.innerHTML="";var hd=mk("div","gph","<h2>"+g.i+" "+e(g.t)+"</h2>"),bk=mk("button","fc","← All games"),st=mk("p","gst",""),bd=mk("div","gbd"),A={st:function(t){st.textContent=t},best:function(v){return bs(g.id,v,g.low)}};var sh=mk("button","fc","Share result");sh.onclick=function(){var t="🎮 "+g.t+" · "+st.textContent+" — pramodtidke.in/games/";(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){toast("Result copied. Paste it anywhere.")}).catch(function(){toast(t)})};hd.append(sh,bk);p.append(hd,st,bd);bk.onclick=closeGame;var c=g.f(bd,A);if(typeof c==="function")cleanup=c;$("#gl").hidden=true}
function closeGame(){if(cleanup){cleanup();cleanup=null}$("#gp").hidden=true;$("#gl").hidden=false;renderGL()}
function initGames(){if(!$("#gl"))return;renderGL();var q=new URLSearchParams(location.search).get("g");if(q){var gm=GM.filter(function(g){return g.id===q})[0];if(gm)openGame(gm)}}

function boot(d){DB.d={WR:d.WR,VD:d.VD,PJ:d.PJ,EX:d.EX,PF:d.PF,N:d.N,A:d.A};DB.R=d.R;DB.x=buildIdx();initGames()}
if(window.fetch)fetch(ROOT+"assets/data.json").then(function(r){return r.json()}).then(boot).catch(function(){initGames()});else initGames();
intro();onscroll();rv();
})();
