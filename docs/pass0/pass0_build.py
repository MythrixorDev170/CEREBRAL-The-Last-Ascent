# PASS 0 build: applies infrastructure-only edits to the pre-Pass-0 source. Re-runnable (always starts from the baseline copy).
import re,json,collections,hashlib
import os,sys,subprocess,tempfile
P0=os.path.dirname(os.path.abspath(__file__));OUT=os.path.dirname(P0)
src=open(P0+'/baseline_cerebral_pre_pass0.html').read()
i=src.index('<script>\n"use strict";');head=src[:i]+'<script>\n';rest=src[i+len('<script>\n'):];j=rest.index('</script>');js=rest[:j];tail=rest[j:]
js0=js
def sub(a,b,n=1):
    global js
    c=js.count(a)
    if c!=n: raise SystemExit('MISMATCH (%d != %d): %s'%(c,n,a[:80]))
    js=js.replace(a,b)
# ---------- baseline facts (captured BEFORE changes) ----------
lines0=js0.split('\n')
def analyze(text,names):
    f=tempfile.NamedTemporaryFile('w',suffix='.js',delete=False);f.write(text);f.close()
    try: return json.loads(subprocess.check_output(['node',P0+'/deadcode.js',f.name]+names))
    finally: os.unlink(f.name)
A0=analyze(js0,['ghost','jump','warn2'])  # executable references only (AST based: comments/strings ignored)
assert len(A0['warn2']['declared'])==1 and len(A0['warn2']['refs'])>=1,'warn2 expected to be LIVE: '+json.dumps(A0['warn2'])
facts={'colors_0x_distinct':len(set(re.findall(r'0x[0-9a-fA-F]{6}\b',js0))),'colors_0x_uses':len(re.findall(r'0x[0-9a-fA-F]{6}\b',js0)),
 'dead_code_executable_refs':A0,
 'save_format_baseline':re.search(r"function save\(i\)\{.*\}",js0).group(0),'sha256_baseline_script':hashlib.sha256(js0.encode()).hexdigest()}
# ---------- 7. dead code: ghost() and jump() (warn2 has a live call site and is KEPT) ----------
for n in ['ghost','jump']:
    if len(A0[n]['declared'])!=1 or A0[n]['refs']: raise SystemExit(n+' is not dead: '+json.dumps(A0[n]))
    js,k=re.subn(r'^function '+n+r'\(\)\{.*$\n','',js,flags=re.M)
    if k!=1: raise SystemExit('could not remove '+n)
A1=analyze(js,['ghost','jump','warn2'])
for n in ['ghost','jump']: assert not A1[n]['declared'] and not A1[n]['refs'],(n,A1[n])
assert A1['warn2']==A0['warn2'] or len(A1['warn2']['refs'])==len(A0['warn2']['refs'])
facts['dead_code_after']=A1
# ---------- 3. PAL ----------
PALN={'66f8ff':'laser','d070ff':'plasma','02030a':'space','ffffff':'white','8a94a0':'scrapMetal','ff2a2a':'alertRed','ff5a3a':'enemyShot','ffb060':'sparkWarm','ff8844':'hullHit','66e8ff':'genHit','6f8cff':'skyAmb','ff4a3a':'atmoRed','33ffee':'beacon','1a3a6a':'solarPanel','081a3a':'solarGlow','ffaa55':'flameOrange','88ddff':'shieldPale','66ccff':'shieldBlue','55ccff':'engineBlue','33ff66':'navGreen','ff3344':'navRed','663300':'nodeDim','ff3a2a':'cerebralRed','ffaa33':'amberLight','3fb0ff':'droneBlue','ffaa22':'missileAmber','ffaa44':'explosion','ffcc66':'sparkGold'}
for h,n in PALN.items():
    c0=len(re.findall(r'\b0x'+h+r'\b',js0,flags=re.I))
    if c0<2: raise SystemExit('PAL color not repeated: '+h)
    js=re.sub(r'\b0x'+h+r'\b','PAL.'+n,js,flags=re.I)
