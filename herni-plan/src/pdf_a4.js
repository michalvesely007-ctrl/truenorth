const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => { const [src,out]=process.argv.slice(2); const b=await chromium.launch(); const p=await b.newPage();
await p.goto('file://'+require('path').resolve(src)); await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:out, format:'A4', printBackground:true, preferCSSPageSize:true}); await b.close(); })();
