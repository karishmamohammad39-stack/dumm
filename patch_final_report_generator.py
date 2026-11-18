# -*- coding: utf-8 -*-
with open("generate_final_report.cjs", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the hardcoded mdReport and the file write
old_part_start = code.find("// 1. Build the updated Markdown Documentation")
old_part_end = code.find("// 2. Build the HTML Document matching University Template")

new_read_code = """// 1. Read the calibrated Markdown Documentation
const mdPath = path.join(__dirname, 'Project_Report_Documentation.md');
const mdReport = fs.readFileSync(mdPath, 'utf8');
console.log('Loaded calibrated Project_Report_Documentation.md, length:', mdReport.length);

"""

code = code[:old_part_start] + new_read_code + code[old_part_end:]

# Also update the Chrome PDF generation at the end
puppeteer_block = """// 3. Render High-Definition PDF via Google Chrome Headless
console.log('Rendering print-ready PDF using Google Chrome with exact A4 academic margins...');
const pdfPath = path.join(__dirname, 'Project_Report_Documentation.pdf');
const chromePath = 'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe';

const chromeArgs = [
  '--headless',
  '--disable-gpu',
  '--no-pdf-header-footer',
  '--print-to-pdf=' + path.resolve(pdfPath),
  path.resolve(htmlPath)
];

childProcess.execFile(chromePath, chromeArgs, function (err, stdout, stderr) {
  if (err) {
    console.error('Error rendering PDF with Chrome:', err);
    process.exit(1);
  } else {
    const stats = fs.statSync(pdfPath);
    console.log('========================================================');
    console.log('SUCCESS! Academic Project Report PDF Generated via Chrome:');
    console.log('PDF Location:  ', pdfPath);
    console.log('PDF File Size: ', stats.size, 'bytes (~' + (stats.size / 1024).toFixed(1) + ' KB)');
    console.log('Markdown:      ', mdPath);
    console.log('HTML Version:  ', htmlPath);
    console.log('========================================================');
  }
});
"""

# Replace the Puppeteer block or Phantom block at the end
code = code[:code.find("// 3. Render")] + puppeteer_block

with open("generate_final_report.cjs", "w", encoding="utf-8") as f:
    f.write(code)

print("Patched generate_final_report.cjs successfully.")
