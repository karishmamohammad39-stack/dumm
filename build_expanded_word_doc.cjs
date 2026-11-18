const fs = require('fs');
const path = require('path');
const docx = require('docx');

const {
  Document, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle,
  PageBreak, ImageRun, Footer, PageNumber, NumberFormat,
  Packer, ShadingType
} = docx;

console.log('========================================================');
console.log('Building Expanded Word Document (.docx)');
console.log('Strict Adherence to Project Formatting Guidelines');
console.log('========================================================');

const bitsLogoPath = path.join(__dirname, 'bits_logo.jpg');
const diagDir = path.join(__dirname, 'diagrams');
const mdPath = path.join(__dirname, 'Project_Report_Documentation.md');

const FONT_NAME = 'Times New Roman';
const COLOR_CRIMSON = 'B22222';
const COLOR_BLUE = '1B65A4';
const COLOR_GREEN = '1E7E34';
const COLOR_BLACK = '111111';
const COLOR_MUTED = '475569';

function run(text, options = {}) {
  return new TextRun({
    text: text,
    font: options.font || FONT_NAME,
    size: options.size || 24, // 12pt default (24 half-points)
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
    indent: options.firstLine ? { firstLine: 504 } : (options.indent ? options.indent : undefined),
    spacing: {
      line: 360, // 1.5 line spacing (240 * 1.5)
      lineRule: 'auto',
      before: options.before !== undefined ? options.before : 0,
      after: options.after !== undefined ? options.after : 100
    },
    children: children
  });
}

function chapterHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    pageBreakBefore: true,
    spacing: { before: 200, after: 300, line: 360 },
    children: [
      new TextRun({
        text: title.toUpperCase(),
        font: FONT_NAME,
        size: 28, // 14pt, Bold, Uppercase
        bold: true,
        color: COLOR_BLACK
      })
    ]
  });
}

function subsectionHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 240, after: 100, line: 360 },
    children: [
      new TextRun({
        text: title,
        font: FONT_NAME,
        size: 24, // 12pt, Bold
        bold: true,
        color: COLOR_BLACK
      })
    ]
  });
}

function subsubsectionHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 180, after: 80, line: 360 },
    children: [
      new TextRun({
        text: title,
        font: FONT_NAME,
        size: 24, // 12pt, Bold, Italic
        bold: true,
        italics: true,
        color: COLOR_BLACK
      })
    ]
  });
}

