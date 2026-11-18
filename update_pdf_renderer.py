# -*- coding: utf-8 -*-
with open("generate_final_report.cjs", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the PhantomJS rendering block with Puppeteer rendering
old_phantom_block = """// 3. Render PDF via PhantomJS
console.log('Rendering print-ready PDF using PhantomJS with exact A4 margins...');
const phantomPath = require('phantomjs-prebuilt').path;
const renderScript = path.join(__dirname, 'node_modules', 'markdown-pdf', 'phantom', 'render.js');
const runningsScript = path.join(__dirname, 'report_runnings.js');
const cssPath = path.join(__dirname, 'report_style.css');
const pdfPath = path.join(__dirname, 'Project_Report_Documentation.pdf');

const childArgs = [
  renderScript,
  path.resolve(htmlPath),
  path.resolve(pdfPath),
  __dirname,
  runningsScript,
  cssPath,
  cssPath,
  'A4',
  'portrait',
  JSON.stringify({
    top: '1in',
    bottom: '1in',
    left: '1.25in',
    right: '1in'
  }),
  1000,
  30000
];

childProcess.execFile(phantomPath, childArgs, function (err, stdout, stderr) {
  if (err) {
    console.error('Error rendering PDF:', err);
    process.exit(1);
  } else {
    const stats = fs.statSync(pdfPath);
    console.log('========================================================');
    console.log('SUCCESS! Academic Project Report Generated:');
    console.log('PDF Location:  ', pdfPath);
    console.log('PDF File Size: ', stats.size, 'bytes (~' + (stats.size / 1024).toFixed(1) + ' KB)');
    console.log('Markdown:      ', mdPath);
    console.log('HTML Version:  ', htmlPath);
    console.log('========================================================');
  }
});"""

new_puppeteer_block = """// 3. Render High-Definition PDF via Puppeteer (Headless Chrome)
console.log('Rendering print-ready PDF using Puppeteer with exact A4 academic margins...');
const puppeteer = require('puppeteer');
const pdfPath = path.join(__dirname, 'Project_Report_Documentation.pdf');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
    });
    const page = await browser.newPage();
    const fileUrl = 'file:///' + path.resolve(htmlPath).replace(/\\\\/g, '/');
    await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });
    
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
        <div style="width: 100%; text-align: center; font-family: 'Times New Roman', serif; font-size: 10pt; color: #111;">
          <span class="pageNumber"></span>
        </div>
      `
    });
    
    await browser.close();
    
    const stats = fs.statSync(pdfPath);
    console.log('========================================================');
    console.log('SUCCESS! Academic Project Report PDF Generated:');
    console.log('PDF Location:  ', pdfPath);
    console.log('PDF File Size: ', stats.size, 'bytes (~' + (stats.size / 1024).toFixed(1) + ' KB)');
    console.log('Markdown:      ', mdPath);
    console.log('HTML Version:  ', htmlPath);
    console.log('========================================================');
  } catch (err) {
    console.error('Error rendering PDF via Puppeteer:', err);
    process.exit(1);
  }
})();"""

if old_phantom_block in code:
    code = code.replace(old_phantom_block, new_puppeteer_block)
    print("Replaced with Puppeteer.")
else:
    # Use regex
    import re
    code = re.sub(r'// 3\. Render PDF via PhantomJS[\s\S]*?childProcess\.execFile[\s\S]*?\}\);', new_puppeteer_block, code)
    print("Replaced via regex.")

with open("generate_final_report.cjs", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved generate_final_report.cjs successfully.")
