const PW='/home/tomin/.local/opt/node-v24.22.1-linux-x64/lib/node_modules/@playwright/cli/node_modules/playwright-core';
const {chromium,devices}=require(PW); const d0={...devices['iPhone 15']}; delete d0.defaultBrowserType; const dev={...d0,viewport:{width:393,height:659},screen:{width:393,height:659}};
const URL='file:///home/tomin/agent-config/projects/wedding-invite/comps/prototype.v13.single.html?motion=full';
const off=(sel)=>`${sel}{animation:none !important;opacity:1 !important;transform:none !important;translate:none !important;rotate:none !important}`;
const V={base:'',
 sky:off('.sky,.sky>.in,.sky-b-wrap,.sky-b,.c1,.c1>.in,.c2,.c2>.in,.mist,.land'),
 top:off('.olive,.olive>.in,.olive-b,.olive-b>.in,.bough,.bough .fruit,.bough .fruit>.in,.leaf'),
 ground:off('.bgrass-l,.bgrass-r,.grass-l,.grass-l>.in,.grass-r,.grass-r>.in,.bloom,.bloom-l,.strip,.bind,.soar,.soar>.in'),
 text:off('.kicker,.panel,.when,.names-block .seq,.pen .ch')};
(async()=>{const b=await chromium.launch();
for(const [k,css] of Object.entries(V)){const out=[];
 for(let r=0;r<2;r++){const c=await b.newContext(dev);const p=await c.newPage();const cdp=await c.newCDPSession(p);
  await p.goto(URL,{waitUntil:'networkidle'}); if(css) await p.addStyleTag({content:css});
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))); await p.waitForTimeout(500);
  await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
  await p.evaluate(()=>{window.__f=[];window.__t0=0;document.getElementById('seal').addEventListener('click',()=>{window.__t0=performance.now();const tick=t=>{window.__f.push(t);if(t-window.__t0<10500)requestAnimationFrame(tick)};requestAnimationFrame(tick)},{capture:true})});
  await p.tap('#seal'); await p.waitForTimeout(11200);
  out.push(await p.evaluate(()=>{const f=window.__f.filter(t=>t-window.__t0>=2500&&t-window.__t0<10000);const g=[];for(let i=1;i<f.length;i++)g.push(f[i]-f[i-1]);const s=[...g].sort((x,y)=>x-y);return `${(1000*(f.length-1)/(f[f.length-1]-f[0])).toFixed(0)}fps p95 ${s[Math.floor(s.length*.95)]?.toFixed(0)}`}));
  await c.close();}
 console.log(k.padEnd(8),out.join(' | '));}
await b.close();})();
