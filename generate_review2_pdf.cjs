const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

async function convertMdToPdf() {
  const mdPath = path.join(__dirname, 'Project_Review_2_Documentation.md');
  const pdfPath = path.join(__dirname, 'Project_Review_2_Documentation.pdf');
  const markdownText = fs.readFileSync(mdPath, 'utf8');

  // Convert basic markdown to formatted HTML
  const lines = markdownText.split('\n');
  let htmlBody = '';
  let inTable = false;
  let inList = false;

  for (let line of lines) {
    line = line.trimEnd();

    // Table handling
    if (line.startsWith('|')) {
      if (!inTable) {
        inTable = true;
        htmlBody += '<table>';
      }
      if (line.includes('---')) {
        continue; // delimiter row
      }
      const cells = line.split('|').filter((c, i, a) => i > 0 && i < a.length - 1);
      const isHeader = !htmlBody.includes('<tbody>') && !htmlBody.includes('<tr>');
      htmlBody += '<tr>' + cells.map(c => `<td>${c.trim().replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>').replace(/<br>/g, '<br/>')}</td>`).join('') + '</tr>';
      continue;
    } else if (inTable) {
      inTable = false;
      htmlBody += '</table>';
    }

    if (line.startsWith('# ')) {
      htmlBody += `<h1>${line.replace('# ', '')}</h1>`;
    } else if (line.startsWith('## ')) {
      htmlBody += `<h2>${line.replace('## ', '')}</h2>`;
    } else if (line.startsWith('### ')) {
      htmlBody += `<h3>${line.replace('### ', '')}</h3>`;
    } else if (line.startsWith('#### ')) {
      htmlBody += `<h4>${line.replace('#### ', '')}</h4>`;
    } else if (line.startsWith('---')) {
      htmlBody += '<hr/>';
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      htmlBody += `<li>${line.replace(/^[-*]\s+/, '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>')}</li>`;
    } else if (/^\d+\.\s+/.test(line)) {
      htmlBody += `<p class="numbered">${line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>')}</p>`;
    } else if (line.trim() === '') {
      htmlBody += '<div class="space"></div>';
    } else {
      htmlBody += `<p>${line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>')}</p>`;
    }
  }

  const fullHtml = `
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf-8">
    <title>Project Review - II</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
      body {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
        line-height: 1.6;
        padding: 40px 50px;
        font-size: 13px;
        background: #ffffff;
      }
      h1 {
        font-size: 22px;
        color: #0f172a;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 8px;
        margin-top: 25px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
      h2 {
        font-size: 16px;
        color: #1e40af;
        margin-top: 15px;
        margin-bottom: 8px;
        text-align: center;
      }
      h3 {
        font-size: 15px;
        color: #0f172a;
        border-left: 4px solid #2563eb;
        padding-left: 10px;
        margin-top: 20px;
        margin-bottom: 10px;
      }
      h4 {
        font-size: 13px;
        color: #334155;
        margin-top: 12px;
        margin-bottom: 6px;
        font-weight: 700;
      }
      p {
        margin: 4px 0;
      }
      .numbered {
        margin-left: 15px;
        font-weight: 500;
      }
      li {
        margin-left: 25px;
        margin-bottom: 4px;
      }
      hr {
        border: none;
        border-top: 1.5px solid #e2e8f0;
        margin: 20px 0;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 11px;
      }
      th, td {
        border: 1px solid #cbd5e1;
        padding: 8px 10px;
        text-align: left;
        vertical-align: top;
      }
      tr:first-child td {
        background-color: #f1f5f9;
        font-weight: bold;
        color: #0f172a;
      }
      tr:nth-child(even) {
        background-color: #f8fafc;
      }
      .space {
        height: 6px;
      }
      strong {
        color: #0f172a;
      }
    </style>
  </head>
  <body>
    ${htmlBody}
  </body>
  </html>
  `;

  console.log('Launching browser to render PDF...');
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const executablePath = fs.existsSync(edgePath) ? edgePath : (fs.existsSync(chromePath) ? chromePath : undefined);

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setContent(fullHtml, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    margin: {
      top: '20mm',
      right: '15mm',
      bottom: '20mm',
      left: '15mm'
    },
    printBackground: true
  });

  await browser.close();
  console.log('PDF successfully generated at:', pdfPath);
}

convertMdToPdf().catch(err => {
  console.error('Error generating PDF:', err);
  process.exit(1);
});
