const PW='/home/tomin/.local/opt/node-v24.22.1-linux-x64/lib/node_modules/@playwright/cli/node_modules/playwright-core';
const {chromium,devices}=require(PW); const d0={...devices['iPhone 15']}; delete d0.defaultBrowserType;
const B='file:///home/tomin/agent-config/projects/wedding-invite/comps/';
const U=[['v12',B+'prototype.v12.single.html?motion=full'],['v13full',B+'prototype.v13.single.html?motion=full'],['v13lite',B+'prototype.v13.single.html?motion=lite']];
const P=[[393,659],[360,740],[430,932]]; const RUNS=3;
(async()=>{const b=await chromium.launch();
for(const [w,h] of P){ const dev={...d0,viewport:{width:w,height:h},screen:{width:w,height:h}};
 for(const [k,url] of U){ const res=[];
  for(let r=0;r<RUNS;r++){ const c=await b.newContext(dev); const p=await c.newPage(); const cdp=await c.newCDPSession(p);
   await p.goto(url,{waitUntil:'networkidle'}); await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))); await p.waitForTimeout(500);
   await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
   await p.evaluate(()=>{window.__f=[];document.getElementById('seal').addEventListener('click',()=>{const t0=performance.now();const tick=t=>{window.__f.push(t);if(t-t0<8000)requestAnimationFrame(tick)};requestAnimationFrame(tick)},{capture:true})});
   await p.tap('#seal'); await p.waitForTimeout(8800);
   res.push(await p.evaluate(()=>{const f=window.__f,g=[];for(let i=1;i<f.length;i++)g.push(f[i]-f[i-1]);const s=[...g].sort((a,b)=>a-b);return {fps:+(1000*(f.length-1)/(f[f.length-1]-f[0])).toFixed(1),p95:+s[Math.floor(s.length*.95)].toFixed(1),over33:g.filter(x=>x>33).length,max:Math.round(s[s.length-1])}}));
   await c.close(); }
  const fs=res.map(x=>x.fps).sort((a,b)=>a-b);
  console.log(`${w}x${h}`,k.padEnd(8),'fps med',fs[1],'| runs',res.map(x=>`${x.fps}/p95 ${x.p95}/>33:${x.over33}/max ${x.max}`).join(' ; ')); } }
await b.close();})();
