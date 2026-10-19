// node shot.js <svg|html> <out.png|out.pdf> [widthmm heightmm] [scale]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [src, out, wmm, hmm, sc] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' + '' ? undefined : undefined });
  const page = await browser.newPage();
  const path = require('path');
  await page.goto('file://' + path.resolve(src));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  if (out.endsWith('.pdf')) {
    await page.pdf({ path: out, width: wmm + 'mm', height: hmm + 'mm', printBackground: true, margin: {top:0,left:0,right:0,bottom:0} });
  } else {
    const W = parseFloat(wmm), H = parseFloat(hmm), s = parseFloat(sc || '2');
    await page.setViewportSize({ width: Math.round(W * 3.7795), height: Math.round(H * 3.7795) });
    await page.screenshot({ path: out, fullPage: false, scale: 'css', type: 'png' , clip:{x:0,y:0,width:Math.round(W*3.7795),height:Math.round(H*3.7795)}});
  }
  await browser.close();
})();
