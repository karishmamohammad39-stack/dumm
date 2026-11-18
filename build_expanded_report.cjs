const fs = require('fs');
const path = require('path');
const docx = require('docx');
const childProcess = require('child_process');

const {
  Document, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle,
  PageBreak, ImageRun, Footer, PageNumber, NumberFormat,
  Packer, ShadingType
} = docx;

console.log('========================================================');
console.log('EXPANDING FINAL ACADEMIC DOCUMENTATION TO 40 PAGES');
console.log('Targeting: Balaji Institute of Technology & Science Template');
console.log('Department of CSE (Data Science) - 2026-2027');
console.log('========================================================');

const bitsLogoPath = path.join(__dirname, 'bits_logo.jpg');
const diagDir = path.join(__dirname, 'diagrams');

let bitsLogoBase64 = '';
if (fs.existsSync(bitsLogoPath)) {
  bitsLogoBase64 = fs.readFileSync(bitsLogoPath).toString('base64');
}

const FONT_NAME = 'Times New Roman';
const COLOR_CRIMSON = 'B22222';
const COLOR_BLUE = '1B65A4';
const COLOR_GREEN = '1E7E34';
const COLOR_BLACK = '111111';
const COLOR_MUTED = '475569';

// -------------------------------------------------------------------------
// DOCX BUILDER HELPERS
// -------------------------------------------------------------------------
function p(textRuns, options = {}) {
  let children = [];
  if (typeof textRuns === 'string') {
    children = parseFormattedText(textRuns, options.size || 24);
  } else if (Array.isArray(textRuns)) {
    children = textRuns;
  } else {
    children = [textRuns];
  }
  return new Paragraph({
    alignment: options.alignment || AlignmentType.JUSTIFIED,
    indent: options.firstLine ? { firstLine: 504 } : undefined, // 0.35"
    spacing: {
      line: 360, // 1.5 line spacing (240 * 1.5)
      lineRule: 'auto',
      before: options.before !== undefined ? options.before : 0,
      after: options.after !== undefined ? options.after : 140
    },
    children: children
  });
}

function run(text, options = {}) {
  return new TextRun({
    text: text,
    font: options.font || FONT_NAME,
    size: options.size || 24, // 12pt default
    bold: !!options.bold,
    italics: !!options.italics,
    color: options.color || COLOR_BLACK
  });
}

