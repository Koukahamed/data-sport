var FOCUS = {
  pecs:[{muscle:'Pecs / Epaules / Triceps', fx:{name:'Chest press machine',sets:4,reps:'8-12'}, cx:[{name:'Pec fly (papillon)',sets:3,reps:'12-15',m:'Pectoraux'},{name:'Shoulder press',sets:3,reps:'10-12',m:'Epaules'},{name:'Elevations laterales',sets:4,reps:'15',m:'Epaules'},{name:'Triceps pushdown',sets:3,reps:'12-15',m:'Triceps'}]}],
  dos:[{muscle:'Dos / Biceps', fx:{name:'Tirage vertical',sets:4,reps:'8-10'}, cx:[{name:'Row machine',sets:3,reps:'10-12',m:'Dos (épaisseur)'},{name:'Tirage horizontal cable',sets:3,reps:'10-12',m:'Dos (largeur)'},{name:'Curl barre',sets:3,reps:'10-12',m:'Biceps'},{name:'Curl marteau',sets:3,reps:'12-15',m:'Brachial'}]}],
  legs:[{muscle:'Jambes / Mollets', fx:{name:'Leg press',sets:4,reps:'10-12'}, cx:[{name:'Leg curl',sets:3,reps:'12-15',m:'Ischios'},{name:'Leg extension machine',sets:3,reps:'12-15',m:'Quadriceps'},{name:'Mollets debout',sets:4,reps:'15-20',m:'Mollets'}]}],
  cardio:[{muscle:'Cardio / Endurance', fx:null, cx:[{name:'Marche inclinee (tapis)',sets:1,reps:'20-30',m:'LISS',ct:'marche'},{name:'Course intensité modérée', sets:1,reps:'30-45',m:'Endurance',ct:'course'}]}]
};

var WEEK = ['pecs','cardio','dos','rest','legs','cardio','rest'];
var DAYS = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'];
var COL  = {pecs:'#ff5c35',dos:'#00c2ff',legs:'#a855f7',cardio:'#22d3a5',rest:'#222'};
var weekOffset = 0, selectedDay = null, cWork = null, restInt = null, restSec = 0;

function gd(k,d){try{return JSON.parse(localStorage.getItem(k))!=null?JSON.parse(localStorage.getItem(k)):d;}catch(e){return d;}}
function sd(k,v){localStorage.setItem(k,JSON.stringify(v));}
function today(){var d=new Date();return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());}
function pad(n){return String(n).padStart(2,'0');}
function iso(d){return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());}
function fmtDate(s){var d=new Date(s+'T12:00:00');return d.toLocaleDateString('fr-FR',{weekday:'short',day:'numeric',month:'short'});}
function getMonday(d){var dt=new Date(d);var day=dt.getDay();dt.setDate(dt.getDate()+(day===0?-6:1-day));dt.setHours(0,0,0,0);return dt;}
function getWaterTarget(){return gd('wt',8);}

function showScreen(n){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nb').forEach(b=>b.classList.remove('active'));
  document.getElementById('screen-'+n).classList.add('active');
  if(document.getElementById('nav-'+n)) document.getElementById('nav-'+n).classList.add('active');
  if(n==='home')renderHome(); if(n==='poids')renderPoids(); if(n==='history')renderHistory();
}
function goHome(){showScreen('home')}

function changeWeek(dir){ weekOffset += dir; if(weekOffset > 0) weekOffset = 0; renderHome(); }

