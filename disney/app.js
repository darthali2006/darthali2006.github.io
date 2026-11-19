const BY={};
CATS.forEach(c=>{BY[c.id]=c;c.items=c.q.map((x,i)=>({key:c.id+":"+i,cat:c.id,n:i+1,r:x[0],q:x[1],a:x[2]}))});
const ALL=CATS.flatMap(c=>c.items);
const KEY={};ALL.forEach(x=>KEY[x.key]=x);
const app=document.getElementById("app");

function load(k,d){try{const v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function save(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
let known=load("dct_known",null);
if(!known){known={};const old=load("dvt_known",{});Object.keys(old).forEach(id=>{known["villains:"+id]=old[id]});save("dct_known",known)}

const state={
  route:{cat:null,mode:"home"},
  study:{cat:null},fc:{cat:null},games:{},
  players:load("dct_players",load("dvt_players",["Player 1","Player 2"]))
};

const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const shuffle=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
function hl(text,term){const t=esc(text);if(!term)return t;const safe=esc(term).replace(/[.*+?^${}()|[\]\\]/g,"\\$&");return t.replace(new RegExp("("+safe+")","ig"),"<mark>$1</mark>")}
const knownIn=c=>c.items.filter(x=>known[x.key]==="k").length;

function parseHash(){
  const h=(location.hash||"").slice(1);
  if(!h||h==="home")return{cat:null,mode:"home"};
  if(h==="mixed-game")return{cat:null,mode:"game"};
  const m=h.match(/^([a-z]+)(?:-(flashcards|game))?$/);
  if(m&&BY[m[1]])return{cat:m[1],mode:m[2]||"study"};
  return{cat:null,mode:"home"};
}
function go(hash){if(location.hash.slice(1)!==hash){try{location.hash=hash}catch(e){}}state.route=parseHash();render();window.scrollTo({top:0})}
window.addEventListener("hashchange",()=>{state.route=parseHash();render();window.scrollTo({top:0})});

/* ---------- Home ---------- */
function homeHTML(){
  const total=ALL.length,k=ALL.filter(x=>known[x.key]==="k").length;
  let h=`<header class="wrap hero">
    <p class="eyebrow">Trivia prep for the high seas</p>
    <h1 class="display">Disney <em>Cruise</em> Trivia</h1>
    <p class="lede">${CATS.length} categories and ${total} questions, with the answers. Study them, drill them as flashcards, then run a scored game night with the family.</p>
    <div class="stats"><div><b>${total}</b><span>Questions</span></div><div><b>${CATS.length}</b><span>Categories</span></div><div><b>${k}</b><span>You know</span></div></div>
    <div class="cta-row"><a class="btn primary" href="#mixed-game">Start a mixed game night</a><a class="btn" href="#cruise">Study the ship first</a></div>
  </header>
  <section class="wrap" aria-label="Categories"><div class="grid">`;
  CATS.forEach(c=>{
    const kc=knownIn(c),pct=c.items.length?Math.round(kc/c.items.length*100):0;
    h+=`<a class="tile" data-cat="${c.id}" href="#${c.id}"><span class="count">${c.items.length} questions</span><span class="name">${esc(c.name)}</span><span class="tg">${esc(c.tag)}</span><span class="prog" aria-hidden="true"><i style="width:${pct}%"></i></span><span class="known">${kc} known</span></a>`;
  });
  h+=`</div>
  <div class="tips"><h2 class="display">How trivia works on board</h2><ul>
    <li><b>Expect a mix.</b> Sessions in the lounges jump between Disney films, parks, music, Walt history and ship facts, so use the mixed game to practice switching.</li>
    <li><b>Know your ship.</b> Some questions are about the ship you’re on and the ports you visit. The Disney Cruise Line category covers the Destiny and the Magic in detail.</li>
    <li><b>The card is final.</b> Cast members read questions that come as a set, so go with the stated answer instead of arguing.</li>
    <li><b>Bring a team.</b> Family sessions are often multiple choice, and close games end in a tie-breaker.</li>
  </ul></div></section>`;
  return h;
}

/* ---------- Category shell ---------- */
const MODES=[["study","Study"],["flashcards","Flashcards"],["game","Game Night"]];
function render(){
  const r=state.route;
  document.body.setAttribute("data-cat",r.cat||"home");
  if(r.mode==="home"){app.innerHTML=homeHTML();document.title="Disney Cruise Trivia";return}
  const c=r.cat?BY[r.cat]:null;
  if(c&&state.study.cat!==c.id)state.study={cat:c.id,round:-1,search:"",showAll:false,open:{}};
  if(c&&state.fc.cat!==c.id)state.fc={cat:c.id,round:-1,onlyAgain:false,shuffled:false,order:null,i:0,flipped:false};
  let h=`<header class="wrap cat-head"><a class="back" href="#home">← All categories</a>
    <p class="eyebrow">${c?`${c.items.length} questions · ${c.rounds.length} rounds`:`${ALL.length} questions · every category`}</p>
    <h1 class="display">${c?esc(c.name):"Mixed Game Night"}</h1>
    <p class="tag">${c?esc(c.tag):"Questions from every category, shuffled together the way onboard trivia mixes them."}</p></header>`;
  if(c){h+=`<nav class="tabs" aria-label="Mode"><div class="wrap" role="tablist">${MODES.map(([m,l])=>`<a class="tab" role="tab" href="#${c.id}${m==="study"?"":"-"+m}" aria-selected="${r.mode===m}">${l}</a>`).join("")}</div></nav>`}
  h+=`<main id="view" class="wrap"></main>`;
  app.innerHTML=h;
  document.title=(c?c.name:"Mixed Game Night")+" · Disney Cruise Trivia";
  renderView();
}
function renderView(){
  const v=document.getElementById("view");if(!v)return;
  const r=state.route;
  if(r.mode==="study")v.innerHTML=studyHTML();
  else if(r.mode==="flashcards")v.innerHTML=flashHTML();
  else v.innerHTML=gameHTML();
}
function roundChips(c,selected,attr){
  let h=`<div class="chips" role="group" aria-label="Rounds"><button class="chip" data-${attr}="-1" aria-pressed="${selected===-1}">All rounds</button>`;
  c.rounds.forEach((r,i)=>{h+=`<button class="chip" data-${attr}="${i}" aria-pressed="${selected===i}">${i+1} · ${esc(r.n)}</button>`});
  return h+"</div>";
}

/* ---------- Study ---------- */
function studyHTML(){
  const c=BY[state.route.cat],s=state.study,term=s.search.trim().toLowerCase();
  let h=`<div class="toolbar">${roundChips(c,s.round,"sround")}
    <div class="row"><input type="search" id="study-search" placeholder="Search" value="${esc(s.search)}" aria-label="Search questions or answers"><button class="btn" id="toggle-all">${s.showAll?"Hide answers":"Show all answers"}</button></div></div>`;
  let any=false;
  c.rounds.forEach((r,ri)=>{
    if(s.round!==-1&&s.round!==ri)return;
    const items=c.items.filter(x=>x.r===ri&&(!term||x.q.toLowerCase().includes(term)||x.a.toLowerCase().includes(term)));
    if(!items.length)return;any=true;
    h+=`<section class="round"><h2 class="display">${esc(r.n)}</h2><span class="sub"><b>Round ${ri+1}</b> · ${esc(r.s)}</span><ol class="list">`;
    items.forEach(x=>{
      const open=s.showAll||s.open[x.key]||(term&&x.a.toLowerCase().includes(term));
      h+=`<li class="qa${open?" open":""}"><button class="qbtn" data-qa="${x.key}" aria-expanded="${!!open}"><span class="num">${x.n}</span><span class="qtext">${hl(x.q,term)}</span><span class="hint">Tap to reveal</span></button><div class="ans">${hl(x.a,term)}</div></li>`;
    });
    h+="</ol></section>";
  });
  if(!any)h+=`<p class="empty">No questions match “${esc(s.search)}”. Try a character, a film or a ship.</p>`;
  return h;
}

/* ---------- Flashcards ---------- */
function fcDeck(){
  const c=BY[state.route.cat],f=state.fc;
  let ids=c.items.filter(x=>(f.round===-1||x.r===f.round)&&(!f.onlyAgain||known[x.key]==="a")).map(x=>x.key);
  if(f.shuffled)ids=shuffle(ids);
  f.order=ids;if(f.i>=ids.length)f.i=0;f.flipped=false;
}
function flashHTML(){
  const c=BY[state.route.cat],f=state.fc;if(!f.order)fcDeck();
  const deck=f.order,len=deck.length,scope=c.items.filter(x=>f.round===-1||x.r===f.round);
  const kc=scope.filter(x=>known[x.key]==="k").length,ac=scope.filter(x=>known[x.key]==="a").length;
  let h=`<div class="toolbar">${roundChips(c,f.round,"fround")}
    <label class="check" for="only-again"><input type="checkbox" id="only-again" ${f.onlyAgain?"checked":""}> Only cards marked “study again” (${ac})</label></div>`;
  if(!len)return h+`<p class="empty">${f.onlyAgain?"Nothing left to study again here. Nice work.":"No cards here."}</p>`;
  const x=KEY[deck[f.i]],st=known[x.key];
  h+=`<div class="fc-top"><span class="label">Card ${f.i+1} of ${len}</span><span class="muted" style="font-size:14px;font-weight:700">${kc} of ${scope.length} known</span></div>
  <div class="bar" aria-hidden="true"><i style="width:${((f.i+1)/len*100).toFixed(1)}%"></i></div>
  <div class="flip"><div class="card${f.flipped?" flipped":""}" id="card" tabindex="0" role="button" aria-label="Flip card">
    <div class="face" aria-hidden="${f.flipped}"><div class="row" style="justify-content:space-between"><span class="meta">Round ${x.r+1} · ${esc(c.rounds[x.r].n)} · #${x.n}</span>${st?`<span class="pill ${st}">${st==="k"?"Known":"Study again"}</span>`:""}</div>
      <p>${esc(x.q)}</p><span class="tap">Tap the card or press space to flip</span></div>
    <div class="face back-face" aria-hidden="${!f.flipped}"><span class="meta">Answer to #${x.n}</span><p>${esc(x.a)}</p><span class="tap">Did you know it?</span></div>
  </div></div>
  <div class="fc-actions"><button class="btn" id="mark-again" ${f.flipped?"":"disabled"}>Study again</button><button class="btn good" id="mark-known" ${f.flipped?"":"disabled"}>Got it</button></div>
  <div class="fc-nav"><button class="btn ghost" id="fc-prev" ${f.i===0?"disabled":""}>← Back</button><button class="btn ghost" id="fc-shuffle">${f.shuffled?"In order":"Shuffle"}</button><button class="btn ghost" id="fc-next">${f.i===len-1?"Start over":"Skip →"}</button></div>
  <div class="row" style="margin-top:16px"><button class="btn ghost small" id="fc-reset">Clear progress in this category</button></div>`;
  return h;
}
function fcAdvance(){const f=state.fc;f.flipped=false;f.i=f.i+1>=f.order.length?0:f.i+1}
function fcMark(v){
  const f=state.fc,id=f.order[f.i];known[id]=v;save("dct_known",known);
  if(f.onlyAgain&&v==="k"){f.order.splice(f.i,1);if(f.i>=f.order.length)f.i=0;f.flipped=false}else fcAdvance();
  renderView();
}

/* ---------- Game Night ---------- */
function gameCtx(){return state.route.cat||"mixed"}
function game(){
  const ctx=gameCtx();
  if(!state.games[ctx])state.games[ctx]={phase:"setup",cats:state.route.cat?[state.route.cat]:CATS.map(c=>c.id),length:"20",shuffle:true,deck:[],results:[],i:0,shown:false};
  return state.games[ctx];
}
function scores(g){return state.players.map((_,p)=>g.results.filter(r=>r&&r.includes(p)).length)}
function gameHTML(){
  const g=game(),P=state.players;
  if(g.phase==="setup"){
    const pool=ALL.filter(x=>g.cats.includes(x.cat)).length;
    let h=`<div class="panel"><h3>Who’s playing?</h3><div class="players">`;
    P.forEach((p,i)=>{h+=`<div class="player-row"><input type="text" id="player-${i}" data-player="${i}" value="${esc(p)}" maxlength="20" aria-label="Player ${i+1} name">${P.length>1?`<button class="icon-btn" data-remove="${i}" aria-label="Remove ${esc(p)}">×</button>`:""}</div>`});
    h+=`</div>${P.length<8?`<div><button class="btn" id="add-player">+ Add player</button></div>`:""}</div>
    <div class="panel"><h3>Which categories?</h3><div class="chips wrapit">`;
    CATS.forEach(c=>{h+=`<button class="chip" data-gcat="${c.id}" aria-pressed="${g.cats.includes(c.id)}">${esc(c.name)}</button>`});
    h+=`</div><div class="row"><button class="btn ghost small" id="all-cats">Select all</button><button class="btn ghost small" id="no-cats">Clear</button><span class="muted" style="font-size:14px;font-weight:700">${pool} questions available</span></div></div>
    <div class="panel"><h3>How long?</h3><div class="row">
      <select id="game-length" aria-label="Number of questions">${["10","20","30","50","all"].map(v=>`<option value="${v}" ${g.length===v?"selected":""}>${v==="all"?"Every question ("+pool+")":v+" questions"}</option>`).join("")}</select>
      <label class="check" for="game-shuffle"><input type="checkbox" id="game-shuffle" ${g.shuffle?"checked":""}> Shuffle</label></div></div>
    <button class="btn primary wide" id="start-game" ${pool?"":"disabled"}>Start game</button>
    <p class="muted" style="font-size:14px">One person reads each question aloud, reveals the answer, then taps everyone who got it right.</p>`;
    return h;
  }
  const sc=scores(g),top=Math.max(...sc);
  const strip=`<div class="score-strip">${P.map((p,i)=>`<div class="score${top>0&&sc[i]===top?" lead":""}"><span>${esc(p)}</span><b>${sc[i]}</b></div>`).join("")}</div>`;
  if(g.phase==="done"){
    const ranked=P.map((p,i)=>({p,s:sc[i]})).sort((a,b)=>b.s-a.s),win=ranked.filter(r=>r.s===ranked[0].s);
    const title=ranked[0].s===0?"Nobody scored. The villains win this one.":win.length>1?`It’s a tie: ${win.map(w=>esc(w.p)).join(" & ")}`:`${esc(win[0].p)} takes the crown`;
    return `<div class="panel"><span class="label">Final standings · ${g.deck.length} questions</span><p class="display crown">${title}</p>
      <ol class="standings">${ranked.map(r=>`<li><span>${esc(r.p)}</span><span class="pts">${r.s} / ${g.deck.length}</span></li>`).join("")}</ol></div>
      <div class="row"><button class="btn primary" id="play-again">Play again</button><button class="btn" id="to-setup">Change setup</button></div>`;
  }
  const x=KEY[g.deck[g.i]],c=BY[x.cat],got=g.results[g.i]||[];
  let h=strip+`<div class="fc-top"><span class="label">Question ${g.i+1} of ${g.deck.length}</span><span class="pill cat" data-cat="${c.id}">${esc(c.name)}</span></div>
  <div class="bar" aria-hidden="true"><i style="width:${((g.i+1)/g.deck.length*100).toFixed(1)}%"></i></div>
  <div class="qcard"><span class="muted" style="font-size:13px;font-weight:700">Round ${x.r+1} · ${esc(c.rounds[x.r].n)}</span><p class="q">${esc(x.q)}</p>${g.shown?`<p class="a">${esc(x.a)}</p>`:""}</div>`;
  if(!g.shown)h+=`<button class="btn primary wide" id="reveal">Reveal answer</button>`;
  else h+=`<div class="panel"><span class="label">Who got it right?</span><div class="who">${P.map((p,i)=>`<button class="chip" data-got="${i}" aria-pressed="${got.includes(i)}">${esc(p)}</button>`).join("")}</div></div>
    <button class="btn primary wide" id="next-q">${g.i===g.deck.length-1?"See final scores":"Next question"}</button>`;
  h+=`<div class="row" style="margin-top:14px;justify-content:space-between"><button class="btn ghost small" id="prev-q" ${g.i===0?"disabled":""}>← Previous</button><button class="btn ghost small" id="end-game">End game</button></div>`;
  return h;
}
function startGame(){
  const g=game();
  let ids=ALL.filter(x=>g.cats.includes(x.cat)).map(x=>x.key);
  if(g.shuffle)ids=shuffle(ids);
  if(g.length!=="all")ids=ids.slice(0,parseInt(g.length,10));
  g.deck=ids;g.results=ids.map(()=>[]);g.i=0;g.shown=false;g.phase="play";
  save("dct_players",state.players);renderView();window.scrollTo({top:0});
}

/* ---------- Events ---------- */
app.addEventListener("click",e=>{
  const b=e.target.closest("button,#card");if(!b)return;
  const s=state.study,f=state.fc,d=b.dataset;
  if(d.sround!==undefined){s.round=+d.sround;renderView();return}
  if(b.id==="toggle-all"){s.showAll=!s.showAll;if(!s.showAll)s.open={};renderView();return}
  if(d.qa!==undefined){
    const k=d.qa,isOpen=b.closest(".qa").classList.contains("open");
    if(isOpen&&s.showAll){s.showAll=false;BY[s.cat].items.forEach(x=>s.open[x.key]=true)}
    s.open[k]=!isOpen;renderView();return}
  if(d.fround!==undefined){f.round=+d.fround;f.i=0;fcDeck();renderView();return}
  if(b.id==="card"){f.flipped=!f.flipped;renderView();return}
  if(b.id==="mark-known"){fcMark("k");return}
  if(b.id==="mark-again"){fcMark("a");return}
  if(b.id==="fc-next"){fcAdvance();renderView();return}
  if(b.id==="fc-prev"){f.i=Math.max(0,f.i-1);f.flipped=false;renderView();return}
  if(b.id==="fc-shuffle"){f.shuffled=!f.shuffled;f.i=0;fcDeck();renderView();return}
  if(b.id==="fc-reset"){BY[f.cat].items.forEach(x=>delete known[x.key]);save("dct_known",known);fcDeck();renderView();return}
  const P=state.players;
  if(b.id==="add-player"){P.push("Player "+(P.length+1));save("dct_players",P);renderView();const el=document.getElementById("player-"+(P.length-1));if(el){el.focus();el.select()}return}
  if(d.remove!==undefined){P.splice(+d.remove,1);save("dct_players",P);Object.values(state.games).forEach(g=>{if(g.phase==="setup")g.results=[]});renderView();return}
  const g=state.route.mode==="game"?game():null;if(!g)return;
  if(d.gcat!==undefined){const k=g.cats.indexOf(d.gcat);k>=0?g.cats.splice(k,1):g.cats.push(d.gcat);renderView();return}
  if(b.id==="all-cats"){g.cats=CATS.map(c=>c.id);renderView();return}
  if(b.id==="no-cats"){g.cats=[];renderView();return}
  if(b.id==="start-game"||b.id==="play-again"){startGame();return}
  if(b.id==="reveal"){g.shown=true;renderView();return}
  if(d.got!==undefined){const p=+d.got,r=g.results[g.i],k=r.indexOf(p);k>=0?r.splice(k,1):r.push(p);renderView();return}
  if(b.id==="next-q"){if(g.i===g.deck.length-1)g.phase="done";else{g.i++;g.shown=false}renderView();window.scrollTo({top:0});return}
  if(b.id==="prev-q"){g.i=Math.max(0,g.i-1);g.shown=true;renderView();return}
  if(b.id==="end-game"){g.phase="done";renderView();return}
  if(b.id==="to-setup"){g.phase="setup";renderView();return}
});
app.addEventListener("input",e=>{
  const t=e.target;
  if(t.id==="study-search"){state.study.search=t.value;const pos=t.selectionStart;renderView();const el=document.getElementById("study-search");if(el){el.focus();try{el.setSelectionRange(pos,pos)}catch(_){}}}
  if(t.dataset.player!==undefined){state.players[+t.dataset.player]=t.value;save("dct_players",state.players)}
});
app.addEventListener("change",e=>{
  const t=e.target;
  if(t.id==="only-again"){state.fc.onlyAgain=t.checked;state.fc.i=0;fcDeck();renderView()}
  if(t.id==="game-length"){game().length=t.value}
  if(t.id==="game-shuffle"){game().shuffle=t.checked}
  if(t.dataset.player!==undefined&&!t.value.trim()){const i=+t.dataset.player;state.players[i]="Player "+(i+1);save("dct_players",state.players);renderView()}
});
document.addEventListener("keydown",e=>{
  if(state.route.mode!=="flashcards"||/INPUT|SELECT|TEXTAREA/.test((document.activeElement||{}).tagName||""))return;
  const f=state.fc;if(!f.order||!f.order.length)return;
  if(e.key===" "||e.key==="Enter"){e.preventDefault();f.flipped=!f.flipped;renderView();const c=document.getElementById("card");c&&c.focus()}
  else if(e.key==="ArrowRight"){fcAdvance();renderView()}
  else if(e.key==="ArrowLeft"){f.i=Math.max(0,f.i-1);f.flipped=false;renderView()}
});

/* ---------- Boot ---------- */
function start(data){
  if(data&&data.games){state.study=data.study||state.study;state.fc=data.fc||state.fc;state.games=data.games||{}}
  state.route=parseHash();render();
}
start({});
