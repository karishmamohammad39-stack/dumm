const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

async function renderPdf() {
  console.log('========================================================');
  console.log('Rendering High-Definition Academic PDF via Headless Chrome');
  console.log('========================================================');

  const htmlPath = path.resolve('Project_Report_Documentation.html');
  const pdfPath = path.resolve('Project_Report_Documentation.pdf');

  if (!fs.existsSync(htmlPath)) {
    console.error('HTML file not found:', htmlPath);
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
  });

  const page = await browser.newPage();
  const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');
  console.log('Loading document:', fileUrl);

  await page.goto(fileUrl, {
    waitUntil: 'networkidle0',
    timeout: 60000
  });

  console.log('Generating PDF with A4 dimensions and academic margins...');
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '1in',
      bottom: '1in',
      left: '1.25in',
      right: '1in'
    },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `
      <div style="width: 100%; text-align: center; font-family: 'Times New Roman', serif; font-size: 10pt; color: #333333;">
        <span class="pageNumber"></span>
      </div>
    `
  });

  await browser.close();

  const stats = fs.statSync(pdfPath);
  console.log('========================================================');
  console.log('SUCCESS! Academic Project Report PDF Generated:');
  console.log('Location: ', pdfPath);
  console.log('File Size:', stats.size, 'bytes (~' + (stats.size / 1024).toFixed(1) + ' KB)');
  console.log('========================================================');
}

renderPdf().catch(err => {
  console.error('Error generating PDF:', err);
  process.exit(1);
});
