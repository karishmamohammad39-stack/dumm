const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

(async () => {
  console.log('Generating dummy video...');
  if (!fs.existsSync('dummy.mp4')) {
    execSync('ffmpeg -f lavfi -i testsrc=duration=5:size=1920x1080:rate=30 -c:v libx264 -preset ultrafast -y dummy.mp4', {stdio:'pipe'});
  }

  console.log('Launching browser...');
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', msg => {
    const text = msg.text();
    if (text.includes('[FFmpeg]') || text.includes('Export failed') || text.includes('Error')) {
      console.log('BROWSER LOG:', text);
    }
  });

  page.on('pageerror', err => {
    console.error('BROWSER ERROR:', err.message);
  });

  console.log('Navigating to http://localhost:5173...');
  await page.goto('http://localhost:5173', { waitUntil: 'networkidle0', timeout: 60000 });

  console.log('Uploading video...');
  const fileInput = await page.$('input[type="file"]');
  await fileInput.uploadFile(path.resolve('dummy.mp4'));

  // Wait for the video to load
  await page.waitForTimeout(2000);

  console.log('Toggling Cinematic Mode...');
  // Find the label containing "Force Telugu Cinematic Style"
  const toggleWrappers = await page.$$('.cinematic-toggle-wrap');
  if (toggleWrappers.length > 0) {
     const input = await toggleWrappers[0].$('input[type="checkbox"]');
     const checked = await page.evaluate(el => el.checked, input);
     if (!checked) {
        const toggleBox = await toggleWrappers[0].$('.toggle-box');
        await toggleBox.click();
     }
  }

  console.log('Clicking Generate Magic Cuts...');
  const buttons = await page.$$('button');
  for (const btn of buttons) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text && text.includes('Generate Magic Cuts')) {
      await btn.click();
      break;
    }
  }

  console.log('Waiting for export to complete or fail...');
  
  // Wait until we see "Your highlight reel is ready" OR "Export failed" in the pipeline status
  try {
    await page.waitForFunction(() => {
      const el = document.querySelector('.pipeline-title');
      const el2 = document.querySelector('.pipeline-status-card');
      if (!el2) return false;
      const text = el2.textContent;
      return text && (text.includes('Complete') || text.includes('failed') || text.includes('Error'));
    }, { timeout: 120000 });
  } catch(e) {
    console.log('Timeout waiting for completion');
  }

  // Get final status
  const status = await page.evaluate(() => {
    const el = document.querySelector('.pipeline-status-card');
    return el ? el.textContent : 'No pipeline status visible';
  });
  console.log('Final Status:', status);

  await browser.close();
  console.log('Done.');
})();
