"""Build a single-file, fully offline HTML replay of the generated War of 56."""
import json,html
from pathlib import Path
p=Path(__file__).resolve().parents[1] / 'output'
p.mkdir(parents=True, exist_ok=True)
data=json.loads((p/'war56_v3_results.json').read_text())
# Quote JSON into a non-executed application/json script.
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
htmlcode=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>THE WAR OF 56 · Interactive Campaign Atlas</title>
<style>
:root{color-scheme:dark;--bg:#09121e;--card:#101f30;--border:#2a3c4b;--muted:#9daebd;--amber:#f4ce77;--bright:#edf5fb;--cyan:#73ced9}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(160deg,#132536 0%,#08121f 52%,#0a1421 100%);color:var(--bright);font-family:Inter,Segoe UI,system-ui,-apple-system,sans-serif;font-size:14px}
header{padding:22px max(18px,calc((100vw - 1620px)/2));border-bottom:1px solid #284151;background:#0d1a29}
h1{font-family:Georgia,serif;font-size:clamp(24px,3.2vw,40px);letter-spacing:2px;margin:2px 0;color:var(--amber)}
header p{color:var(--muted);margin:6px 0 0;max-width:900px;line-height:1.6}.eyebrow{text-transform:uppercase;color:#7ed2d9;font-size:11px;letter-spacing:2px;font-weight:800}
.layout{max-width:1620px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) 355px;gap:16px;padding:17px} .left,.right{min-width:0}.right{display:flex;flex-direction:column;gap:15px}
.panel{background:rgba(17,32,47,.94);border:1px solid #304558;border-radius:12px;box-shadow:0 7px 26px rgba(0,0,0,.18)}
.panel-title{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;gap:12px;font-weight:750;letter-spacing:.2px}.panel-title small{font-weight:400;color:var(--muted)}
.topbar{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:0 0 14px}.metric{padding:13px 12px;background:var(--card);border:1px solid var(--border);border-radius:10px}.metric b{font-size:25px;display:block;font-variant-numeric:tabular-nums;color:#f8ecc9}.metric span{font-size:11px;color:var(--muted)}
.map-actions{padding:12px 14px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}.map-actions label{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:6px}.mapframe{position:relative;background:#102f43;margin:0 10px 8px;border:1px solid #264153;border-radius:8px;overflow:hidden}canvas{width:100%;height:auto;display:block;cursor:crosshair;image-rendering:pixelated}.tooltip{position:absolute;pointer-events:none;z-index:5;background:#07111ded;color:white;padding:9px 11px;border:1px solid #88a6b1;max-width:260px;font-size:12px;line-height:1.5;border-radius:6px;box-shadow:0 5px 20px #0008;display:none}.legend{font-size:11px;color:var(--muted);display:flex;flex-wrap:wrap;gap:15px;padding:0 15px 12px}.legend span{display:inline-flex;align-items:center;gap:6px}.circle{display:inline-block;border:2px solid #ffda83;border-radius:50%;height:11px;width:11px}
.toolbar{padding:14px 16px}.timeline{display:flex;align-items:center;gap:9px}.timeline input{width:100%;accent-color:var(--amber);cursor:pointer}button,select,input[type=search]{border:1px solid #496072;background:#172d42;color:var(--bright);border-radius:6px;font:inherit;padding:7px 9px}button:hover{background:#2a475d;cursor:pointer}button:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid var(--amber);outline-offset:2px}button.primary{background:#bd9344;color:#08121a;border-color:#dbbc76;font-weight:750}.turnbadge{min-width:85px;text-align:center;color:var(--amber);font-weight:800;font-variant-numeric:tabular-nums;font-size:18px}.milestones{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px} .milestones button{font-size:11px;padding:4px 7px}.small{font-size:12px;color:var(--muted)}
.progress{height:7px;background:#243e4b;overflow:hidden;border-radius:6px;margin:5px 0 0}.progress div{height:100%;background:linear-gradient(90deg,#418c9e,#f2ca73)}
.select-row{display:flex;align-items:center;gap:8px;margin:10px 12px}.select-row select{flex:1;min-width:0}
#nation-card{padding:12px 16px}.nation-name{font-family:Georgia,serif;font-size:20px;line-height:1.2;margin:6px 0} .nation-tag{display:inline-block;border-radius:4px;font-size:11px;font-weight:700;padding:3px 6px;background:#233b4d}
.statgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin:15px 0}.stat{padding:9px 12px;background:#152b3b;border-radius:7px}.stat b{display:block;font-size:18px;font-variant-numeric:tabular-nums}.stat label{font-size:11px;color:var(--muted)}
.threat{margin:14px 0 5px;font-size:12px;color:#c1d7e4}.threat strong{float:right;color:#f4cf7e}
.event-list{padding:8px 8px 12px;max-height:480px;overflow:auto}.event{padding:9px 10px;margin:4px 0;background:#132a3b;border-left:3px solid #648fa9;border-radius:4px;line-height:1.43;font-size:12px}.event.important{border-left-color:#eac36c}.event .time{font-weight:800;color:var(--amber);margin-right:9px}.event .type{color:#a0bac9;text-transform:uppercase;font-size:10px;letter-spacing:.7px}.event p{margin:5px 0 0}.event:hover{background:#1b3850;cursor:pointer}
.ranking{margin-top:15px}.tablewrap{overflow:auto;max-height:410px}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th{background:#162d3f;color:#a9bece;position:sticky;top:0;text-align:left;font-weight:700;font-size:11px}td,th{border-bottom:1px solid #294154;padding:9px 11px;white-space:nowrap}td{font-size:12px}tr:hover td{background:#17344a}tr.highlight td{background:#36402f}.dot{display:inline-block;border-radius:4px;height:9px;width:9px;margin-right:6px}.ranking-controls{display:flex;gap:6px;align-items:center;flex-wrap:wrap;padding:10px 14px}.ranking-controls input{flex:1;min-width:140px}.ranking-controls select{max-width:175px}
#replay-footer{max-width:1620px;margin:0 auto;padding:10px 22px 30px;color:#9daebd;font-size:12px;line-height:1.7}.muted{color:var(--muted)} .winner-label{font-size:11px;font-weight:800;letter-spacing:1px;color:var(--amber)} .status{color:#a4e6c7} #summary{line-height:1.5;padding:10px 16px;color:#c9e0e8}
@media(max-width:1150px){.layout{grid-template-columns:1fr}.right{display:grid;grid-template-columns:1fr 1fr}.topbar{grid-template-columns:repeat(3,minmax(0,1fr))}.rank-panel{grid-column:1/-1}}
@media(max-width:700px){.layout{padding:10px}.right{display:flex}.topbar{grid-template-columns:repeat(2,minmax(0,1fr))}.metric b{font-size:21px}.panel-title{flex-wrap:wrap}.turnbadge{min-width:70px}.timeline{gap:4px}button{padding:6px}.map-actions{gap:10px}}
</style></head>
<body>
<header><div class="eyebrow">SolusGo · Civilization V · fan simulation · Seed __SEED__</div><h1>THE WAR OF 56</h1><div style="font-size:18px;color:#f1e3c7">Balanced Mega-Simulation 3.0 &nbsp;·&nbsp; Interactive Campaign Replay</div><p>56 modeled factions · 11 City-States · every turn calculated · the political map saved at configurable checkpoints. Select a civilization, inspect battles, watch capitals change hands and follow victory threats. Not an actual Civ V engine run.</p></header>
<div class="layout">
 <div class="left">
  <div class="topbar">
   <div class="metric"><b id="metric-turn">0</b><span>Current turn</span></div>
   <div class="metric"><b id="metric-remaining">56</b><span>Surviving civilizations</span></div>
   <div class="metric"><b id="metric-war">0</b><span>Active wars</span></div>
   <div class="metric"><b id="metric-city">56</b><span>Cities founded</span></div>
   <div class="metric"><b id="metric-caps">0</b><span>Founding capitals conquered</span></div>
  </div>
  <section class="panel">
   <div class="panel-title"><span id="map-heading">POLITICAL MAP</span><small id="era-label">Ancient Era</small></div>
   <div class="map-actions"><label><input type="checkbox" id="toggle-borders" checked> Borders</label><label><input type="checkbox" id="toggle-cities" checked> City markers</label><label><input type="checkbox" id="toggle-fronts" checked> War fronts</label><label><input type="checkbox" id="toggle-labels"> Capital numbers</label><button id="reset-select">Show all civs</button></div>
   <div class="mapframe"><canvas id="world" width="1116" height="576" aria-label="Political map of the simulated world"></canvas><div class="tooltip" id="tooltip"></div></div>
   <div class="legend"><span><i class="circle"></i> Founding capital</span><span>● Secondary city</span><span style="color:#f5d37f">★ City-State</span><span style="color:#fd786b">➞ Active war front</span><span>Colors = territorial controller</span><span>Gray = unclaimed land</span></div>
  </section>
  <section class="panel" style="margin-top:14px">
   <div class="panel-title"><span>TURN-BY-TURN CAMPAIGN TIMELINE</span><small id="checkpoint-count"></small></div>
   <div class="toolbar"><div class="timeline"><button id="start" title="First map">|◀</button><button id="prev" title="Previous map">◀</button><button class="primary" id="play">▶ Play</button><button id="next" title="Next map">▶</button><button id="end" title="Final map">▶|</button><input id="timeline" aria-label="Map checkpoint" type="range" min="0" max="0" step="1" value="0"><div class="turnbadge" id="turn-badge">T0000</div></div>
   <div class="milestones"><button data-jump="0">Founding</button><button data-jump="150">Early wars</button><button data-jump="300">Expansion</button><button data-jump="500">Rivalries</button><button data-jump="700">World powers</button><button data-jump="850">Victory race</button><button id="jump-first-capital">First capital fall</button><button id="jump-cultural">Cultural hold</button></div>
   <div class="small" style="margin-top:12px">Checkpoint <span id="checkpoint-label"></span>. Events are resolved each turn; select a checkpoint to see the recorded changes since the previous map.</div></div>
  </section>
  <section class="panel ranking" id="ranking-panel"><div class="panel-title">CIVILIZATION SCOREBOARD <small>Click a row to inspect</small></div><div class="ranking-controls"><select id="ranking-sort"><option value="score">Overall score</option><option value="army">Military strength</option><option value="tech">Research</option><option value="tourism">Tourism</option><option value="cultural_progress">Cultural influence</option><option value="delegates">Congress delegates</option><option value="city_count">Cities</option><option value="capital_count">Founding capitals</option></select><input type="search" id="ranking-filter" placeholder="Find civilization…"><label class="small"><input type="checkbox" id="show-all"> Show all 56</label></div><div class="tablewrap"><table><thead><tr><th>#</th><th>Civilization</th><th>Score</th><th>Cities</th><th>Capitals</th><th>Army</th><th>Science</th></tr></thead><tbody id="ranking-body"></tbody></table></div></section>
 </div>
 <aside class="right">
  <section class="panel"><div class="panel-title">CIVILIZATION INSPECTOR <small>Click the map or choose below</small></div><div class="select-row"><select id="nation-select" aria-label="Select civilization"></select></div><div id="nation-card"></div></section>
  <section class="panel"><div class="panel-title">CAMPAIGN EVENTS <small id="events-span"></small></div><div style="padding:8px 12px"><label class="small"><input type="checkbox" id="events-major"> Major events only</label></div><div id="event-list" class="event-list"></div></section>
  <section class="panel"><div class="panel-title">CAMPAIGN RESULT</div><div id="summary"></div></section>
 </aside>
</div>
<footer id="replay-footer">The political map is a schematic projection of modeled city-control radii, not actual Civ V tiles. Army strength, research, city development, culture, City-State influence and combat are abstracted and do not execute any CP v151 or individual civilization Lua scripts. The nine pre-existing standalone roster entries are carried over from our earlier War of 54 inventory. File is self-contained and works offline.</footer>
<script type="application/json" id="campaign-data">__PAYLOAD__</script>
<script>
(()=>{'use strict';
const data=JSON.parse(document.getElementById('campaign-data').textContent);
const roster=data.roster, snaps=data.snapshots, cities=data.cities, events=data.events, n=roster.length, scale=data.world.map_scale;
const worldW=data.world.width,worldH=data.world.height, pixel=12, canvas=document.getElementById('world'),ctx=canvas.getContext('2d'), tip=document.getElementById('tooltip');
let k=0,selected=-1,playing=false,interval=null;
const $=id=>document.getElementById(id);
const land=Uint8Array.from(atob(data.world.land),c=>c.charCodeAt(0));
const territories=snaps.map(s=>Uint8Array.from(atob(s.territory),c=>c.charCodeAt(0)));
const byid=new Map(cities.map(c=>[c.id,c]));
const cityElements=(s)=>s.city_ids.map((id,i)=>({...byid.get(id),currentOwner:s.city_owners[i]}));
const color=data.colors;
const fmt=(a)=>Math.round(a).toLocaleString();
const thumb=(s)=>`${s.turn.toString().padStart(4,'0')} · ${s.era}`;
function setSelected(i){selected=i;$('nation-select').value=String(i);render()}
function setFrame(i){k=Math.max(0,Math.min(snaps.length-1,i));$('timeline').value=k;render()}
function jumpTurn(t){let idx=snaps.reduce((best,s,i)=>Math.abs(s.turn-t)<Math.abs(snaps[best].turn-t)?i:best,0);setFrame(idx)}
function plot(){
 let s=snaps[k],a=territories[k],showBorders=$('toggle-borders').checked;
 ctx.fillStyle='#102f43';ctx.fillRect(0,0,canvas.width,canvas.height);
 // Paint cells; unclaimed land stays pale and empty water stays deep blue.
 for(let y=0;y<worldH;y++)for(let x=0;x<worldW;x++){
  const index=y*worldW+x, civ=a[index];
  if(!land[index])continue;
  ctx.fillStyle=civ===255?'#b9c4ae':color[civ];
  ctx.globalAlpha=(selected>=0 && civ!==255 && civ!==selected)?0.29:1;
  ctx.fillRect(x*pixel,y*pixel,pixel+0.2,pixel+0.2);
 }
 ctx.globalAlpha=1;
 if(showBorders){ctx.strokeStyle='rgba(8,20,29,.64)';ctx.lineWidth=1.1;ctx.beginPath();
  for(let y=0;y<worldH;y++)for(let x=0;x<worldW;x++){
   const i=y*worldW+x,v=a[i];if(v===255)continue;
   if(x+1<worldW&&v!==a[i+1]){ctx.moveTo((x+1)*pixel,y*pixel);ctx.lineTo((x+1)*pixel,(y+1)*pixel)}
   if(y+1<worldH&&v!==a[i+worldW]){ctx.moveTo(x*pixel,(y+1)*pixel);ctx.lineTo((x+1)*pixel,(y+1)*pixel)}
  }ctx.stroke();}
 const loc=cityElements(s);
 // Active war fronts: line connecting the two nearest cities in each active conflict.
 if($('toggle-fronts').checked){
  for(const w of s.wars){let best=null;for(const a of loc){if(a.currentOwner!==w.a)continue;
    for(const b of loc){if(b.currentOwner!==w.b)continue;let dist=(a.x-b.x)**2+(a.y-b.y)**2;if(!best||dist<best.dist)best={a,b,dist};}}
   if(!best)continue;
   const x1=best.a.x*pixel/scale,y1=best.a.y*pixel/scale,x2=best.b.x*pixel/scale,y2=best.b.y*pixel/scale;
   if(selected>=0&&selected!==w.a&&selected!==w.b)continue;
   ctx.strokeStyle='#ff6357';ctx.lineWidth=2.4;ctx.globalAlpha=.87;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
   const ang=Math.atan2(y2-y1,x2-x1);ctx.fillStyle='#ff6357';ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-10*Math.cos(ang-.5),y2-10*Math.sin(ang-.5));ctx.lineTo(x2-10*Math.cos(ang+.5),y2-10*Math.sin(ang+.5));ctx.fill();
   ctx.globalAlpha=1;
  }
 }
 if($('toggle-cities').checked){
  for(const c of loc){let x=c.x*pixel/scale,y=c.y*pixel/scale;
   ctx.globalAlpha=(selected>=0 && selected!==c.currentOwner)?0.40:1;
   ctx.beginPath();ctx.arc(x,y,c.capital?5.4:2.2,0,2*Math.PI);
   ctx.fillStyle=color[c.currentOwner];ctx.fill();ctx.lineWidth=c.capital?2.1:.65;ctx.strokeStyle=c.capital?'#ffe7a4':'#092333';ctx.stroke();
   if($('toggle-labels').checked&&c.capital){ctx.font='bold 11px ui-sans-serif,system-ui';ctx.lineWidth=3;ctx.strokeStyle='#071521';ctx.fillStyle='#fff';ctx.strokeText(c.founder+1,x+6,y-8);ctx.fillText(c.founder+1,x+6,y-8)}
  }ctx.globalAlpha=1;
 }
 for(let i=0;i<data.world.city_states.length;i++){
  const [tx,ty]=data.world.city_states[i],x=tx*pixel/scale,y=ty*pixel/scale;
  ctx.fillStyle='#ffe8a2';ctx.strokeStyle='#243748';ctx.lineWidth=1;
  ctx.beginPath();for(let v=0;v<10;v++){let a=v*Math.PI/5-Math.PI/2,r=v%2?3.5:7.5;let px=x+Math.cos(a)*r,py=y+Math.sin(a)*r;if(!v)ctx.moveTo(px,py);else ctx.lineTo(px,py)}ctx.closePath();ctx.fill();ctx.stroke();
 }
}
function inspector(){const s=snaps[k],id=selected;
 if(id<0){$('nation-card').innerHTML='<div class="small">Select a civilization on the map or in the scoreboard to follow it throughout the campaign. Capitals with golden outlines change color when conquered. You can also toggle the war arrows.</div>';return;}
 const c=roster[id],st=s.statistics[id];
 const div=document.createElement('div');const nam=document.createElement('h2');nam.className='nation-name';nam.textContent=c.name;
 const em=document.createElement('span');em.className='dot';em.style.background=color[id];nam.prepend(em);
 div.innerHTML=`<span class="nation-tag">${c.collection} · ${c.preferred} specialist</span>`;div.appendChild(nam);
 const status=document.createElement('div');status.innerHTML=st.alive?'<span class="status">● Surviving</span>':'<span style="color:#f5a6a2">● Eliminated</span>';
 div.appendChild(status);
 let stats=[['Score',st.score],['Cities',st.city_count],['Capitals',st.capital_count],['Army',fmt(st.army)],['Research',st.tech.toFixed(1)+'/110'],['Influential',st.inf_count],['Delegates',st.delegates],['City-State allies',st.alliances]];
 const grid=document.createElement('div');grid.className='statgrid';for(const [label,value]of stats){let node=document.createElement('div');node.className='stat';let b=document.createElement('b');b.textContent=value;let l=document.createElement('label');l.textContent=label;node.appendChild(b);node.appendChild(l);grid.appendChild(node)}div.appendChild(grid);
 let prog=st.threat*100;const threat=document.createElement('div');threat.className='threat';threat.innerHTML=`Highest modeled victory progress <strong>${prog.toFixed(0)}%</strong><div class="progress"><div style="width:${Math.max(0,Math.min(100,prog))}%"></div></div>`;div.appendChild(threat);
 if(c.name==='The Triumphal Imperium'){let x=document.createElement('p');x.className='small';x.textContent=`Victory Momentum: ${st.momentum}/6 (schematic model)`;div.appendChild(x)}
 if(c.name==='The Lantern Fleet'){let x=document.createElement('p');x.className='small';x.textContent=`Guarded harbors: ${st.guarded_harbors} (schematic fleet budget)`;div.appendChild(x)}
 if(c.name==='The Republic of First Drafts'){let x=document.createElement('p');x.className='small';x.textContent=`First-possessed building classes: ${st.classes_known}`;div.appendChild(x)}
 if(c.name==='T1 — The ZOFGK Dynasty'){let x=document.createElement('p');x.className='small';x.textContent=`Upgrade development: ${st.veteran}/7 · surviving roster: ${st.roster_alive}/5`;div.appendChild(x)}
 if(data.winner&&data.winner.id===id){let x=document.createElement('p');x.className='winner-label';x.textContent=`🏆 SIMULATED ${data.winner.method.toUpperCase()} WINNER · T${data.winner.turn}`;div.appendChild(x)}
 $('nation-card').replaceChildren(div);
}
function scoreboard(){let s=snaps[k],query=$('ranking-filter').value.toLowerCase(),sort=$('ranking-sort').value;
 const ordered=roster.map((_,i)=>i).filter(i=>roster[i].name.toLowerCase().includes(query));
 ordered.sort((a,b)=>(s.statistics[b][sort]-s.statistics[a][sort])||a-b);
 const view=$('show-all').checked?ordered:ordered.slice(0,16);
 $('ranking-body').replaceChildren(...view.map((i,idx)=>{let c=roster[i],st=s.statistics[i],tr=document.createElement('tr');if(i===selected)tr.classList.add('highlight');let cells=[idx+1,c.name,st.score,st.city_count,st.capital_count,fmt(st.army),st.tech.toFixed(1)];for(let j=0;j<cells.length;j++){let td=document.createElement('td');td.textContent=cells[j];if(j===1){let dot=document.createElement('span');dot.className='dot';dot.style.background=color[i];td.prepend(dot);if(!st.alive){let xx=document.createElement('span');xx.textContent=' †';xx.style.color='#e7a9a9';td.appendChild(xx)}}tr.appendChild(td)}tr.onclick=()=>setSelected(i);return tr;}));
}
function eventLog(){const curr=snaps[k].turn,prev=k?snaps[k-1].turn:0;
 $('events-span').textContent=`Turns ${prev}–${curr}`;
 const major=$('events-major').checked;
 const period=events.filter(e=>e.turn>=(k===0?0:prev+1)&&e.turn<=curr&&(!major||e.importance>=3));
 const list=$('event-list');list.replaceChildren();if(!period.length){let el=document.createElement('p');el.className='small';el.style.padding='15px';el.textContent='No matching events in this checkpoint.';list.appendChild(el);return}
 const sorted=period.slice().sort((a,b)=>b.turn-a.turn||b.importance-a.importance);
 sorted.slice(0,60).forEach(e=>{let div=document.createElement('div');div.className='event'+(e.importance>=3?' important':'');
 const first=document.createElement('div');const t=document.createElement('span');t.className='time';t.textContent='T'+e.turn;const typ=document.createElement('span');typ.className='type';typ.textContent=e.kind;first.append(t,typ);
 const p=document.createElement('p');p.textContent=e.text;div.append(first,p);div.onclick=()=>{if(e.ids?.length)setSelected(e.ids[0]);};list.appendChild(div)});
 if(sorted.length>60){let tail=document.createElement('p');tail.className='small';tail.textContent=`... and ${sorted.length-60} more recorded events in this checkpoint (available in JSON).`;list.appendChild(tail)}
}
function render(){const s=snaps[k],last=snaps[snaps.length-1];
 $('metric-turn').textContent=s.turn;$('metric-remaining').textContent=s.statistics.filter(x=>x.alive).length;
 $('metric-war').textContent=s.wars.length;$('metric-city').textContent=s.city_ids.length;
 $('metric-caps').textContent=s.city_ids.filter((cid,j)=>cid<56&&s.city_owners[j]!==cid).length;
 $('map-heading').textContent=`POLITICAL MAP · ${s.turn===last.turn?'FINAL STATE':'WORLD TURN '+s.turn}`;
 $('era-label').textContent=s.era+' Era';$('turn-badge').textContent='T'+s.turn.toString().padStart(4,'0');
 $('checkpoint-label').textContent=`${k+1} of ${snaps.length}`;$('checkpoint-count').textContent=`${snaps.length} snapshots`;
 plot();inspector();scoreboard();eventLog();
 $('summary').innerHTML=data.winner?`<span class="winner-label">THE CAMPAIGN'S RESULT</span><h3 style="margin:9px 0;color:#f3d185">${data.winner.name}</h3><div>${data.winner.method} victory · Turn ${data.winner.turn}</div><div class="small" style="margin-top:11px">The winner need not lead the standard score ranking. The map and event log represent the full decisive sequence that caused this outcome.</div>`:`<span class="winner-label">NO WINNER YET</span><p>Stopped at Turn ${data.endturn}; increase max turns to continue.</p>`;
}
$('nation-select').innerHTML='<option value="-1">All 56 civilizations</option>'+roster.map((r,i)=>`<option value="${i}">${i+1}. ${r.name.replaceAll('&','&amp;')}</option>`).join('');
$('nation-select').onchange=e=>setSelected(+e.target.value);
$('reset-select').onclick=()=>setSelected(-1);
$('timeline').max=snaps.length-1;$('timeline').oninput=e=>setFrame(+e.target.value);
$('start').onclick=()=>setFrame(0);$('end').onclick=()=>setFrame(snaps.length-1);
$('prev').onclick=()=>setFrame(k-1);$('next').onclick=()=>setFrame(k+1);
$('play').onclick=()=>{playing=!playing;$('play').textContent=playing?'Ⅱ Pause':'▶ Play';if(interval)clearInterval(interval);if(playing){if(k===snaps.length-1)setFrame(0);interval=setInterval(()=>{if(k>=snaps.length-1){playing=false;$('play').textContent='▶ Play';clearInterval(interval)}else setFrame(k+1)},850)}};
for(let id of ['toggle-borders','toggle-cities','toggle-fronts','toggle-labels'])$(id).onchange=render;
$('events-major').onchange=eventLog;$('ranking-sort').onchange=scoreboard;
$('ranking-filter').oninput=scoreboard;$('show-all').onchange=scoreboard;
for(const b of document.querySelectorAll('[data-jump]'))b.onclick=()=>jumpTurn(+b.dataset.jump);
const firstCap=events.find(e=>e.kind==='capital');$('jump-first-capital').onclick=()=>jumpTurn(firstCap?.turn||0);
const victoryHold=events.find(e=>e.kind==='victory'&&e.text.includes('begins'));$('jump-cultural').onclick=()=>jumpTurn(victoryHold?.turn||data.endturn);
canvas.onmousemove=e=>{const rect=canvas.getBoundingClientRect();let gx=(e.clientX-rect.left)/rect.width*worldW,gy=(e.clientY-rect.top)/rect.height*worldH;
 const x=Math.floor(gx),y=Math.floor(gy);if(x<0||x>=worldW||y<0||y>=worldH){tip.style.display='none';return}const civ=territories[k][y*worldW+x];
 const mousePX=gx*scale,mousePY=gy*scale,close=cityElements(snaps[k]).filter(q=>Math.hypot(q.x-mousePX,q.y-mousePY)<4).sort((a,b)=>Math.hypot(a.x-mousePX,a.y-mousePY)-Math.hypot(b.x-mousePX,b.y-mousePY))[0];
 const cs=data.world.city_states.findIndex(pt=>Math.hypot(pt[0]-mousePX,pt[1]-mousePY)<3);
 let label=close?`${close.name} · controlled by ${roster[close.currentOwner].name}`:cs>=0?`City-State ${cs+1}`:civ===255?land[y*worldW+x]?'Unclaimed territory':'Open sea':roster[civ].name;
 tip.textContent=label;tip.style.display='block';tip.style.left=Math.min(rect.width-220,e.clientX-rect.left+12)+'px';tip.style.top=Math.max(0,e.clientY-rect.top-45)+'px';};
canvas.onmouseleave=()=>tip.style.display='none';
canvas.onclick=e=>{const box=canvas.getBoundingClientRect();const xx=Math.floor((e.clientX-box.left)/box.width*worldW),yy=Math.floor((e.clientY-box.top)/box.height*worldH);let civ=territories[k][yy*worldW+xx];if(civ!==255)setSelected(civ)};
window.onkeydown=e=>{if(['INPUT','SELECT','TEXTAREA'].includes(document.activeElement.tagName))return;if(e.key==='ArrowRight')setFrame(k+1);if(e.key==='ArrowLeft')setFrame(k-1)};
render();setFrame(snaps.length-1);
})();</script>
</body></html>'''
htmlcode=htmlcode.replace('__PAYLOAD__',payload).replace('__SEED__',str(data['seed']))
(p/'war56_v3_interactive_replay.html').write_text(htmlcode,encoding='utf-8')
print('HTML created:',(p/'war56_v3_interactive_replay.html').stat().st_size,'bytes')