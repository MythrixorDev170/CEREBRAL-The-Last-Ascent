const fs=require('fs'),vm=require('vm'),path=require('path');
const THREE=require('./pass0/node_modules/three/build/three.js');
const stub=()=>new Proxy(function(){},{get(t,p){if(p===Symbol.toPrimitive)return()=>0;if(p==='then')return undefined;if(p===Symbol.iterator)return function*(){};return stub()},set(){return true},apply(){return stub()},construct(){return stub()}});
const extract=h=>[...h.matchAll(/<script>([\s\S]*?)<\/script>/g)].pop()[1];
const SRC=extract(fs.readFileSync('cerebral.html','utf8'));
function makeSpeech(opts={}){
  opts=Object.assign({mode:'ok'},opts);
  const log=[];
  const syn={ _cur:null, _mode:opts.mode, speak(u){ log.push('speak:'+u.text.slice(0,24)); this._cur=u; if(opts.mode==='never') return; if(opts.mode==='error'){ setTimeout(()=>{ try{u.onerror&&u.onerror(new Error('mock'))}catch(e){} },1); return; } if(opts.mode==='ok'){ setTimeout(()=>{ try{u.onend&&u.onend()}catch(e){} },5); } }, cancel(){ log.push('cancel'); this._cur=null; } };
  syn.log=log;
  const klass=function(t){ this.text=t; this.onend=null; this.onerror=null; this.onstart=null; this.pitch=0; this.rate=0; this.volume=0; };
  return {syn, klass, log};
}
function loadWithSpeech(SRC, speech){
  const els={},store=new Map(),hand={},q=[],txEl={},created=[],appended=[],errors=[];
  let txLog=[];
  const txStyle=new Proxy({},{set(t,p,v){ txLog.push('tx.style.'+p+'='+v); txEl['style.'+p]=v; return true}, get(t,p){ return txEl['style.'+p]; }});
  let txHTML='';
  const txProxy=new Proxy(function(){},{get(t,p){
    if(p==='style') return txStyle;
    if(p==='innerHTML') return txHTML;
    if(p==='classList') return { remove(c){ txLog.push('classList.remove '+c)}, add(c){ txLog.push('classList.add '+c)} };
    if(p==='offsetWidth') return 0;
    if(p===Symbol.toPrimitive) return ()=>0;
    if(p==='then') return undefined;
    return stub();
  }, set(t,p,v){
    if(p==='innerHTML'){ txHTML=v; txLog.push('tx.innerHTML='+String(v).slice(0,80)); return true; }
    return true;
  }});
  const hudLog={};
  const recEl=id=>{ if(id==='tx') return txProxy; const sty=new Proxy({},{set(t_,p,v){hudLog[id+'.style.'+p]=v;return true},get(){return stub()}}); return new Proxy(function(){},{get(t_,p){if(p==='style')return sty;if(p===Symbol.toPrimitive)return()=>0;if(p==='then')return undefined;return stub()},set(t_,p,v){hudLog[id+'.'+p]=v;return true},apply(){return stub()}})};
  els['tx']=txProxy;
  let nextId=1;
  const pendingTimeouts=[];
  const fakeSetTimeout=(fn,ms)=>{ const id=nextId++; pendingTimeouts.push({id,fn,ms}); setTimeout(()=>{ const idx=pendingTimeouts.findIndex(x=>x.id===id); if(idx>=0) pendingTimeouts.splice(idx,1); try{fn()}catch(e){ console.error('fakeTimeout fn error',e)} }, ms); return id; };
  const fakeClearTimeout=(id)=>{ const idx=pendingTimeouts.findIndex(x=>x.id===id); if(idx>=0) pendingTimeouts.splice(idx,1); };
  const doc={
    getElementById:id=>els[id]||(els[id]=recEl(id)),
    createElement:t=>{ if(t==='pre'){const e={style:{},tag:t};created.push(e);return e}return stub(); },
    body:{appendChild:e=>appended.push(e)},
    documentElement:{style:{setProperty(){}}},
    currentScript:{textContent:SRC},
    addEventListener(){}, fullscreenElement:null
  };
  const T3=Object.assign({},THREE,{WebGLRenderer:class{constructor(){this.info={render:{calls:0,triangles:0},memory:{geometries:0,textures:0}};this.shadowMap={enabled:false}}setPixelRatio(){}setSize(){}render(){}}});
  const ctx={
    THREE:T3, document:doc, location:{search:''},
    localStorage:{getItem:k=>store.has(k)?store.get(k):null,setItem:(k,v)=>store.set(k,String(v)),removeItem:k=>store.delete(k)},
    navigator:{}, innerWidth:1280, innerHeight:720, devicePixelRatio:1,
    matchMedia:()=>({matches:false}),
    requestAnimationFrame:f=>{q.push(f); return q.length},
    performance:{now:()=>0},
    setTimeout:fakeSetTimeout, clearTimeout:fakeClearTimeout,
    console:{log(){},warn() {}, error(...a){ console.error('VM console.error',...a) }},
    addEventListener:(t,f)=>{(hand[t]=hand[t]||[]).push(f)},
    speechSynthesis: speech.syn,
    SpeechSynthesisUtterance: speech.klass
  };
  ctx.window=ctx; vm.createContext(ctx);
  vm.runInContext('Math.random=(function(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}})(1)',ctx);
  try{
    vm.runInContext(SRC, ctx, {filename:'game.js'});
    console.log('load ok');
    return {ctx, run:c=>vm.runInContext(c,ctx), txLog, speech, pendingTimeouts, doc, els};
  }catch(e){
    console.error('LOAD FAILED', e.stack);
    console.error('msg', e.message);
    throw e;
  }
}
const speech=makeSpeech({mode:'never'});
try{
  const L=loadWithSpeech(SRC, speech);
  console.log('created');
  L.run(`cfg.gp.subs=true; cfg.gp.voice=false;`);
  console.log('set cfg ok');
  L.run(`CER_DIALOGUE.clear('play'); go('play');`);
  console.log('clear/go ok');
  L.run(`say('alpha'); say('bravo'); say('charlie');`);
  console.log('say ok', L.run(`JSON.stringify(CER_DIALOGUE.queue.map(x=>x.text))`), L.run(`CER_DIALOGUE.cur?CER_DIALOGUE.cur.text:''`));
}catch(e){
  console.error('RUN FAILED', e.stack);
}