PALS={"'#f43'":'radarEnemy',"'#4ff'":'radarStation',"'#fd3'":'radarDerelict',"'#5f8'":'radarRefuge',"'#2a7a8a'":'radarRing',"'#fff'":'radarWhite'}
for q,n in PALS.items(): sub(q,'PAL.'+n,js.count(q))
sub('background:#4fb8ff"',"background:'+PAL.hudShield+'\"");sub('background:#e5484d"',"background:'+PAL.hudHull+'\"")
palvals={n:'0x'+h for h,n in PALN.items()};palvals.update({'radarEnemy':"'#f43'",'radarStation':"'#4ff'",'radarDerelict':"'#fd3'",'radarRefuge':"'#5f8'",'radarRing':"'#2a7a8a'",'radarWhite':"'#fff'",'hudShield':"'#4fb8ff'",'hudHull':"'#e5484d'"})
PALJS='const PAL=Object.freeze({'+','.join(k+':'+v for k,v in palvals.items())+'});'
# ---------- 2. TUNE (name,value,group,original expression) ----------
TS=[('mouseZone','.28','steering','mouse steering zone radius = .28*min(w,h)'),('yawRate','2.2','steering','-crv(mx)*2.2*cfg.sens'),('pitchRate','1.8','steering','-crv(my)*1.8*cfg.sens'),
('dead','.07','steering curve','(abs(x)-.07)/.93 dead zone'),('deadSpan','.93','steering curve','(abs(x)-.07)/.93 span'),('crvLin','.3','steering curve','.3*t+.7*t*t'),('crvQuad','.7','steering curve','.3*t+.7*t*t'),
('touchStick','55','touch','left stick radius px'),('touchDead','.15','touch','stick dead zone'),('touchAim','80','touch','right aim radius px'),
('bankRoll','.35','visual bank','yaw*.35'),('bankPitch','.1','visual bank','pit*.1'),('bankRate','6','visual bank','exp(-6*dt)'),
('enMax','100','energy','cl(P.en...,0,100)'),('enMin','1','energy','P.en<=1 / P.en>1'),('enResume','30','energy','P.en>30'),('energyRegen','14','energy','regen 14/s'),('boostDrain','26','energy','boost drain -26/s'),('bfRate','4','boost','min(1,dt*4)'),
('accel','60','thrust','acc=60*...'),('thrStep','.1','thrust','1+.1*up.thr'),('boostAccel','1.4','boost','1+1.4*bo'),('sprintAccel','1.2','thrust','K.sp?1.2:1'),
('maxSpeed','90','velocity','mxv=90*...'),('spdStep','.1','velocity','1+.1*up.spd'),('warpStep','.15','velocity','1+.15*up.wp'),('sprintMax','1.15','velocity','K.sp?1.15:1'),
('boostThrust','.5','boost','bo*acc*.5'),('strafe','.6','thrust','ix*acc*.6'),
('drag','.55','damping','pow(.55,dt)'),('brake','.02','braking','pow(.02,dt) when reversing'),('clampRate','3','velocity','min(1,dt*3) soft clamp'),
('worldRadius','2900','bounds','position.length()>2900'),('boundBounce','.5','bounds','vel*.5 at limit'),
('shipRadius','6','collision','q=b.r+6'),('restRock','.25','collision','rock restitution'),('restMetal','.45','collision','metal restitution'),('impactMin','6','collision','-rel>6'),('impactDmgFree','10','collision','(-rel-10)'),('impactDmgScale','.7','collision','*.7'),('impactShake','.3','collision','shake .3'),
('evadeMinEn','10','evade','P.en<10'),('evadeCost','10','evade','P.en-=10'),('evadeCd','1.4','evade','P.ec=1.4'),('evadeInv','.35','evade','P.ev=.35'),('evadeSide','.3','evade','mv.x<-.3'),('evadeImpulse','75','evade','impulse *75'),
('camUp','7','camera','V(0,7,..)'),('camBack','30','camera','30+sp*.06'),('camSpeedBack','.06','camera','sp*.06'),('camFollow','9','camera','exp(-9*dt)'),('camTurn','8','camera','exp(-8*dt)'),('fov','70','camera','70+13*bf'),('fovBoost','13','camera','13*bf'),('shakeScale','.6','camera','shk*.6'),('shakeDecay','1.5','camera','shk-dt*1.5')]
TUNEJS='const TUNE=Object.freeze({'+','.join(k+':'+v for k,v,_,_ in TS)+'});'
R=[('const R=.28*Math.min(innerWidth,innerHeight)','const R=TUNE.mouseZone*Math.min(innerWidth,innerHeight)'),('const zr=.28*Math.min(innerWidth,innerHeight)','const zr=TUNE.mouseZone*Math.min(innerWidth,innerHeight)'),
('(t.clientX-t0.l[0])/55,y=(t.clientY-t0.l[1])/55','(t.clientX-t0.l[0])/TUNE.touchStick,y=(t.clientY-t0.l[1])/TUNE.touchStick'),('Math.abs(x)<.15?0:x/m;mv.y=Math.abs(y)<.15?0:y/m','Math.abs(x)<TUNE.touchDead?0:x/m;mv.y=Math.abs(y)<TUNE.touchDead?0:y/m'),('(t.clientX-t0.r[0])/80,y=(t.clientY-t0.r[1])/80','(t.clientX-t0.r[0])/TUNE.touchAim,y=(t.clientY-t0.r[1])/TUNE.touchAim'),
('(Math.abs(x)-.07)/.93','(Math.abs(x)-TUNE.dead)/TUNE.deadSpan'),('(.3*t+.7*t*t)','(TUNE.crvLin*t+TUNE.crvQuad*t*t)'),
('-crv(mx)*2.2*cfg.sens','-crv(mx)*TUNE.yawRate*cfg.sens'),('-crv(my)*1.8*cfg.sens','-crv(my)*TUNE.pitchRate*cfg.sens'),
('(yaw*.35-pm.rotation.z)*(1-Math.exp(-6*dt))','(yaw*TUNE.bankRoll-pm.rotation.z)*(1-Math.exp(-TUNE.bankRate*dt))'),('(pit*.1-pm.rotation.x)*(1-Math.exp(-6*dt))','(pit*TUNE.bankPitch-pm.rotation.x)*(1-Math.exp(-TUNE.bankRate*dt))'),
('if(P.en<=1)P.cd=1;else if(P.en>30)P.cd=0;','if(P.en<=TUNE.enMin)P.cd=1;else if(P.en>TUNE.enResume)P.cd=0;'),('K.boost&&!P.cd&&P.en>1?1:0','K.boost&&!P.cd&&P.en>TUNE.enMin?1:0'),
('P.en=cl(P.en+(bo?-26:14)*dt,0,100);P.bf+=(bo-P.bf)*Math.min(1,dt*4);','P.en=cl(P.en+(bo?-TUNE.boostDrain:TUNE.energyRegen)*dt,0,TUNE.enMax);P.bf+=(bo-P.bf)*Math.min(1,dt*TUNE.bfRate);'),
('const acc=60*(1+.1*up.thr)*(1+1.4*bo)*(K.sp?1.2:1),mxv=90*(1+.1*up.spd)*(1+(1+.15*up.wp)*bo)*(K.sp?1.15:1);','const acc=TUNE.accel*(1+TUNE.thrStep*up.thr)*(1+TUNE.boostAccel*bo)*(K.sp?TUNE.sprintAccel:1),mxv=TUNE.maxSpeed*(1+TUNE.spdStep*up.spd)*(1+(1+TUNE.warpStep*up.wp)*bo)*(K.sp?TUNE.sprintMax:1);'),
('bo*acc*.5).addScaledVector(P.rt,ix*acc*.6)','bo*acc*TUNE.boostThrust).addScaledVector(P.rt,ix*acc*TUNE.strafe)'),
('Math.pow(.55,dt));if(iz<0)P.vel.multiplyScalar(Math.pow(.02,dt))','Math.pow(TUNE.drag,dt));if(iz<0)P.vel.multiplyScalar(Math.pow(TUNE.brake,dt))'),
('P.vel.setLength(sp+(mxv-sp)*Math.min(1,dt*3))','P.vel.setLength(sp+(mxv-sp)*Math.min(1,dt*TUNE.clampRate))'),
('if(pl.position.length()>2900){pl.position.setLength(2900);P.vel.multiplyScalar(.5);','if(pl.position.length()>TUNE.worldRadius){pl.position.setLength(TUNE.worldRadius);P.vel.multiplyScalar(TUNE.boundBounce);'),
('q=b.r+6','q=b.r+TUNE.shipRadius'),("(1+(b.t==='rock'?.25:.45))","(1+(b.t==='rock'?TUNE.restRock:TUNE.restMetal))"),('if(-rel>6)','if(-rel>TUNE.impactMin)'),
('hurt(Math.max(0,(-rel-10)*.7));P.shk=Math.max(P.shk,.3)}}}}','hurt(Math.max(0,(-rel-TUNE.impactDmgFree)*TUNE.impactDmgScale));P.shk=Math.max(P.shk,TUNE.impactShake)}}}}'),
('P.en<10)return;P.en-=10;P.ec=1.4;P.ev=.35;P.vel.addScaledVector(P.rt,(K.l||mv.x<-.3?-1:1)*75)','P.en<TUNE.evadeMinEn)return;P.en-=TUNE.evadeCost;P.ec=TUNE.evadeCd;P.ev=TUNE.evadeInv;P.vel.addScaledVector(P.rt,(K.l||mv.x<-TUNE.evadeSide?-1:1)*TUNE.evadeImpulse)'),
('V(0,7,30+sp*.06)','V(0,TUNE.camUp,TUNE.camBack+sp*TUNE.camSpeedBack)'),('cam.position.lerp(tp,1-Math.exp(-9*dt));cam.quaternion.slerp(pl.quaternion,1-Math.exp(-8*dt));','cam.position.lerp(tp,1-Math.exp(-TUNE.camFollow*dt));cam.quaternion.slerp(pl.quaternion,1-Math.exp(-TUNE.camTurn*dt));'),
('P.shk*.6*(cfg.gp.rm?.25:1)));P.shk=Math.max(0,P.shk-dt*1.5)}','P.shk*TUNE.shakeScale*(cfg.gp.rm?.25:1)));P.shk=Math.max(0,P.shk-dt*TUNE.shakeDecay)}'),
('cam.fov=70+13*P.bf;cam.updateProjectionMatrix();EL.intensity=','cam.fov=TUNE.fov+TUNE.fovBoost*P.bf;cam.updateProjectionMatrix();EL.intensity=')]
for a,b in R: sub(a,b)
# ---------- 1. FLIGHT LOCK markers (each on its own line) ----------
mk=lambda k,n='':'// === FLIGHT LOCK %s%s ==='%(k,(': '+n) if k=='BEGIN' else '')
L=js.split('\n');o=[];hit=collections.Counter();k=0
while k<len(L):
    l=L[k]
    if l.startswith('function evade(){'): o+=[mk('BEGIN','evade'),l,mk('END')];hit['evade']+=1
    elif l.startswith("addEventListener('mousemove'"): o+=[mk('BEGIN','mouse-steering'),l,mk('END')];hit['mouse']+=1
    elif l.startswith(" tc.addEventListener('touchmove'"):
        assert L[k+1].startswith('  if(t.identifier===tid.r)') and L[k+1].rstrip().endswith('{passive:false});')
        o+=[mk('BEGIN','touch-stick'),l,L[k+1],mk('END')];k+=1;hit['touch']+=1
    elif l.startswith('const crv='): o+=[mk('BEGIN','steering-curve'),l,mk('END')];hit['crv']+=1
    elif l.startswith('function play(dt){P.t+=dt;'): o+=[l,mk('BEGIN','movement')];hit['play']+=1
    elif l.startswith(' P.fc-=dt;if(K.fire&&P.fc<=0)'): o+=[mk('END'),l];hit['playend']+=1
    elif l==' /* camera */': o+=[l,mk('BEGIN','camera')];hit['cam']+=1
    elif l.startswith(' cam.fov='):
        p=l.index('EL.intensity=');o+=[l[:p],mk('END'),' '+l[p:]];hit['camend']+=1
    else: o.append(l)
    k+=1