function parseFormattedText(text, defaultSize = 24) {
  const runs = [];
  const regex = /(\*\*.*?\*\*|\*.*?\*|`.*?`|[^*`]+)/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    const chunk = match[0];
    if (chunk.startsWith('**') && chunk.endsWith('**')) {
      runs.push(run(chunk.slice(2, -2), { bold: true, size: defaultSize }));
    } else if (chunk.startsWith('*') && chunk.endsWith('*')) {
      runs.push(run(chunk.slice(1, -1), { italics: true, size: defaultSize }));
    } else if (chunk.startsWith('`') && chunk.endsWith('`')) {
      runs.push(new TextRun({ text: chunk.slice(1, -1), font: 'Consolas', size: defaultSize - 2, color: '0369A1' }));
    } else if (chunk) {
      runs.push(run(chunk, { size: defaultSize }));
    }
  }
  return runs.length > 0 ? runs : [run(text, { size: defaultSize })];
}

function chapterHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    pageBreakBefore: true,
    spacing: { before: 200, after: 360, line: 360 },
    children: [
      new TextRun({
        text: title.toUpperCase(),
        font: FONT_NAME,
        size: 28, // 14pt
        bold: true,
        color: COLOR_BLACK
      })
    ]
  });
}

function subsectionHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 280, after: 120, line: 360 },
    children: [
      new TextRun({
        text: title,
        font: FONT_NAME,
        size: 24, // 12pt
        bold: true,
        color: COLOR_BLACK
      })
    ]
  });
}

function subsubsectionHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 200, after: 80, line: 360 },
    children: [
      new TextRun({
        text: title,
        font: FONT_NAME,
        size: 24, // 12pt
        bold: true,
        italics: true,
        color: COLOR_BLACK
      })
    ]
  });
}

function imageFigure(imgPath, width, height, captionText) {
  if (!fs.existsSync(imgPath)) {
    return [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 120, after: 120 },
        children: [run(`[Figure: ${captionText}]`, { italics: true, size: 22, color: COLOR_MUTED })]
      })
    ];
  }
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 160, after: 80 },
      children: [
        new ImageRun({
          data: fs.readFileSync(imgPath),
          transformation: { width, height }
        })
      ]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 60, after: 180 },
      children: [
        new TextRun({
          text: captionText,
          font: FONT_NAME,
          size: 22, // 11pt
          italics: true,
          color: COLOR_BLACK
        })
      ]
    })
  ];
}

function academicTable(headers, rows, colWidthPercentages) {
  const tableRows = [];
  tableRows.push(new TableRow({
    children: headers.map((h, i) => new TableCell({
      width: { size: colWidthPercentages[i], type: WidthType.PERCENTAGE },
      shading: { type: ShadingType.CLEAR, fill: 'F8FAFC' },
      borders: {
        top: { style: BorderStyle.SINGLE, size: 12, color: '000000' },
        bottom: { style: BorderStyle.SINGLE, size: 12, color: '000000' },
        left: { style: BorderStyle.NONE },
        right: { style: BorderStyle.NONE }
      },
      children: [
        new Paragraph({
          alignment: i === headers.length - 1 && h.includes('PAGE') ? AlignmentType.RIGHT : AlignmentType.LEFT,
          spacing: { before: 80, after: 80 },
          children: [new TextRun({ text: h, font: FONT_NAME, size: 22, bold: true, color: COLOR_BLACK })]
        })
      ]
    }))
  }));

  rows.forEach((r, rowIdx) => {
    const isLast = rowIdx === rows.length - 1;
    tableRows.push(new TableRow({
      children: r.map((cellText, i) => new TableCell({
        width: { size: colWidthPercentages[i], type: WidthType.PERCENTAGE },
        borders: {
          top: { style: BorderStyle.NONE },
          bottom: isLast ? { style: BorderStyle.SINGLE, size: 12, color: '000000' } : { style: BorderStyle.SINGLE, size: 4, color: 'CBD5E1' },
          left: { style: BorderStyle.NONE },
          right: { style: BorderStyle.NONE }
        },
        children: [
          new Paragraph({
            alignment: i === r.length - 1 && (/^\d+$/.test(cellText.trim())) ? AlignmentType.RIGHT : AlignmentType.LEFT,
            spacing: { before: 50, after: 50 },
            children: parseFormattedText(cellText, 21) // 10.5pt
          })
        ]
      }))
    }));
  });

  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: tableRows
  });
}

function codeBlock(codeText) {
  const lines = codeText.split('\n');
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: 'CBD5E1' },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: 'CBD5E1' },
      left: { style: BorderStyle.SINGLE, size: 16, color: '1B65A4' },
      right: { style: BorderStyle.SINGLE, size: 4, color: 'CBD5E1' }
    },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            shading: { type: ShadingType.CLEAR, fill: 'F8FAFC' },
            margins: { top: 100, bottom: 100, left: 140, right: 140 },
            children: lines.map(line => new Paragraph({
              spacing: { line: 240, before: 0, after: 20 },
              children: [
                new TextRun({
                  text: line || ' ',
                  font: 'Consolas',
                  size: 19, // 9.5pt
                  color: '0F172A'
                })
              ]
            }))
          })
        ]
      })
    ]
  });
}

module.exports = {
  p, run, parseFormattedText, chapterHeading, subsectionHeading, subsubsectionHeading,
  imageFigure, academicTable, codeBlock,
  bitsLogoPath, diagDir, bitsLogoBase64,
  FONT_NAME, COLOR_CRIMSON, COLOR_BLUE, COLOR_GREEN, COLOR_BLACK, COLOR_MUTED
};
