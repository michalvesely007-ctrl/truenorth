const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [src, out, x, y, w, h, scale] = process.argv.slice(2);
  const b = await chromium.launch(); const pg = await b.newPage({deviceScaleFactor: parseFloat(scale)});
  await pg.setViewportSize({width: Math.round(554*3.7795), height: Math.round(392*3.7795)});
  await pg.goto('file://' + require('path').resolve(src)); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
  const k=3.7795; await pg.screenshot({path: out, clip:{x:x*k,y:y*k,width:w*k,height:h*k}}); await b.close();
})();
