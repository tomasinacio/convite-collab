const PW='/home/tomin/.local/opt/node-v24.22.1-linux-x64/lib/node_modules/@playwright/cli/node_modules/playwright-core';
const {chromium,devices}=require(PW); const d0={...devices['iPhone 15']}; delete d0.defaultBrowserType; const dev={...d0,viewport:{width:393,height:659},screen:{width:393,height:659}};
const B='file:///home/tomin/agent-config/projects/wedding-invite/comps/';
const U=[['v12',B+'prototype.v12.single.html?motion=full'],['v13full',B+'prototype.v13.single.html?motion=full']];
const W=[[0,2.5],[2.5,6],[6,10],[12,18]];
(async()=>{const b=await chromium.launch();
for(const [k,url] of U){ for(let r=0;r<2;r++){const c=await b.newContext(dev);const p=await c.newPage();const cdp=await c.newCDPSession(p);
  await p.goto(url,{waitUntil:'networkidle'}); await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))); await p.waitForTimeout(500);
  await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
  await p.evaluate(()=>{window.__f=[];window.__t0=0;document.getElementById('seal').addEventListener('click',()=>{window.__t0=performance.now();const tick=t=>{window.__f.push(t);if(t-window.__t0<19000)requestAnimationFrame(tick)};requestAnimationFrame(tick)},{capture:true})});
  await p.tap('#seal'); await p.waitForTimeout(19800);
  const o=await p.evaluate((W)=>W.map(([a,z])=>{const f=window.__f.filter(t=>t-window.__t0>=a*1000&&t-window.__t0<z*1000);const g=[];for(let i=1;i<f.length;i++)g.push(f[i]-f[i-1]);const s=[...g].sort((x,y)=>x-y);return `${a}-${z}s ${(1000*(f.length-1)/(f[f.length-1]-f[0])).toFixed(0)}fps p95 ${s[Math.floor(s.length*.95)]?.toFixed(0)}`}).join(' | '),W);
  console.log(k.padEnd(8),o); await c.close();}}
await b.close();})();