function tableTitle(titleText) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 180, after: 80, line: 360 },
    children: [
      new TextRun({
        text: titleText,
        font: FONT_NAME,
        size: 22, // 11pt, Italic / Bold as per Table guidelines
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
        spacing: { before: 100, after: 100 },
        children: [run(`[Figure: ${captionText}]`, { italics: true, size: 22, color: COLOR_MUTED })]
      })
    ];
  }
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 140, after: 60 },
      children: [
        new ImageRun({
          data: fs.readFileSync(imgPath),
          transformation: { width, height }
        })
      ]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 40, after: 160 },
      children: [
        new TextRun({
          text: captionText,
          font: FONT_NAME,
          size: 22, // 11pt, Italic (Captions - 11 pt, Italic, Centered below figure)
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
      width: { size: colWidthPercentages[i] || Math.floor(100 / headers.length), type: WidthType.PERCENTAGE },
      shading: { type: ShadingType.CLEAR, fill: 'F1F5F9' },
      borders: {
        top: { style: BorderStyle.SINGLE, size: 12, color: '000000' },
        bottom: { style: BorderStyle.SINGLE, size: 12, color: '000000' },
        left: { style: BorderStyle.NONE },
        right: { style: BorderStyle.NONE }
      },
      children: [
        new Paragraph({
          alignment: i === headers.length - 1 && h.includes('PAGE') ? AlignmentType.RIGHT : AlignmentType.LEFT,
          spacing: { before: 60, after: 60 },
          children: [new TextRun({ text: h, font: FONT_NAME, size: 22, bold: true, color: COLOR_BLACK })]
        })
      ]
    }))
  }));

  rows.forEach((r, rowIdx) => {
    const isLast = rowIdx === rows.length - 1;
    tableRows.push(new TableRow({
      children: r.map((cellText, i) => new TableCell({
        width: { size: colWidthPercentages[i] || Math.floor(100 / headers.length), type: WidthType.PERCENTAGE },
        borders: {
          top: { style: BorderStyle.NONE },
          bottom: isLast ? { style: BorderStyle.SINGLE, size: 12, color: '000000' } : { style: BorderStyle.SINGLE, size: 4, color: 'CBD5E1' },
          left: { style: BorderStyle.NONE },
          right: { style: BorderStyle.NONE }
        },
        children: [
          new Paragraph({
            alignment: i === r.length - 1 && (/^\d+$/.test(cellText.trim())) ? AlignmentType.RIGHT : AlignmentType.LEFT,
            spacing: { before: 40, after: 40 },
            children: parseFormattedText(cellText, 20) // 10pt for compact table body
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
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: lines.map(line => new Paragraph({
              spacing: { line: 240, before: 0, after: 15 },
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

// -------------------------------------------------------------------------
// SECTION 1: PRELIMINARY PAGES (i to x)
// Strict Adherence to Item 3: Table of Contents Format
// 1. Outer Cover Page
// 2. Inner Title Page
// 3. Certificate
// 4. Acknowledgement
// 5. Abstract
// 6. Table of Contents
// 7. List of Figures
// 8. List of Tables
// 9. List of Abbreviations
// -------------------------------------------------------------------------
const prelimElements = [];

// 1. Outer Cover Page (Times New Roman, 16 pt, Bold, Uppercase, Centered)
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 100, after: 40 },
    children: [run('A MAJOR PROJECT REPORT', { bold: true, size: 32 })] // 16 pt
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 50 },
    children: [run('ON', { bold: true, size: 28 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [
      run('VIBE-CUTS (REEL): AI-POWERED AUTOMATED HIGHLIGHT REEL GENERATION AND BEAT-SYNCED VIDEO EDITING SYSTEM', {
        bold: true,
        size: 32, // 16 pt, Bold, Uppercase, Centered
        color: COLOR_CRIMSON
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 20 },
    children: [run('Submitted in Partial Fulfilment of the Requirements for', { size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 40 },
    children: [run('The Award of Degree of', { size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 20 },
    children: [run('BACHELOR OF TECHNOLOGY', { bold: true, size: 32 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 20 },
    children: [run('IN', { bold: true, size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 80 },
    children: [run('COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', { bold: true, size: 28, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 30 },
    children: [run('By', { bold: true, size: 24 })]
  }),
  new Table({
    width: { size: 75, type: WidthType.PERCENTAGE },
    alignment: AlignmentType.CENTER,
    rows: [
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('KATHULA AISHWARYA', { bold: true, size: 24 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6746)', { bold: true, size: 24 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('BURA ALEKHYA', { bold: true, size: 24 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6719)', { bold: true, size: 24 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('GANAPARAPU SAHAN', { bold: true, size: 24 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6733)', { bold: true, size: 24 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('ENAKONDA VISHNUVARDHAN REDDY', { bold: true, size: 24 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6730)', { bold: true, size: 24 })] })] })
        ]
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 20 },
    children: [run('UNDER THE GUIDANCE OF', { bold: true, size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 10 },
    children: [run('Mr. K. VIJAY KUMAR', { bold: true, size: 26, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 60 },
    children: [run('Assistant Professor, Department of CSE (Data Science)', { size: 23 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 10 },
    children: fs.existsSync(bitsLogoPath) ? [
      new ImageRun({
        data: fs.readFileSync(bitsLogoPath),
        transformation: { width: 75, height: 75 }
      })
    ] : []
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 10 },
    children: [run('DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', { bold: true, size: 24, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 10 },
    children: [run('BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE', { bold: true, size: 28, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 5 },
    children: [run('(AUTONOMOUS)', { bold: true, size: 24, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 5 },
    children: [run('Accredited by NBA (UG-CE, EEE, ECE, ME & CSE Programmes) & NAAC A+ Grade', { size: 19 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 5 },
    children: [run('(Affiliated to JNTU Hyderabad and Approved by the AICTE, New Delhi)', { size: 19 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 10 },
    children: [run('NARSAMPET, WARANGAL-506331, TELANGANA, INDIA', { size: 20 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 20 },
    children: [run('2026-2027', { bold: true, size: 24 })]
  }),
  new Paragraph({ children: [new PageBreak()] })
);

// 2. Inner Title Page (Times New Roman, 16 pt, Bold, Uppercase, Centered)
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 40 },
    children: [run('A MAJOR PROJECT REPORT', { bold: true, size: 32 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 50 },
    children: [run('ON', { bold: true, size: 28 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [
      run('VIBE-CUTS (REEL): AI-POWERED AUTOMATED HIGHLIGHT REEL GENERATION AND BEAT-SYNCED VIDEO EDITING SYSTEM', {
        bold: true,
        size: 32,
        color: COLOR_CRIMSON
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 20 },
    children: [run('Submitted in Partial Fulfilment of the Requirements for the Award of Degree of', { size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 20 },
    children: [run('BACHELOR OF TECHNOLOGY', { bold: true, size: 32 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 20 },
    children: [run('IN', { bold: true, size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 80 },
    children: [run('COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', { bold: true, size: 28, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 30 },
    children: [run('By', { bold: true, size: 24 })]
  }),
  new Table({
    width: { size: 75, type: WidthType.PERCENTAGE },
    alignment: AlignmentType.CENTER,
    rows: [
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('KATHULA AISHWARYA', { bold: true, size: 24 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6746)', { bold: true, size: 24 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('BURA ALEKHYA', { bold: true, size: 24 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6719)', { bold: true, size: 24 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('GANAPARAPU SAHAN', { bold: true, size: 24 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6733)', { bold: true, size: 24 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('ENAKONDA VISHNUVARDHAN REDDY', { bold: true, size: 24 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6730)', { bold: true, size: 24 })] })] })
        ]
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 20 },
    children: [run('Under the Esteemed Guidance of', { bold: true, size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 10 },
    children: [run('Mr. K. VIJAY KUMAR', { bold: true, size: 26, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 100 },
    children: [run('Assistant Professor, Department of CSE (Data Science)', { size: 23 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 10 },
    children: [run('DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', { bold: true, size: 24, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 10 },
    children: [run('BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE (AUTONOMOUS)', { bold: true, size: 26, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 10 },
    children: [run('Narsampet, Warangal - 506 331, Telangana, India', { size: 21 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 20 },
    children: [run('Academic Year: 2026-2027', { bold: true, size: 24 })]
  }),
  new Paragraph({ children: [new PageBreak()] })
);

// 3. Certificate Page
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 15 },
    children: [run('BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE', { bold: true, size: 28, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 15 },
    children: [run('(AUTONOMOUS)', { bold: true, size: 24, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 5 },
    children: [run('Accredited by NBA (UG-CE, EEE, ECE, ME & CSE Programmes) & NAAC A+ Grade', { size: 19 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 5 },
    children: [run('(Affiliated to JNTU Hyderabad and Approved by the AICTE, New Delhi)', { size: 19 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 15 },
    children: [run('NARSAMPET, WARANGAL-506331, TELANGANA, INDIA', { size: 20 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 10 },
    children: [run('DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', { bold: true, size: 24, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 20 },
    children: fs.existsSync(bitsLogoPath) ? [
      new ImageRun({
        data: fs.readFileSync(bitsLogoPath),
        transformation: { width: 75, height: 75 }
      })
    ] : []
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 30 },
    children: [run('CERTIFICATE', { bold: true, size: 28, color: COLOR_CRIMSON })]
  }),
  p([
    run('This is to certify that '),
    run('Kathula Aishwarya (23C31A6746), Bura Alekhya (23C31A6719), Ganaparapu Sahan (23C31A6733)', { bold: true, color: COLOR_BLUE }),
    run(' and '),
    run('Enakonda Vishnuvardhan Reddy (23C31A6730)', { bold: true, color: COLOR_BLUE }),
    run(' of B.Tech IV-II have satisfactorily completed the Major Project work entitled '),
    run('“VIBE-CUTS (REEL): AI-POWERED AUTOMATED HIGHLIGHT REEL GENERATION AND BEAT-SYNCED VIDEO EDITING SYSTEM”', { bold: true }),
    run(', as part of curriculum in Computer Science & Engineering (Data Science) during academic year 2026-2027.')
  ], { firstLine: true }),
  p('The results embodied in this report have not been submitted to any other University or Institute for the award of any degree or diploma.', { firstLine: true, before: 60 }),
  new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
            children: [
              new Paragraph({ spacing: { before: 250, after: 10 }, children: [run('External Examiner', { bold: true, color: COLOR_CRIMSON, size: 24 })] }),
              new Paragraph({ spacing: { before: 10, after: 10 }, children: [run('_______________________', { size: 24 })] })
            ]
          }),
          new TableCell({
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
            children: [
              new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 250, after: 10 }, children: [run('Guide & Head', { bold: true, color: COLOR_CRIMSON, size: 24 })] }),
              new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 10, after: 5 }, children: [run('Mr. K. VIJAY KUMAR', { bold: true, size: 25 })] }),
              new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 5, after: 5 }, children: [run('Assistant Professor', { size: 23 })] }),
              new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 5, after: 10 }, children: [run('Department of CSE (Data Science)', { size: 23 })] })
            ]
          })
        ]
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 10 },
    children: [run('Dr. V. S. HARIHARAN', { bold: true, size: 25, color: COLOR_GREEN })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 10 },
    children: [run('Principal, Balaji Institute of Technology & Science', { size: 23 })]
  }),
  new Paragraph({ children: [new PageBreak()] })
);

// 4. Acknowledgement Page
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [run('ACKNOWLEDGEMENT', { bold: true, size: 28, color: COLOR_BLUE })]
  }),
  p([
    run('We would like to express our heartfelt gratitude to our esteemed Project Guide '),
    run('Mr. K. Vijay Kumar', { bold: true, color: COLOR_CRIMSON }),
    run(', Assistant Professor, Department of CSE (Data Science), and Head of Department '),
    run('Dr. M. Sridhar', { bold: true, color: COLOR_CRIMSON }),
    run(', whose vast knowledge, insightful suggestions, constant motivation, and continuous supervision have inspired us throughout the course of this major project. Their guidance has provided critical direction in resolving complex architectural challenges in client-side WebAssembly video processing and real-time audio digital signal processing.')
  ], { firstLine: true }),
  p('We extend our sincere thanks to our respected Principal, Dr. V. S. Hariharan, for providing excellent computational infrastructure, laboratory facilities, and an encouraging academic environment that enabled us to conceptualize, design, and implement this project successfully.', { firstLine: true }),
  p('We also express our deepest gratitude to all the senior faculty members, project coordinators, and evaluation committee members of the Department of Computer Science & Engineering (Data Science) for their constructive critiques and valuable feedback during our progressive seminar presentations. Our heartfelt appreciation goes to the laboratory technical staff for their technical assistance whenever needed.', { firstLine: true }),
  p('Special thanks and love are due to our parents and family members for their unconditional sacrifices, boundless patience, and continuous moral support throughout our undergraduate education. Finally, we convey our sincere gratitude to our peers, fellow researchers, and well-wishers for their stimulating discussions, collaborative spirit, and encouragement.', { firstLine: true }),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    spacing: { before: 180, after: 40 },
    children: [
      run('Kathula Aishwarya (23C31A6746)\nBura Alekhya (23C31A6719)\nGanaparapu Sahan (23C31A6733)\nEnakonda Vishnuvardhan Reddy (23C31A6730)', {
        bold: true,
        size: 24
      })
    ]
  }),
  new Paragraph({ children: [new PageBreak()] })
);

// 5. Abstract Page
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [run('ABSTRACT', { bold: true, size: 28, color: COLOR_CRIMSON })]
  }),
  p('The exponential growth of mobile-first vertical video formats (9:16 aspect ratio) across platforms such as Instagram Reels, YouTube Shorts, TikTok, and Snapchat Spotlight has fundamentally transformed digital content consumption. In this micro-attention digital economy, content engagement is heavily dictated by pacing, rhythmic energy, and multimodal visual dynamics. Audiences consistently demonstrate up to 3.2 times greater retention when video cuts, zooms, and dynamic transitions are tightly synchronized with musical downbeats and rhythmic transients. However, converting raw, multi-gigabyte unedited video footage into aesthetically compelling, beat-synchronized highlight montages requires extensive manual editing skills, specialized desktop software proficiency, and significant time investment (often 2 to 4 hours per 30-second reel). Conversely, commercial cloud-based automated editing platforms introduce severe user privacy vulnerabilities, high server subscription fees, long cloud rendering queues, and excessive bandwidth consumption during multi-gigabyte video uploads.', { firstLine: true }),
  p([
    run('To overcome these fundamental industry bottlenecks, this project presents '),
    run('Vibe-Cuts (Reel)', { bold: true }),
    run(': an intelligent, client-first, privacy-preserving automated video editing and beat-synchronized highlight reel generation system that operates entirely inside modern client web browsers. Vibe-Cuts pioneers a decentralized edge-computing architecture built upon three core technological pillars: client-side WebAssembly video rendering utilizing @ffmpeg/ffmpeg compiled with WORKERFS zero-copy memory mounting; real-time audio digital signal processing using the HTML5 Web Audio API with a second-order biquad lowpass filter (<150 Hz) and moving-window RMS energy thresholding to extract kick-drum transients within 12ms accuracy; and procedural filtergraph compilation that mathematically synchronizes punch-in zooms, chromatic RGB glitches, exposure flashbangs, and kinetic typography precisely to beat intervals.')
  ], { firstLine: true }),
  p('In addition, an optional lightweight Python FastAPI microservice integrates OpenAI\'s Whisper Automatic Speech Recognition (ASR) model for timestamped subtitle synthesis and Google MediaPipe Face Detection for dynamic 9:16 saliency reframing. Experimental benchmarks indicate that Vibe-Cuts completes end-to-end rendering in sub-30-second execution times for standard 15–30 second social reels, delivers 100% data privacy sovereignty, maintains a constant browser memory footprint below 230 MB, and requires zero remote cloud GPU infrastructure.', { firstLine: true }),
  p([
    run('Keywords: ', { bold: true, color: COLOR_CRIMSON }),
    run('Automated Highlight Reel Generation, Beat Synchronization, WebAssembly FFmpeg, Web Audio API, Client-Side Media Processing, Digital Signal Processing, Procedural VFX, Kinetic Typography, OpenAI Whisper, MediaPipe Face Tracking, Edge Computing.')
  ], { before: 100 }),
  new Paragraph({ children: [new PageBreak()] })
);

// 6. Table of Contents
// Dynamic/Calibrated Table of Contents rows
let tocRows = [
  ['1', 'INTRODUCTION', '1'],
  ['', '1.1 Overview and Background', '1'],
  ['', '1.2 Problem Definition and Limitations of Existing Solutions', '1'],
  ['', '1.3 Objectives of the Project', '2'],
  ['', '1.4 Scope and Feasibility of the Project', '3'],
  ['', '1.5 Organization of the Report', '3'],
  ['2', 'LITERATURE SURVEY / REVIEW', '5'],
  ['', '2.1 Theoretical Foundations of Audio-Visual Beat Synchronization', '5'],
  ['', '2.2 Survey of Existing Automated Video Editing Frameworks', '5'],
  ['', '2.3 Evolution of Web Computing: WebAssembly and Client-Side Media Processing', '6'],
  ['', '2.4 Deep Learning in Speech Recognition and Computer Vision', '7'],
  ['', '2.5 Comparative Literature Survey & Research Gap Analysis', '7'],
  ['3', 'SYSTEM ANALYSIS', '9'],
  ['', '3.1 Introduction', '9'],
  ['', '3.2 Existing System Analysis', '9'],
  ['', '3.3 Proposed System: The Client-First Decentralized Paradigm', '9'],
  ['', '3.4 Feasibility Study', '10'],
  ['', '3.5 System Architecture', '11'],
  ['', '3.6 System Requirements Specification (SRS)', '11'],
  ['', '3.6.1 Functional Requirements', '11'],
  ['', '3.6.2 Non-Functional Requirements', '13'],
  ['', '3.6.3 Hardware Requirements', '14'],
  ['', '3.6.4 Software Requirements', '14'],
  ['4', 'SYSTEM DESIGN', '16'],
  ['', '4.1 Architectural Design Principles & Design Patterns', '16'],
  ['', '4.2 Comprehensive UML Modeling', '16'],
  ['', '4.2.1 Use Case Diagram & Specifications', '16'],
  ['', '4.2.2 Class Diagram & Structural Domain Model', '17'],
  ['', '4.2.3 Sequence Diagram', '18'],
  ['', '4.2.4 Activity Diagram', '18'],
  ['', '4.2.5 State Machine Diagram', '18'],
  ['', '4.2.6 Component & Deployment Modeling', '19'],
  ['', '4.3 Data Flow Modeling (DFD Level 0, Level 1 & Level 2)', '19'],
  ['', '4.4 Mathematical Formulations & Audio Digital Signal Processing', '19'],
  ['', '4.4.1 Second-Order Lowpass Biquad Filter Transfer Function', '19'],
  ['', '4.4.2 Moving-Window RMS & Adaptive Peak Picking Algorithm', '20'],
  ['', '4.5 Dual-Pass FFmpeg WebAssembly Memory Architecture', '20'],
  ['', '4.6 Procedural VFX Mathematical Expressions & Filtergraph Compiler', '21'],
  ['', '4.7 Speech-to-Text Whisper Subtitle Engine', '21'],
  ['', '4.8 MediaPipe Dynamic 9:16 Face-Tracking Reframing', '21'],
  ['5', 'IMPLEMENTATION', '23'],
  ['', '5.1 Technology Stack & Architectural Setup', '23'],
  ['', '5.2 Core Implementation Algorithms & Production Code', '23'],
  ['', '5.2.1 Client-Side Audio Beat & Transient Extraction Algorithm', '23'],
  ['', '5.2.2 Procedural FFmpeg Filtergraph Construction Algorithm', '24'],
  ['', '5.2.3 Dual-Pass WASM Rendering & Worker Execution', '25'],
  ['', '5.2.4 FastAPI Microservice for Subtitle Extraction', '25'],
  ['', '5.2.5 MediaPipe Face Detection & Saliency Horizontal Crop', '25'],
  ['', '5.3 Web UI Component Architecture & Timeline Canvas', '26'],
  ['', '5.4 Cross-Origin Isolation & Security Configuration', '26'],
  ['6', 'TESTING', '27'],
  ['', '6.1 Objectives and Test Strategy', '27'],
  ['', '6.2 Unit Testing', '27'],
  ['', '6.3 Integration Testing', '28'],
  ['', '6.4 Audio Beat Synchronization Validation', '29'],
  ['', '6.5 Whisper ASR Word Error Rate (WER) Evaluation', '29'],
  ['', '6.6 Performance, Memory & Stress Testing', '30'],
  ['', '6.7 Cross-Browser & Cross-Platform Compatibility Matrix', '30'],
  ['7', 'RESULTS AND DISCUSSION', '31'],
  ['', '7.1 Graphical User Interface Walkthrough & Features', '31'],
  ['', '7.1.1 Project Ingestion & Asset Library Dashboard', '31'],
  ['', '7.1.2 HomeScreen & Main Video Studio Editor', '31'],
  ['', '7.1.3 Audio Waveform & Beat Visualizer Interface', '31'],
  ['', '7.1.4 Cinematic VFX & Filter Customization Panel', '31'],
  ['', '7.1.5 Kinetic Captions & Whisper Subtitle Inspector', '32'],
  ['', '7.1.6 WASM Export & Multi-Format Render Panel', '32'],
  ['', '7.2 Experimental Benchmark Results', '32'],
  ['', '7.2.1 Audio Transient Extraction & Beat Peak Alignment Waveform', '32'],
  ['', '7.2.2 Procedural Zoom & Glitch VFX Synchronization Waveform', '32'],
  ['', '7.2.3 Sub-Frame Subtitle Alignment & Word-Level Highlighting', '33'],
  ['', '7.2.4 System Performance Benchmark & Processing Latency Graph', '33'],
  ['', '7.3 Comparative Analysis with Commercial Platforms', '34'],
  ['', '7.4 Architectural Advantages & Technical Merits', '34'],
  ['', '7.5 Practical Industry & Commercial Applications', '35'],
  ['8', 'CONCLUSION AND FUTURE WORK', '36'],
  ['', '8.1 Summary of Stage-I Contributions', '36'],
  ['', '8.2 Practical Engineering Limitations Identified', '36'],
  ['', '8.3 Future Scope & Stage-II Development Roadmap', '36'],
  ['', 'REFERENCES', '38']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 30, after: 100 },
    children: [run('TABLE OF CONTENTS', { bold: true, size: 28, color: COLOR_CRIMSON })]
  }),
  academicTable(['S.NO', 'CONTENTS', 'PAGE NO.'], tocRows, [10, 75, 15]),
  new Paragraph({ children: [new PageBreak()] })
);

// 7. List of Figures
const lofRows = [
  ['3.1', 'Functional Flow Chart of the Automated Highlight & Beat-Synced Generation Process', '11'],
  ['3.2', 'High-Level Client-Server System Architecture of Vibe-Cuts', '11'],
  ['4.1', 'UML Use Case Diagram of the Vibe-Cuts System', '16'],
  ['4.2', 'UML Class Diagram Representing Core System Entities and Operations', '17'],
  ['4.3', 'UML Sequence Diagram for Asynchronous Beat Extraction and Dual-Pass Render', '18'],
  ['4.4', 'UML Activity Diagram Depicting Parallel Multithreaded Processing', '18'],
  ['7.1', 'Project Ingestion & Asset Library Dashboard', '31'],
  ['7.2', 'HomeScreen & Main Video Studio Editor', '31'],
  ['7.3', 'Audio Waveform & Beat Visualizer Interface', '31'],
  ['7.4', 'Cinematic VFX & Filter Customization Panel', '32'],
  ['7.5', 'Kinetic Captions & Whisper Subtitle Inspector', '32'],
  ['7.6', 'WASM Export & Multi-Format Render Panel', '32'],
  ['7.7', 'Audio Transient Extraction & Beat Peak Alignment Waveform', '32'],
  ['7.8', 'Procedural Zoom & Glitch VFX Synchronization Waveform', '33'],
  ['7.9', 'Sub-Frame Subtitle Alignment & Word-Level Highlighting', '33'],
  ['7.10', 'System Performance Benchmark & Processing Latency Graph', '33']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 30, after: 100 },
    children: [run('LIST OF FIGURES', { bold: true, size: 28, color: COLOR_BLUE })]
  }),
  academicTable(['Figure.NO', 'CONTENTS', 'PAGE NO.'], lofRows, [15, 70, 15]),
  new Paragraph({ children: [new PageBreak()] })
);

// 8. List of Tables
const lotRows = [
  ['2.1', 'Comparative Literature Survey of Video Editing Systems', '7'],
  ['3.1', 'Hardware Requirements Specification', '14'],
  ['3.2', 'Software Requirements Specification', '15'],
  ['3.3', 'Functional Requirements Specification Matrix', '11'],
  ['3.4', 'Non-Functional Requirements & Performance Targets', '13'],
  ['4.1', 'Detailed Use Case Specification Matrix', '16'],
  ['4.2', 'Mathematical Filtergraph Transform Mapping Table', '21'],
  ['5.1', 'Software Module Decomposition and Responsibility Distribution', '23'],
  ['5.2', 'In-Browser SharedArrayBuffer Security Header Directives', '26'],
  ['6.1', 'Unit Test Cases Specification and Verification Results', '27'],
  ['6.2', 'System Integration Test Cases and End-to-End Validation', '28'],
  ['6.3', 'Whisper ASR Word Error Rate (WER) Acoustic Evaluation Matrix', '29'],
  ['6.4', 'Cross-Browser and Operating System Compatibility Matrix', '30'],
  ['7.1', 'Comprehensive Commercial Feature Matrix', '34'],
  ['7.2', 'Quantitative Rendering Performance and Latency Benchmarks', '33'],
  ['7.3', 'Memory Footprint Evaluation (WORKERFS vs MEMFS Linear Memory)', '34']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 30, after: 100 },
    children: [run('LIST OF TABLES', { bold: true, size: 28, color: COLOR_GREEN })]
  }),
  academicTable(['Table.NO', 'CONTENTS', 'PAGE NO.'], lotRows, [15, 70, 15]),
  new Paragraph({ children: [new PageBreak()] })
);

// 9. List of Abbreviations
const loAbbrRows = [
  ['AI', 'Artificial Intelligence'],
  ['API', 'Application Programming Interface'],
  ['ASR', 'Automatic Speech Recognition'],
  ['Biquad', 'Biquadratic Digital Filter (Second-Order IIR Filter)'],
  ['BPM', 'Beats Per Minute (Musical Tempo Measurement)'],
  ['CCPA', 'California Consumer Privacy Act'],
  ['COOP', 'Cross-Origin-Opener-Policy (Security Header)'],
  ['COEP', 'Cross-Origin-Embedder-Policy (Security Header)'],
  ['CPU', 'Central Processing Unit'],
  ['CSS', 'Cascading Style Sheets'],
  ['DAW', 'Digital Audio Workstation'],
  ['DFD', 'Data Flow Diagram'],
  ['DOM', 'Document Object Model'],
  ['DSP', 'Digital Signal Processing'],
  ['EDM', 'Electronic Dance Music'],
  ['EMA', 'Exponential Moving Average'],
  ['FFmpeg', 'Fast Forward MPEG Multimedia Processing Framework'],
  ['FIFO', 'First-In, First-Out Memory Buffer'],
  ['FPS', 'Frames Per Second'],
  ['GDPR', 'General Data Protection Regulation (EU 2016/679)'],
  ['GPU', 'Graphics Processing Unit'],
  ['GUI', 'Graphical User Interface'],
  ['HTML5', 'HyperText Markup Language 5'],
  ['IEEE', 'Institute of Electrical and Electronics Engineers'],
  ['I/O', 'Input / Output'],
  ['JS', 'JavaScript'],
  ['JSON', 'JavaScript Object Notation'],
  ['MEMFS', 'In-Memory Virtual File System (Emscripten)'],
  ['ML', 'Machine Learning'],
  ['MP4', 'MPEG-4 Part 14 Video Container'],
  ['NLE', 'Non-Linear Editing System'],
  ['ODF', 'Onset Detection Function'],
  ['OS', 'Operating System'],
  ['PCM', 'Pulse Code Modulation (Uncompressed Audio Format)'],
  ['POSIX', 'Portable Operating System Interface'],
  ['QA', 'Quality Assurance'],
  ['RGB', 'Red Green Blue Color Model'],
  ['RMS', 'Root Mean Square Energy Envelope'],
  ['SAB', 'SharedArrayBuffer'],
  ['SPA', 'Single-Page Application'],
  ['SRS', 'Software Requirements Specification'],
  ['STFT', 'Short-Time Fourier Transform'],
  ['TS', 'TypeScript'],
  ['UI', 'User Interface'],
  ['UML', 'Unified Modeling Language'],
  ['URI', 'Uniform Resource Identifier'],
  ['URL', 'Uniform Resource Locator'],
  ['UX', 'User Experience'],
  ['VFX', 'Visual Effects'],
  ['VFS', 'Virtual File System'],
  ['WASM', 'WebAssembly Binary Instruction Format'],
  ['WER', 'Word Error Rate (Acoustic Evaluation Metric)'],
  ['WORKERFS', 'Web Worker File System (Zero-Copy Blob Access)']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 30, after: 100 },
    children: [run('LIST OF ABBREVIATIONS', { bold: true, size: 28, color: COLOR_CRIMSON })]
  }),
  academicTable(['ABBREVIATION', 'FULL FORM / DESCRIPTION'], loAbbrRows, [25, 75]),
  new Paragraph({ children: [new PageBreak()] })
);

// -------------------------------------------------------------------------
// SECTION 2: BODY CHAPTERS (PARSING PROJECT_REPORT_DOCUMENTATION.MD)
// -------------------------------------------------------------------------
const bodyElements = [];
const fullMarkdown = fs.readFileSync(mdPath, 'utf8');

// Parse markdown starting from CHAPTER 1
const bodyMarkdown = fullMarkdown.substring(fullMarkdown.indexOf('# CHAPTER 1: INTRODUCTION'));
const lines = bodyMarkdown.split('\n');

let inCode = false;
let codeBuffer = '';
let inTable = false;
let tableHeaders = [];
let tableRowsData = [];

// Mapping figure markers to images
const figureImageMap = {
  '3.1': { file: 'figure_0.png', w: 480, h: 165, cap: 'Figure 3.1: Functional Flow Chart of the Automated Highlight & Beat-Synced Generation Process' },
  '3.2': { file: 'figure_1.png', w: 480, h: 155, cap: 'Figure 3.2: High-Level Client-Server System Architecture of Vibe-Cuts' },
  '4.1': { file: 'figure_2.png', w: 480, h: 180, cap: 'Figure 4.1: UML Use Case Diagram of the Vibe-Cuts System' },
  '4.2': { file: 'figure_3.png', w: 480, h: 175, cap: 'Figure 4.2: UML Class Diagram Representing Core System Entities and Operations' },
  '4.3': { file: 'figure_4.png', w: 480, h: 175, cap: 'Figure 4.3: UML Sequence Diagram for Asynchronous Beat Extraction and Dual-Pass Render' },
  '4.4': { file: 'figure_5.png', w: 480, h: 175, cap: 'Figure 4.4: UML Activity Diagram Depicting Parallel Multithreaded Processing' },
  '7.1': { file: 'figure_6.png', w: 480, h: 110, cap: 'Figure 7.1: Project Ingestion & Asset Library Dashboard' },
  '7.2': { file: 'figure_7.png', w: 480, h: 110, cap: 'Figure 7.2: HomeScreen & Main Video Studio Editor' },
  '7.3': { file: 'figure_8.png', w: 480, h: 110, cap: 'Figure 7.3: Audio Waveform & Beat Visualizer Interface' },
  '7.4': { file: 'figure_9.png', w: 480, h: 110, cap: 'Figure 7.4: Cinematic VFX & Filter Customization Panel' },
  '7.5': { file: 'figure_10.png', w: 480, h: 110, cap: 'Figure 7.5: Kinetic Captions & Whisper Subtitle Inspector' },
  '7.6': { file: 'figure_11.png', w: 480, h: 110, cap: 'Figure 7.6: WASM Export & Multi-Format Render Panel' },
  '7.7': { file: 'figure_12.png', w: 480, h: 95, cap: 'Figure 7.7: Audio Transient Extraction & Beat Peak Alignment Waveform' },
  '7.8': { file: 'figure_13.png', w: 480, h: 95, cap: 'Figure 7.8: Procedural Zoom & Glitch VFX Synchronization Waveform' },
  '7.9': { file: 'figure_14.png', w: 480, h: 95, cap: 'Figure 7.9: Sub-Frame Subtitle Alignment & Word-Level Highlighting' },
  '7.10': { file: 'figure_15.png', w: 480, h: 95, cap: 'Figure 7.10: System Performance Benchmark & Processing Latency Graph' }
};

for (let i = 0; i < lines.length; i++) {
  let line = lines[i].trimEnd();

  // Code Block
  if (line.startsWith('```')) {
    if (!inCode) {
      inCode = true;
      codeBuffer = '';
    } else {
      inCode = false;
      bodyElements.push(codeBlock(codeBuffer));
    }
    continue;
  }
  if (inCode) {
    codeBuffer += (codeBuffer ? '\n' : '') + line;
    continue;
  }

  // Markdown Tables
  if (line.startsWith('|')) {
    if (!inTable) {
      inTable = true;
      tableHeaders = [];
      tableRowsData = [];
    }
    if (line.includes('---')) {
      continue;
    }
    const cells = line.split('|').filter((c, idx, arr) => idx > 0 && idx < arr.length - 1).map(c => c.trim());
    if (tableHeaders.length === 0) {
      tableHeaders = cells;
    } else {
      tableRowsData.push(cells);
    }
    continue;
  } else if (inTable) {
    inTable = false;
    const colCount = tableHeaders.length || 1;
    const colWidth = Math.floor(100 / colCount);
    const colWidths = new Array(colCount).fill(colWidth);
    bodyElements.push(academicTable(tableHeaders, tableRowsData, colWidths));
  }

  // Figure Matchers: [Figure X.Y: Caption]
  const figMatch = line.match(/^\[Figure\s+([0-9\.]+):/);
  if (figMatch) {
    const figNum = figMatch[1];
    if (figureImageMap[figNum]) {
      const info = figureImageMap[figNum];
      bodyElements.push(...imageFigure(path.join(diagDir, info.file), info.w, info.h, info.cap));
      continue;
    }
  }

  // Headings
  if (line.startsWith('# ')) {
    const title = line.replace('# ', '').trim();
    bodyElements.push(chapterHeading(title));
  } else if (line.startsWith('## ')) {
    const sec = line.replace('## ', '').trim();
    bodyElements.push(subsectionHeading(sec));
  } else if (line.startsWith('### ')) {
    const subsec = line.replace('### ', '').trim();
    bodyElements.push(subsubsectionHeading(subsec));
  } else if (line.startsWith('**Table ')) {
    // Table title placed ABOVE the table as per guideline
    bodyElements.push(tableTitle(line.replace(/\*\*/g, '')));
  } else if (/^\d+\.\s+[A-Z]/.test(line) || /^\d+\.\s+\*/.test(line) || /^\[\d+\]\s+[A-Z]/.test(line)) {
    // References (11 pt, IEEE format, justified with hanging indent)
    bodyElements.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED,
      indent: { left: 504, hanging: 504 },
      spacing: { line: 360, before: 60, after: 60 },
      children: parseFormattedText(line, 22) // 11pt
    }));
  } else if (line.startsWith('- ') || line.startsWith('* ')) {
    bodyElements.push(p([run('• ', { bold: true }), ...parseFormattedText(line.replace(/^[-*]\s+/, ''), 24)], { indent: { left: 504 }, before: 20, after: 30 }));
  } else if (line.trim() === '---') {
    // Divider
  } else if (line.trim() === '') {
    // Blank line
  } else {
    bodyElements.push(p(line, { firstLine: true }));
  }
}

// Ensure last table is flushed if file ends with table
if (inTable) {
  const colCount = tableHeaders.length || 1;
  const colWidth = Math.floor(100 / colCount);
  const colWidths = new Array(colCount).fill(colWidth);
  bodyElements.push(academicTable(tableHeaders, tableRowsData, colWidths));
}

// -------------------------------------------------------------------------
// ASSEMBLE DOCUMENT (A4, EXACT MARGINS, DUAL-SECTION PAGINATION)
// -------------------------------------------------------------------------
const a4PageProps = {
  size: {
    width: 11906,  // A4 width in twips (210mm)
    height: 16838  // A4 height in twips (297mm)
  },
  margin: {
    top: 1440,    // 1" = 1440 twips
    bottom: 1440, // 1" = 1440 twips
    left: 1800,   // 1.25" = 1800 twips
    right: 1440   // 1" = 1440 twips
  }
};

const doc = new Document({
  title: 'VIBE-CUTS (REEL) Major Project Report',
  description: 'Major Project Report - Balaji Institute of Technology & Science',
  sections: [
    {
      properties: {
        page: {
          ...a4PageProps,
          pageNumbers: { start: 1, formatType: NumberFormat.LOWER_ROMAN }
        }
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT_NAME, size: 22 })]
            })
          ]
        })
      },
      children: prelimElements
    },
    {
      properties: {
        page: {
          ...a4PageProps,
          pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL }
        }
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT_NAME, size: 22 })]
            })
          ]
        })
      },
      children: bodyElements
    }
  ]
});

const outDocxPath = path.join(__dirname, 'Project_Report_Documentation.docx');

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outDocxPath, buffer);
  console.log(`Document saved successfully to ${outDocxPath}`);
  console.log(`File size: ${(buffer.length / 1024).toFixed(2)} KB`);
}).catch(err => {
  console.error('Error generating document:', err);
});