function renderHome(){
  var mon = getMonday(new Date()); mon.setDate(mon.getDate() + (weekOffset*7));
  document.getElementById('weekLabel').textContent = weekOffset===0?'CETTE SEMAINE':'ARCHIVES';
  var strip=document.getElementById('wstrip'); strip.innerHTML='';
  for(var i=0;i<7;i++){
    var d=new Date(mon); d.setDate(mon.getDate()+i); var isoD=iso(d); var type=WEEK[i];
    var c=document.createElement('div'); c.className='dchip'+(isoD===(selectedDay||today())?' today':'');
    c.innerHTML=`<div class="dlbl">${DAYS[i]}</div><div class="dnum">${d.getDate()}</div><div class="dtag" style="background:${COL[type]}">${type.toUpperCase()}</div>`;
    (function(dayIso){c.onclick=function(){selectedDay=dayIso;renderHome();};})(isoD);
    strip.appendChild(c);
  }
  var weights=gd('weights',[]); document.getElementById('hw').textContent=weights.length?weights[weights.length-1].val.toFixed(1):'-';
  if(!selectedDay) selectedDay=today(); var tidx=(new Date(selectedDay+'T12:00:00').getDay()+6)%7;
  var ttype=WEEK[tidx]; var card=document.getElementById('todayCard');
  if(ttype==='rest'){ card.innerHTML='<div class="fcard rest"><div class="ftitle">Jour de repos</div></div>'; return; }
  var slot=FOCUS[ttype][0];
  var allExHTML = (slot.fx ? [{name:slot.fx.name, sets:slot.fx.sets, reps:slot.fx.reps}] : []).concat(slot.cx).map(ex => 
    `<div class="citem"><div class="ciname">${ex.name}</div><div class="cimeta">${ex.sets}x${ex.reps}</div></div>`).join('');
  card.innerHTML=`<div class="fcard ${ttype}"><div class="ftop"><span class="fbadge" style="background:${COL[ttype]}">${ttype.toUpperCase()}</span></div><div class="ftitle">${ttype.toUpperCase()} DAY</div><div class="clist">${allExHTML}</div><button class="abtn a${ttype}" onclick="startWorkout('${ttype}')">Commencer la seance</button></div>`;
}

function startWorkout(type){
  var rot=FOCUS[type]; var slot=rot[0]; cWork={type, start:Date.now(), slot};
  var color=COL[type]; document.getElementById('wkbg').textContent=type.toUpperCase();
  document.getElementById('wkbg').style.background=color; document.getElementById('wktit').textContent=type.toUpperCase()+' DAY';
  var list=document.getElementById('exlist'); list.innerHTML='';
  var allEx=slot.fx?[slot.fx].concat(slot.cx):slot.cx;
  allEx.forEach((ex, ei)=>{
    var isCI=(ex.ct==='marche'||ex.ct==='course'); var cols4='22px 1fr 1fr 70px';
    var tbl=''; if(isCI){
      var cols=ex.ct==='marche'?'22px 1fr 1fr 1fr 70px':'22px 1fr 1fr 70px';
      var col2=ex.ct==='marche'?'Inclin.(%)':'Vitesse(km/h)';
      tbl=`<div class="sethdr" style="grid-template-columns:${cols}"><span>#</span><span>Durée(min)</span><span>${col2}</span>${ex.ct==='marche'?'<span>Vitesse</span>':''}<span>ok</span></div>
      <div id="crow-${ei}"><div class="setrow" id="sr-${ei}-0" style="grid-template-columns:${cols}">
      <div class="setnr">1</div><input class="sinp" id="r-${ei}-0" type="number" placeholder="20"><input class="sinp" id="w-${ei}-0" type="text" placeholder="10" inputmode="decimal">
      ${ex.ct==='marche'?'<input class="sinp" id="v-'+ei+'-0" type="text" placeholder="5" inputmode="decimal">':''}
      <div style="display:flex;gap:4px"><button class="schk" id="chk-${ei}-0" onclick="checkSet(${ei},0,'${type}')">ok</button><button class="schk" onclick="copyToNext(${ei},0)">↳</button></div></div></div><button class="addbtn" onclick="addCrow(${ei},'${ex.ct}')">+ Ligne</button>`;
    } else {
      var gc=ex.bw?'22px 1fr 32px':cols4; var rows=''; for(var s=0;s<ex.sets;s++){
        rows+=`<div class="setrow" id="sr-${ei}-${s}" style="grid-template-columns:${gc}"><div class="setnr">${s+1}</div><input class="sinp" id="r-${ei}-${s}" type="number" placeholder="10"><input class="sinp" id="w-${ei}-${s}" type="text" placeholder="0" inputmode="decimal">
        <div style="display:flex;gap:4px"><button class="schk" id="chk-${ei}-${s}" onclick="checkSet(${ei},${s},'${type}')">ok</button><button class="schk" onclick="copyToNext(${ei},${s})">↳</button></div></div>`;
      }
      tbl=`<div class="sethdr" style="grid-template-columns:${gc}"><span>#</span><span>Reps</span><span>Poids</span><span>ok</span></div>${rows}<button class="addbtn" onclick="addSet(${ei})">+ Serie</button>`;
    }
    var isFocus=(ei===0&&slot.fx); var cardClass=isFocus?'fexcard '+type:'excard';
    list.innerHTML+=`<div class="${cardClass}" id="card-${ei}">${isFocus?`<div class="fexlbl ${type}">FOCUS - ${slot.muscle.toUpperCase()}</div>`:''}<div class="exhdr" onclick="toggleEx(${ei})"><div class="exname">${ex.name}</div><svg class="exchev" id="chev-${ei}" viewBox="0 0 24 24" fill="none" stroke="currentColor" width="18"><polyline points="6 9 12 15 18 9"/></svg></div><div class="settbl" id="sets-${ei}">${tbl}</div></div>`;
  });
  toggleEx(0); updateVol(); showScreen('workout');
}