assert len(hit)==8 and all(v==1 for v in hit.values()),hit
js='\n'.join(o)
# ---------- 5. versioned save ----------
sub('function save(i){',"const SAVE_VERSION=1,SAVE_LEGACY=0; // unversioned saves are treated as legacy v0; newer-than-known versions are ignored\nconst saveVerOk=d=>{const v=d.saveVersion===undefined?SAVE_LEGACY:d.saveVersion;return Number.isInteger(v)&&v>=SAVE_LEGACY&&v<=SAVE_VERSION};\nfunction save(i){")
sub("JSON.stringify({G,up,st,ts:Date.now()})","JSON.stringify({saveVersion:SAVE_VERSION,G,up,st,ts:Date.now()})")
sub('d.up&&d.st)r.push({i,d})','d.up&&d.st&&saveVerOk(d))r.push({i,d})')
# ---------- 4+6. test hook and ?perf=1 overlay ----------
HOOK=r'''/* ---------- TEST HOOK (dev only): drives the normal action pathway (press/release, mo, mv) through the real play(dt) ---------- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function flightTestRun(script,o){o=o||{};const dt=o.dt||1/60,every=o.every||6,out=[],rnd0=Math.random,s0=S,sv=[CT,HZ,DFt],bodies=B.splice(0);if(o.seed!=null)Math.random=mulberry32(o.seed);
 try{(script.bodies||[]).forEach(b=>B.push({p:V(...b.p),r:b.r,v:null,t:b.t||'rock',st:1}));
  go('play');clearE();resetP();CT=HZ=DFt=1e9;Object.keys(K).forEach(k=>K[k]=0);mo.x=mo.y=mv.x=mv.y=0;P.sx=P.sy=0;
  const ini=script.init||{};P.vel.set(...(ini.vel||[0,0,0]));pl.position.set(...(ini.pos||[0,0,0]));pl.quaternion.identity();pm.rotation.set(0,0,0);
  P.en=100;P.cd=0;P.bf=0;P.bo=0;P.ev=0;P.ec=0;P.shk=0;P.cor=0;P.hu=P.mh;P.sh=smax();P.lk=null;P.dg=0;P.t=0;P.fc=0;
  cam.position.set(pl.position.x,pl.position.y+TUNE.camUp,pl.position.z+TUNE.camBack);cam.quaternion.identity();
  const rec=f=>out.push({t:f*dt,p:pl.position.toArray(),v:P.vel.toArray(),sp:P.vel.length(),en:P.en,bf:P.bf,cd:P.cd,ev:P.ev,ec:P.ec,q:pl.quaternion.toArray(),cam:cam.position.toArray(),fov:cam.fov});
  let held=[],f=0;rec(0);
  for(const s_ of script.steps){const keys=s_.keys||[];held.filter(a=>!keys.includes(a)).forEach(release);keys.filter(a=>!held.includes(a)).forEach(press);held=keys.slice();
   mo.x=(s_.mo||[0,0])[0];mo.y=(s_.mo||[0,0])[1];mv.x=(s_.mv||[0,0])[0];mv.y=(s_.mv||[0,0])[1];(s_.press||[]).forEach(press);
   const n=Math.round(s_.d/dt);for(let i=0;i<n;i++){play(dt);f++;if(f%every===0)rec(f)}}
  held.forEach(release);rec(f);
 }finally{Math.random=rnd0;B.length=0;bodies.forEach(b=>B.push(b));[CT,HZ,DFt]=sv;go(s0)}
 return {dt,every,samples:out,frames:out.length}}
window.CER_TEST={run:flightTestRun,flightLock:flightLockStatus,tune:TUNE,saveVersion:SAVE_VERSION};
/* ---------- DEBUG OVERLAY (?perf=1 only; nothing is created otherwise) ---------- */
const PERF=/[?&]perf=1(?:&|$)/.test(location.search);let PF=null,PFL=null,pfMs=16.7,pfN=0;
function perfTick(dt){if(!PERF)return;
 if(!PF){PF=document.createElement('pre');PF.id='perf';PF.style.cssText='position:fixed;left:50%;top:4px;transform:translateX(-50%);z-index:99;margin:0;padding:4px 8px;font:11px/1.3 monospace;color:#9ff;background:rgba(0,0,0,.6);pointer-events:none;white-space:pre';document.body.appendChild(PF);PFL=flightLockStatus()}
 pfMs+=(dt*1000-pfMs)*.1;if(++pfN%10)return;const ri=rd.info||{render:{},memory:{}};let pj=0;for(const j of PJ)if(j.on)pj++;
 PF.textContent=['FPS '+(1000/pfMs).toFixed(0)+'  frame '+pfMs.toFixed(1)+' ms','state '+S+'  region '+(RN||'-'),'enemies '+E.length+'  bodies '+B.length+'  scene '+sc.children.length,'projectiles '+pj+'/'+PJ.length+' (pool)  fx '+FX.length+'/220  lights '+LP.length+' pooled','gl calls '+(ri.render.calls||0)+'  tris '+(ri.render.triangles||0)+'  geo '+(ri.memory.geometries||0)+'  tex '+(ri.memory.textures||0),'FLIGHT LOCK: '+(PFL.ok===null?'n/a':PFL.ok?'OK':'FAIL')+'  '+PFL.hash,'save schema v'+SAVE_VERSION].join('\n')}
'''
sub('applyCfg();setMenu();go(\'menu\');requestAnimationFrame(loop);',HOOK+"applyCfg();setMenu();go('menu');requestAnimationFrame(loop);")
sub('rd.render(sc,cam)}','rd.render(sc,cam);perfTick(dt)}')
# ---------- top block: SRC, PAL, lock system, TUNE (inside the lock) ----------
TOP=r'''
const SRC=document.currentScript?document.currentScript.textContent:'';
/* PAL: centralized colors (values identical to the former inline literals). Names are descriptive only. */
'''+PALJS+r'''
/* FLIGHT LOCK system: flight source regions are fenced by marker comments (LKP + BEGIN/END). Their text, plus fingerprints of the steering
   helpers ss()/cl(), the default WASD bindings and default steering settings, is hashed (cyrb53) and compared with FLIGHT_LOCK_HASH.
   Changing flight code or TUNE therefore requires a deliberate re-seal (node pass0/pass0_tests.js seal). */
const LKP='// === FLIGHT LOCK ',FLIGHT_LOCK_REGIONS=7,FLIGHT_LOCK_HASH='__SEAL__';
function cyrb53(str,seed){let h1=0xdeadbeef^(seed||0),h2=0x41c6ce57^(seed||0);for(let i=0,ch;i<str.length;i++){ch=str.charCodeAt(i);h1=Math.imul(h1^ch,2654435761);h2=Math.imul(h2^ch,1597334677)}h1=Math.imul(h1^(h1>>>16),2246822507)^Math.imul(h2^(h2>>>13),3266489909);h2=Math.imul(h2^(h2>>>16),2246822507)^Math.imul(h1^(h1>>>13),3266489909);return(4294967296*(2097151&h2)+(h1>>>0)).toString(16)}
function flightLockRegions(src){const out=[],mb=LKP+'BEGIN: ',me=LKP+'END';let i=0;src=src.replace(/\r/g,'');for(;;){const a=src.indexOf(mb,i);if(a<0)break;const nl=src.indexOf('\n',a),name=src.slice(a+mb.length,nl).replace(/ ===\s*$/,''),b=src.indexOf(me,nl);if(b<0){out.push([name,null]);break}out.push([name,src.slice(nl+1,b)]);i=b+me.length}return out}
function flightLockCompute(src){const rg=flightLockRegions(src),deps=String(ss)+'|'+String(cl)+'|'+JSON.stringify({sens:CD.sens,smo:CD.smo,inv:CD.inv,bind:CD.bind})+'|'+[...HOLD].join(',');
 return{hash:cyrb53(rg.map(r=>r[0]+'\n'+r[1]).join('\n----\n')+'\n#deps\n'+deps),names:rg.map(r=>r[0]),broken:rg.some(r=>r[1]===null)}}
function flightLockStatus(){if(!SRC)return{ok:null,hash:'',expected:FLIGHT_LOCK_HASH,regions:[]};const r=flightLockCompute(SRC);return{ok:!r.broken&&r.names.length===FLIGHT_LOCK_REGIONS&&r.hash===FLIGHT_LOCK_HASH,hash:r.hash,expected:FLIGHT_LOCK_HASH,regions:r.names}}
'''+mk('BEGIN','tune')+'\n/* TUNE: every flight constant, extracted with its original value (see pass0/TUNE_TABLE.md). Inside the lock on purpose. */\n'+TUNEJS+'\n'+mk('END')+'\n'
sub('"use strict";\n','"use strict";'+TOP,1)
open(sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else OUT+'/cerebral.html','w').write(head+js+tail)
if '--no-docs' not in sys.argv:
    # ---------- docs ----------
    tb=['# TUNE table (Pass 0): constants extracted from the flight source, values unchanged\n','| Constant | Value | Group | Original expression |','|---|---|---|---|']+['| `TUNE.%s` | %s | %s | `%s` |'%(k,v,g,w) for k,v,g,w in TS]
    open(P0+'/TUNE_TABLE.md','w').write('\n'.join(tb)+'\n')
    facts['tune_count']=len(TS);facts['pal_hex_entries']=len(PALN);facts['pal_string_entries']=len(PALS)+2
    json.dump(facts,open(P0+'/baseline_facts.json','w'),indent=1)
    print('built; TUNE',len(TS),'PAL',len(palvals),'dead-code analysis',json.dumps(facts['dead_code_after']))