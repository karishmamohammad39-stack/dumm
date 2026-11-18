const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

async function generatePdf() {
  const mdPath = path.join(__dirname, 'Review_2_PPT_Changes_and_Improvements.md');
  const pdfPath = path.join(__dirname, 'Review_2_PPT_Changes_and_Improvements.pdf');
  const markdownText = fs.readFileSync(mdPath, 'utf8');

  // Parse markdown into HTML
  const lines = markdownText.split('\n');
  let htmlBody = '';
  let inTable = false;
  let inCode = false;
  let codeContent = '';

  for (let line of lines) {
    line = line.trimEnd();

    // Code block handling
    if (line.startsWith('```')) {
      if (!inCode) {
        inCode = true;
        codeContent = '';
      } else {
        inCode = false;
        htmlBody += `<pre class="code-box"><code>${escapeHtml(codeContent)}</code></pre>`;
      }
      continue;
    }

    if (inCode) {
      codeContent += (codeContent ? '\n' : '') + line;
      continue;
    }

    // Table handling
    if (line.startsWith('|')) {
      if (!inTable) {
        inTable = true;
        htmlBody += '<table class="styled-table">';
      }
      if (line.includes('---')) {
        continue;
      }
      const cells = line.split('|').filter((c, i, a) => i > 0 && i < a.length - 1);
      const isHeader = !htmlBody.includes('<tbody>') && !htmlBody.includes('<tr>');
      const tag = isHeader ? 'th' : 'td';
      htmlBody += '<tr>' + cells.map(c => `<${tag}>${formatInline(c.trim())}</${tag}>`).join('') + '</tr>';
      continue;
    } else if (inTable) {
      inTable = false;
      htmlBody += '</table>';
    }

    if (line.startsWith('# ')) {
      htmlBody += `<h1 class="main-title">${line.replace('# ', '')}</h1>`;
    } else if (line.startsWith('## ')) {
      htmlBody += `<h2 class="sub-title">${line.replace('## ', '')}</h2>`;
    } else if (line.startsWith('### ')) {
      htmlBody += `<h3 class="section-title">${line.replace('### ', '')}</h3>`;
    } else if (line.startsWith('#### ')) {
      htmlBody += `<h4 class="sub-section-title">${line.replace('#### ', '')}</h4>`;
    } else if (line.startsWith('---')) {
      htmlBody += '<hr class="divider"/>';
    } else if (line.startsWith('- ') || line.startsWith('• ') || line.startsWith('* ')) {
      htmlBody += `<li class="bullet-item">${formatInline(line.replace(/^[-•*]\s+/, ''))}</li>`;
    } else if (/^\d+\.\s+/.test(line)) {
      htmlBody += `<p class="numbered-item">${formatInline(line)}</p>`;
    } else if (line.trim() === '') {
      htmlBody += '<div class="spacer"></div>';
    } else {
      htmlBody += `<p class="text-paragraph">${formatInline(line)}</p>`;
    }
  }

  function escapeHtml(text) {
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function formatInline(str) {
    return str
      .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      .replace(/👉/g, '<span class="emoji-callout">👉</span>')
      .replace(/✅/g, '<span class="status-icon green">✅</span>')
      .replace(/🔄/g, '<span class="status-icon blue">🔄</span>')
      .replace(/📌/g, '<span class="status-icon orange">📌</span>')
      .replace(/❌/g, '<span class="status-icon red">❌</span>');
  }

  const fullHtml = `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Project Review II - PPT Changes & Text Reference</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
      
      * {
        box-sizing: border-box;
      }
      body {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #1e293b;
        line-height: 1.55;
        padding: 40px 48px;
        font-size: 12.5px;
        background: #ffffff;
      }
      .main-title {
        font-size: 20px;
        font-weight: 800;
        color: #0f172a;
        text-align: center;
        margin: 16px 0 8px 0;
        letter-spacing: -0.3px;
        text-transform: uppercase;
      }
      .sub-title {
        font-size: 14px;
        font-weight: 700;
        color: #2563eb;
        text-align: center;
        margin: 4px 0;
      }
      .section-title {
        font-size: 14px;
        font-weight: 700;
        color: #0f172a;
        background: #f1f5f9;
        border-left: 4px solid #2563eb;
        padding: 8px 12px;
        margin: 20px 0 10px 0;
        border-radius: 0 6px 6px 0;
        page-break-after: avoid;
      }
      .sub-section-title {
        font-size: 13px;
        font-weight: 700;
        color: #334155;
        margin: 14px 0 6px 0;
        page-break-after: avoid;
      }
      .divider {
        border: none;
        border-top: 1.5px solid #e2e8f0;
        margin: 18px 0;
      }
      p.text-paragraph {
        margin: 4px 0;
        color: #334155;
      }
      p.numbered-item {
        margin: 6px 0 4px 12px;
        font-weight: 600;
        color: #0f172a;
      }
      li.bullet-item {
        margin-left: 20px;
        margin-bottom: 4px;
        color: #334155;
      }
      .code-box {
        background: #0f172a;
        color: #f8fafc;
        padding: 12px 14px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        line-height: 1.45;
        margin: 10px 0 14px 0;
        white-space: pre-wrap;
        word-break: break-word;
        border: 1px solid #1e293b;
        page-break-inside: avoid;
      }
      .inline-code {
        font-family: 'JetBrains Mono', monospace;
        background: #f1f5f9;
        color: #dc2626;
        padding: 2px 5px;
        border-radius: 4px;
        font-size: 11.5px;
        border: 1px solid #e2e8f0;
      }
      .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 11px;
        page-break-inside: avoid;
      }
      .styled-table th {
        background: #2563eb;
        color: #ffffff;
        font-weight: 700;
        text-align: left;
        padding: 8px 10px;
        border: 1px solid #2563eb;
      }
      .styled-table td {
        border: 1px solid #cbd5e1;
        padding: 7px 10px;
        color: #1e293b;
      }
      .styled-table tr:nth-child(even) td {
        background: #f8fafc;
      }
      .spacer {
        height: 6px;
      }
      strong {
        color: #0f172a;
      }
      .status-icon.green { color: #10b981; }
      .status-icon.blue { color: #2563eb; }
      .status-icon.orange { color: #f59e0b; }
      .status-icon.red { color: #ef4444; }
      
      @page {
        margin: 15mm 15mm 15mm 15mm;
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
      top: '15mm',
      right: '15mm',
      bottom: '15mm',
      left: '15mm'
    },
    printBackground: true
  });

  await browser.close();
  console.log('PDF successfully generated at:', pdfPath);
}

generatePdf().catch(err => {
  console.error('Error generating PDF:', err);
  process.exit(1);
});
