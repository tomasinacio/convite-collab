// Browser checks for the RSVP form (the red-team findings). Run against a FRESH test Worker (node rsvp/worker/tools/devserver.mjs rsvp/output/seed.sql 8791 http://localhost:8766)
// and a test site built with --rsvp-config pointing at it, served on :8766. Uses the FAKE codes of rsvp/guests/codes.json (families 3 to 10).
// Run: source scripts/env.sh && node rsvp/page/form-checks.cjs
const PW='/home/tomin/.local/opt/node-v24.22.1-linux-x64/lib/node_modules/@playwright/cli/node_modules/playwright-core';
const {chromium,devices}=require(PW); const U='http://localhost:8766/';
const d={...devices['iPhone 15']}; delete d.defaultBrowserType;
let fails=0; const ok=(n,c)=>{console.log((c?'PASS ':'FAIL ')+n); if(!c)fails++;};
async function open(b,hash,extra={}){const c=await b.newContext({...d,reducedMotion:'reduce',...extra}); const p=await c.newPage(); await p.goto(U+'?lang=en'+(hash?'#'+hash:''),{waitUntil:'load'}); await p.waitForTimeout(700); await p.click('#seal'); await p.waitForTimeout(1500); return {c,p};}
const st=p=>p.getAttribute('#rsvp','data-state');
(async()=>{const b=await chromium.launch();
 // 1 draft isolation (same browser context)
 let {c,p}=await open(b,'JSCACCGYY5RJ26V0'); await p.click('#p1 .choice.yes'); await p.fill('#p1-d','SECRET nut allergy'); await p.fill('#msg','SECRET message');
 const p2=await c.newPage(); await p2.goto(U+'?lang=en#W4ZDSX50PP5TM9E4',{waitUntil:'load'}); await p2.waitForTimeout(700); await p2.click('#seal'); await p2.waitForTimeout(1500);
 ok('draft does not leak to another household', (await p2.inputValue('#msg'))==='' && !(await p2.isChecked('#p1 .choice.yes input')));
 const p3=await c.newPage(); await p3.goto(U+'?lang=en#JSCACCGYY5RJ26V0',{waitUntil:'load'}); await p3.waitForTimeout(700); await p3.click('#seal'); await p3.waitForTimeout(1500);
 ok('own draft is restored', (await p3.inputValue('#msg'))==='SECRET message');
 // 2 hung request: the answers stay and the network state shows within ~15 s
 ({c,p}=await open(b,'V332Z90SS91FDJWA')); await p.evaluate(()=>document.querySelectorAll('.person').forEach(f=>f.querySelector('input[value=no]').click())); await p.route('**/api/answer',()=>{});
 const t0=Date.now(); await p.click('#send'); await p.waitForTimeout(400); await p.waitForFunction(()=>document.getElementById('rsvp').dataset.state!=='sending',null,{timeout:25000}).catch(()=>{});
 ok('hung request ends in the network state, answers kept ('+Math.round((Date.now()-t0)/1000)+'s)', (await st(p))==='network' && await p.isChecked('#p1 .choice.no input'));
 // 3 reduced motion rule does not touch the face
 const dur=await p.evaluate(()=>getComputedStyle(document.querySelector('.skip')).transitionDuration);
 ok('face Skip transition untouched by the RSVP css (got '+dur+')', !/^0.001s$/.test(dur));
 // 4 code entry feedback
 ({c,p}=await open(b,'')); await p.fill('#code','SHORT'); await p.click('#codeform .btn'); ok('short code: visible message', (await p.innerText('#codeerr')).length>5 && await p.evaluate(()=>document.activeElement.id)==='code');
 await p.fill('#code','AAAABBBBCCCCDDDD'); await p.click('#codeform .btn'); await p.waitForTimeout(800); ok('wrong code: visible message and focus on field', (await p.innerText('#codeerr')).length>5 && await p.evaluate(()=>document.activeElement.id)==='code');
 await p.fill('#code','https://tomasinacio.github.io/convite/?lang=en#V332Z90SS91FDJWA'); await p.click('#codeform .btn'); await p.waitForTimeout(900); ok('pasted whole link works, focus lands in form', (await st(p))==='form' && /^p\d+-a$/.test(await p.evaluate(()=>document.activeElement.name||'')));
 // 5 server reply mapping
 for (const [status,body,expect,label] of [[403,'{"error":"forbidden_origin"}','network','403 forbidden_origin is not "closed"'],[429,'{"error":"too_many_changes"}','error','429 too_many_changes gets its own message'],[500,'x','network','500']]){
   ({c,p}=await open(b,'5V0MS0EHVWJ2MQA4')); await p.click('#p1 .choice.yes'); await p.click('#p2 .choice.yes').catch(()=>{});
   await p.route('**/api/answer',r=>r.fulfill({status,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body}));
   await p.evaluate(()=>{document.querySelectorAll('.person').forEach(f=>{const n=f.querySelector('input[value=yes]'); if(!f.querySelector('input:checked')&&!f.id.endsWith('3')) n.click();});});
   await p.click('#send'); await p.waitForTimeout(700); ok(label+' -> '+await st(p), (await st(p))===expect);}
 // 6 long text in the saved list
 ({c,p}=await open(b,'AMHP92KB3JEVFGB7')); await p.evaluate(()=>{document.querySelectorAll('.person').forEach(f=>f.querySelector('input[value=yes]').click());});
 await p.fill('#p1-d','x'.repeat(200)); await p.evaluate(()=>{const n=document.querySelector('#p3-n'); if(n) n.value='y'.repeat(80);}); await p.click('#send'); await p.waitForTimeout(1200);
 ok('saved list does not overflow the card ('+await st(p)+')', await p.evaluate(()=>{const r=document.querySelector('#savedlist').getBoundingClientRect(); const l=[...document.querySelectorAll('#savedlist li span:last-child')].every(e=>e.getBoundingClientRect().right<=innerWidth); return r.right<=innerWidth&&l;}));
 // 9 no role=alert
 ok('error summary has no role=alert', (await p.getAttribute('#errsum','role'))===null);
 // 11 all declined message
 ({c,p}=await open(b,'X7Q75EX76NS2TPBT')); await p.evaluate(()=>{document.querySelectorAll('.person').forEach(f=>f.querySelector('input[value=no]').click());}); await p.click('#send'); await p.waitForTimeout(1200);
 ok('all declined shows its own message', /miss you/.test(await p.innerText('#savedtext')));
 console.log(fails?('FAILURES: '+fails):'ALL PASS'); await b.close();})();
