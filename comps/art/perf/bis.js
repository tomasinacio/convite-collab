const PW='/home/tomin/.local/opt/node-v24.22.1-linux-x64/lib/node_modules/@playwright/cli/node_modules/playwright-core';
const {chromium,devices}=require(PW); const d0={...devices['iPhone 15']}; delete d0.defaultBrowserType; const dev={...d0,viewport:{width:393,height:659},screen:{width:393,height:659}};
const URL='file:///home/tomin/agent-config/projects/wedding-invite/comps/prototype.v13.single.html?motion=full';
const V={base:'',nomask:'*{-webkit-mask-image:none !important;mask-image:none !important}',
 nosky:'.sky,.sky-b-wrap,.c1,.c2,.mist{display:none !important}',
 noground:'.bgrass-l,.bgrass-r,.grass-l,.grass-r,.bloom,.bloom-l,.strip,.bind,.grass-l2,.grass-r2,.soar,.grass-f1,.grass-f2,.grass-p{display:none !important}',
 notop:'.olive,.olive-b,.bough,.leaf,.bird{display:none !important}',
 nolow:'.land,.gate-box,.vine,.euca,.foot,.dogs{display:none !important}'};
(async()=>{const b=await chromium.launch();
for(const [k,css] of Object.entries(V)){const out=[];
 for(let r=0;r<2;r++){const c=await b.newContext(dev);const p=await c.newPage();const cdp=await c.newCDPSession(p);
  await p.goto(URL,{waitUntil:'networkidle'}); if(css) await p.addStyleTag({content:css});
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))); await p.waitForTimeout(500);
  await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
  await p.evaluate(()=>{window.__f=[];document.getElementById('seal').addEventListener('click',()=>{const t0=performance.now();const tick=t=>{window.__f.push(t);if(t-t0<8000)requestAnimationFrame(tick)};requestAnimationFrame(tick)},{capture:true})});
  await p.tap('#seal'); await p.waitForTimeout(8800);
  out.push(await p.evaluate(()=>{const f=window.__f,g=[];for(let i=1;i<f.length;i++)g.push(f[i]-f[i-1]);const s=[...g].sort((a,b)=>a-b);return (1000*(f.length-1)/(f[f.length-1]-f[0])).toFixed(1)+'fps p95 '+s[Math.floor(s.length*.95)].toFixed(0)}));
  await c.close();}
 console.log(k.padEnd(8),out.join(' | '));}
await b.close();})();