function toggleEx(i){ var el=document.getElementById('sets-'+i); var chev=document.getElementById('chev-'+i); if(!el||!chev)return; var o=el.classList.contains('open'); el.classList.toggle('open',!o); chev.classList.toggle('open',!o); }
function addSet(ei){ var tbl=document.getElementById('sets-'+ei); var s=tbl.querySelectorAll('.setrow').length; var row=document.createElement('div'); row.className='setrow'; row.id='sr-'+ei+'-'+s; row.style.gridTemplateColumns='22px 1fr 1fr 70px'; row.innerHTML=`<div class="setnr">${s+1}</div><input class="sinp" id="r-${ei}-${s}" type="number"><input class="sinp" id="w-${ei}-${s}" type="text" inputmode="decimal"><div style="display:flex;gap:4px"><button class="schk" id="chk-${ei}-${s}" onclick="checkSet(${ei},${s})">ok</button><button class="schk" onclick="copyToNext(${ei},${s})">↳</button></div>`; tbl.querySelector('.addbtn').before(row); }
function addCrow(ei,ct){ var c=document.getElementById('crow-'+ei); var s=c.querySelectorAll('.setrow').length; var cols=ct==='marche'?'22px 1fr 1fr 1fr 70px':'22px 1fr 1fr 70px'; var row=document.createElement('div'); row.className='setrow'; row.id='sr-'+ei+'-'+s; row.style.gridTemplateColumns=cols; row.innerHTML=`<div class="setnr">${s+1}</div><input class="sinp" id="r-${ei}-${s}" type="number"><input class="sinp" id="w-${ei}-${s}" type="text" inputmode="decimal">${ct==='marche'?`<input class="sinp" id="v-${ei}-${s}" type="text" inputmode="decimal">`:''}<div style="display:flex;gap:4px"><button class="schk" id="chk-${ei}-${s}" onclick="checkSet(${ei},${s})">ok</button><button class="schk" onclick="copyToNext(${ei},${s})">↳</button></div>`; c.appendChild(row); }
function copyToNext(ei, si){ var next=si+1; if(!document.getElementById('r-'+ei+'-'+next)){ if(document.getElementById('crow-'+ei)) addCrow(ei, cWork.slot.cx[ei]?.ct||'marche'); else addSet(ei); } var r=document.getElementById('r-'+ei+'-'+si)?.value||'', w=document.getElementById('w-'+ei+'-'+si)?.value||'', v=document.getElementById('v-'+ei+'-'+si)?.value||''; if(document.getElementById('r-'+ei+'-'+next)) document.getElementById('r-'+ei+'-'+next).value=r; if(document.getElementById('w-'+ei+'-'+next)) document.getElementById('w-'+ei+'-'+next).value=w; if(document.getElementById('v-'+ei+'-'+next)) document.getElementById('v-'+ei+'-'+next).value=v; updateVol(); }
function checkSet(ei,si,type){ var btn=document.getElementById('chk-'+ei+'-'+si); var was=btn.classList.contains('on'); btn.classList.toggle('on'); if(!was){startRest(90);updateVol();} }
function updateVol(){ var vol=0; document.querySelectorAll('.setrow').forEach(row=>{ if(row.querySelector('.schk').classList.contains('on')){ var inps=row.querySelectorAll('input'); vol+=(parseInt(inps[0].value)||0)*(parseFloat(inps[1]?.value.replace(',','.'))||0); } }); document.getElementById('voltk').style.display='block'; document.getElementById('volrows').innerHTML=`<div class="volrow"><b>TOTAL</b><div class="volv">${Math.round(vol)}kg</div></div>`; }
function startRest(s){ clearInterval(restInt); restSec=s; var el=document.getElementById('restov'),cnt=document.getElementById('restcnt'); el.classList.add('on'); cnt.textContent=s; restInt=setInterval(()=>{ restSec--; cnt.textContent=restSec; if(restSec<=0)skipRest(); },1000); }
function skipRest(){ clearInterval(restInt); document.getElementById('restov').classList.remove('on'); }
function finishWorkout(){ if(!cWork)return; var vol=0; document.querySelectorAll('.setrow').forEach(row=>{ if(row.querySelector('.schk').classList.contains('on')){ var inps=row.querySelectorAll('input'); vol+=(parseInt(inps[0].value)||0)*(parseFloat(inps[1]?.value.replace(',','.'))||0); } }); var sessions=gd('sessions',[]); sessions.push({date:today(),type:cWork.type,vol:vol,duration:Math.round((Date.now()-cWork.start)/60000)}); sd('sessions',sessions); goHome(); }
function saveWeight(){ var raw=document.getElementById('winp').value.replace(',','.'); var v=parseFloat(raw); if(!v||v<30||v>250)return; var w=gd('weights',[]); w.push({date:today(),val:v}); sd('weights',w); document.getElementById('winp').value=''; renderPoids(); }
function renderPoids(){ var w=gd('weights',[]); document.getElementById('wdisp').textContent=w.length?w[w.length-1].val.toFixed(1):'-'; var ctx=document.getElementById('wchart').getContext('2d'); if(window.wChart) window.wChart.destroy(); if(w.length) window.wChart=new Chart(ctx,{type:'line',data:{labels:w.slice(-10).map(i=>i.date.slice(5)),datasets:[{data:w.slice(-10).map(i=>i.val),borderColor:'#fff',tension:.4}]},options:{plugins:{legend:{display:false}},scales:{all:{display:false}}}}); }
function renderHistory(){ var s=gd('sessions',[]); document.getElementById('hlist').innerHTML=s.slice().reverse().map(i=>`<div class="hitem"><b>${fmtDate(i.date)}</b> - ${i.type.toUpperCase()}<br><small>${i.vol}kg déplacés</small></div>`).join(''); }
function exportData(){ var data={sessions:gd('sessions',[]),weights:gd('weights',[]),wt:gd('wt',8)}; var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'}); var url=URL.createObjectURL(blob); var a=document.createElement('a'); a.href=url; a.download='hkfocus-backup.json'; a.click(); }
function importData(event){ var file=event.target.files[0]; if(!file)return; var reader=new FileReader(); reader.onload=function(e){ try{ var data=JSON.parse(e.target.result); if(data.sessions)sd('sessions',data.sessions); if(data.weights)sd('weights',data.weights); renderHome(); }catch(e){alert('Erreur import');} }; reader.readAsText(file); }
function resetAll(){if(confirm('Tout effacer ?')){localStorage.clear();location.reload();}}
function renderSettings(){ document.getElementById('swat').value=getWaterTarget(); }
function saveSettings(){ sd('wt',parseInt(document.getElementById('swat').value)||8); }

renderHome();
