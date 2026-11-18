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
console.log('Generating Expanded Major Project Report (.docx)');
console.log('Target: EXACTLY 80 Pages | Conforming to Template 2');
console.log('Balaji Institute of Technology & Science (Autonomous)');
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
      after: options.after !== undefined ? options.after : 92
    },
    children: children
  });
}

function chapterHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    pageBreakBefore: true,
    spacing: { before: 240, after: 360, line: 360 },
    children: [
      new TextRun({
        text: title.toUpperCase(),
        font: FONT_NAME,
        size: 28, // 14pt Bold Uppercase
        bold: true,
        color: COLOR_BLACK
      })
    ]
  });
}

function subsectionHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 280, after: 140, line: 360 },
    children: [
      new TextRun({
        text: title,
        font: FONT_NAME,
        size: 24, // 12pt Bold
        bold: true,
        color: COLOR_BLACK
      })
    ]
  });
}

function subsubsectionHeading(title) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 220, after: 100, line: 360 },
    children: [
      new TextRun({
        text: title,
        font: FONT_NAME,
        size: 24, // 12pt Bold Italic
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
      spacing: { before: 40, after: 140 },
      children: [
        new TextRun({
          text: captionText,
          font: FONT_NAME,
          size: 22, // 11pt Italic
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
            spacing: { before: 20, after: 20 },
            children: parseFormattedText(cellText, 18) // 10pt
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

// -------------------------------------------------------------------------
// SECTION 1: PRELIMINARY PAGES (i to x, EXACTLY 10 PAGES)
// -------------------------------------------------------------------------
const prelimElements = [];

// 1. Outer Cover Page (Page i)
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 30 },
    children: [run('A MAJOR PROJECT REPORT', { bold: true, size: 32 })] // 16pt Bold
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 40 },
    children: [run('ON', { bold: true, size: 28 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 80 },
    children: [
      run('VIBE-CUTS (REEL): AI-POWERED AUTOMATED HIGHLIGHT REEL GENERATION AND BEAT-SYNCED VIDEO EDITING SYSTEM', {
        bold: true,
        size: 32, // 16pt Bold Uppercase
        color: COLOR_CRIMSON
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 20 },
    children: [run('Submitted in Partial Fulfilment of the Requirements for', { size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 30 },
    children: [run('The Award of Degree of', { size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 15 },
    children: [run('BACHELOR OF TECHNOLOGY', { bold: true, size: 30 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 15 },
    children: [run('IN', { bold: true, size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 60 },
    children: [run('COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', { bold: true, size: 26, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 30, after: 20 },
    children: [run('By', { bold: true, size: 24 })]
  }),
  new Table({
    width: { size: 75, type: WidthType.PERCENTAGE },
    alignment: AlignmentType.CENTER,
    rows: [
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('KATHULA AISHWARYA', { bold: true, size: 23 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6746)', { bold: true, size: 23 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('BURA ALEKHYA', { bold: true, size: 23 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6719)', { bold: true, size: 23 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('GANAPARAPU SAHAN', { bold: true, size: 23 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6733)', { bold: true, size: 23 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('ENAKONDA VISHNUVARDHAN REDDY', { bold: true, size: 23 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6730)', { bold: true, size: 23 })] })] })
        ]
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 50, after: 15 },
    children: [run('UNDER THE GUIDANCE OF', { bold: true, size: 23 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 10 },
    children: [run('Mr. K. VIJAY KUMAR', { bold: true, size: 26, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 40 },
    children: [run('Assistant Professor, Department of CSE (Data Science)', { bold: true, size: 21 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 20 },
    children: fs.existsSync(bitsLogoPath) ? [
      new ImageRun({
        data: fs.readFileSync(bitsLogoPath),
        transformation: { width: 85, height: 85 }
      })
    ] : []
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 10 },
    children: [run('DEPARTMENT OF CSE (DATA SCIENCE)', { bold: true, size: 24, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 10 },
    children: [run('BALAJI INSTITUTE OF TECHNOLOGY AND SCIENCE', { bold: true, size: 26, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 10 },
    children: [run('(AUTONOMOUS)', { bold: true, size: 23, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 5 },
    children: [run('Accredited by NBA & NAAC A+ Grade | Affiliated to JNTUH, Approved by AICTE', { bold: true, size: 17 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 10 },
    children: [run('NARSAMPET, WARANGAL – 506 331, TELANGANA', { bold: true, size: 19 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 40 },
    children: [run('2026-2027', { bold: true, size: 23 })]
  }),
  new Paragraph({ children: [new PageBreak()] })
);

// 2. Inner Title Page (Page ii)
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 25 },
    children: [run('A MAJOR PROJECT REPORT', { bold: true, size: 30 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 30 },
    children: [run('ON', { bold: true, size: 24 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 70 },
    children: [
      run('VIBE-CUTS (REEL): AI-POWERED AUTOMATED HIGHLIGHT REEL GENERATION AND BEAT-SYNCED VIDEO EDITING SYSTEM', {
        bold: true,
        size: 30,
        color: COLOR_CRIMSON
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 30, after: 15 },
    children: [run('Submitted in Partial Fulfilment of the Requirements for', { size: 23 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 25 },
    children: [run('The Award of Degree of', { size: 23 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 15 },
    children: [run('BACHELOR OF TECHNOLOGY', { bold: true, size: 28 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 15 },
    children: [run('IN', { bold: true, size: 23 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 50 },
    children: [run('COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', { bold: true, size: 24, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 25, after: 15 },
    children: [run('Submitted by:', { bold: true, size: 23 })]
  }),
  new Table({
    width: { size: 75, type: WidthType.PERCENTAGE },
    alignment: AlignmentType.CENTER,
    rows: [
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('KATHULA AISHWARYA', { bold: true, size: 22 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6746)', { bold: true, size: 22 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('BURA ALEKHYA', { bold: true, size: 22 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6719)', { bold: true, size: 22 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('GANAPARAPU SAHAN', { bold: true, size: 22 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6733)', { bold: true, size: 22 })] })] })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.LEFT, children: [run('ENAKONDA VISHNUVARDHAN REDDY', { bold: true, size: 22 })] })] }),
          new TableCell({ borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run('(23C31A6730)', { bold: true, size: 22 })] })] })
        ]
      })
    ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 10 },
    children: [run('Under the Esteemed Guidance of:', { bold: true, size: 22 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 5 },
    children: [run('Mr. K. VIJAY KUMAR', { bold: true, size: 24, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 30 },
    children: [run('Assistant Professor, Department of CSE (Data Science)', { size: 21 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 10 },
    children: [run('DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', { bold: true, size: 22, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 10, after: 5 },
    children: [run('BALAJI INSTITUTE OF TECHNOLOGY AND SCIENCE (AUTONOMOUS)', { bold: true, size: 24, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 5 },
    children: [run('Narsampet, Warangal – 506 331, Telangana, India', { size: 20 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 30 },
    children: [run('Academic Year: 2026-2027', { bold: true, size: 22 })]
  }),
  new Paragraph({ children: [new PageBreak()] })
);

// 3. Certificate Page (Page iii)
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 15 },
    children: [run('BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE', { bold: true, size: 26, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 15 },
    children: [run('(AUTONOMOUS)', { bold: true, size: 24, color: COLOR_CRIMSON })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 5 },
    children: [run('Accredited by NBA (UG-CE, EEE, ECE, ME & CSE Programmes) & NAAC A+ Grade', { size: 18 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 10 },
    children: [run('(Affiliated to JNTU Hyderabad and Approved by the AICTE, New Delhi)', { size: 18 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 15 },
    children: [run('NARSAMPET, WARANGAL-506331.', { size: 19 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 5 },
    children: [run('DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING', { bold: true, size: 22, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 5, after: 20 },
    children: [run('(DATA SCIENCE)', { bold: true, size: 22, color: COLOR_BLUE })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 15, after: 15 },
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
    run(' of the B-Tech IV-II have satisfactorily completed the Major Project work entitled '),
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
              new Paragraph({ spacing: { before: 280, after: 10 }, children: [run('External Examiner', { bold: true, color: COLOR_CRIMSON, size: 23 })] }),
              new Paragraph({ spacing: { before: 10, after: 10 }, children: [run('_______________________', { size: 23 })] })
            ]
          }),
          new TableCell({
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
            children: [
              new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 280, after: 10 }, children: [run('Guide & Head', { bold: true, color: COLOR_CRIMSON, size: 23 })] }),
              new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 10, after: 5 }, children: [run('Mr. K. VIJAY KUMAR', { bold: true, size: 24 })] }),
              new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 5, after: 5 }, children: [run('Assistant Professor', { size: 22 })] }),
              new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 5, after: 10 }, children: [run('Department of CSE (Data Science)', { size: 22 })] })
            ]
          })
        ]
      })
    ]
  }),
  new Paragraph({ children: [new PageBreak()] })
);

// 4. Acknowledgement Page (Page iv)
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [run('ACKNOWLEDGEMENT', { bold: true, size: 28, color: COLOR_BLUE })]
  }),
  p([
    run('We would like to express our heartfelt gratitude to our esteemed Guide '),
    run('Mr. K. Vijay Kumar', { bold: true, color: COLOR_CRIMSON }),
    run(' and Head of Department '),
    run('Dr. M. Sridhar', { bold: true, color: COLOR_CRIMSON }),
    run(', whose vast knowledge, invaluable guidance, and constant motivation have inspired us to achieve milestones we once thought unattainable. His encouragement and support have been a continuous source of inspiration, making our time under his mentorship a truly rewarding experience.')
  ], { firstLine: true }),
  p('We also extend our sincere thanks to all the senior faculty members for their valuable help throughout our course. Our heartfelt thanks also go to the programmers and non-teaching staff of the CSE (Data Science) Department for their assistance whenever needed.', { firstLine: true }),
  p([
    run('We are deeply grateful to our respected Principal, '),
    run('Dr. V. S. Hariharan', { bold: true, color: COLOR_GREEN }),
    run(', for providing us with this wonderful opportunity and for his continuous support in completing our project. We sincerely appreciate the guidance and encouragement given by our Project Coordinator and the Project Evaluation Panels. Their valuable feedback during our project presentations has greatly enhanced our presentation skills and helped us grow professionally.')
  ], { firstLine: true }),
  p('A special note of thanks goes to our beloved parents for their endless support, encouragement, and belief in us throughout our academic journey and beyond. Finally, we are grateful to all our friends and well-wishers for their constant support, encouragement, and motivation.', { firstLine: true }),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    spacing: { before: 140, after: 30 },
    children: [
      run('Kathula Aishwarya (23C31A6746)\nBura Alekhya (23C31A6719)\nGanaparapu Sahan (23C31A6733)\nEnakonda Vishnuvardhan Reddy (23C31A6730)', {
        bold: true,
        size: 23
      })
    ]
  }),
  new Paragraph({ children: [new PageBreak()] })
);

// 5. Abstract Page (Page v)
prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [run('ABSTRACT', { bold: true, size: 28, color: COLOR_CRIMSON })]
  }),
  p('In contemporary digital media ecosystems, short-form vertical video formats (e.g., Instagram Reels, YouTube Shorts, TikTok) dominate audience engagement. However, converting long, unedited footage into high-energy, aesthetically polished, beat-synchronized montages requires intensive manual editing, specialized software proficiency, and substantial computational resources. Conventional cloud-based automated editing platforms introduce severe user privacy vulnerabilities, high server maintenance overheads, bandwidth throttling during multi-gigabyte uploads, and long cloud rendering queues.', { firstLine: true }),
  p([
    run('To overcome these fundamental bottlenecks, this project introduces '),
    run('Vibe-Cuts (Reel)', { bold: true }),
    run(', an intelligent, client-first, privacy-preserving video editing system that automates the generation of cinematic highlight reels directly inside modern web browsers. Vibe-Cuts integrates three core technological pillars: client-side WebAssembly video rendering utilizing @ffmpeg/ffmpeg compiled with WORKERFS zero-copy memory mounting; real-time audio signal processing using the HTML5 Web Audio API with a second-order biquad lowpass filter (<150 Hz) combined with dynamic energy envelope thresholding to extract kick-drum transients within 12ms accuracy; and dynamic procedural filtergraph compilation that synchronizes punch-in zooms, chromatic RGB glitches, flashbangs, and hype typography precisely to beat intervals.')
  ], { firstLine: true }),
  p('In addition, an optional Python FastAPI microservice integrates OpenAI\'s Whisper Automatic Speech Recognition (ASR) model for timestamped subtitle synthesis and MediaPipe Computer Vision for dynamic 9:16 face-centered reframing. Experimental benchmarks indicate that Vibe-Cuts completes end-to-end rendering in sub-30-second execution times for standard 15–30 second social reels, delivers 100% data privacy, and requires zero remote cloud GPU infrastructure.', { firstLine: true }),
  p([
    run('Keywords: ', { bold: true, color: COLOR_CRIMSON }),
    run('Automated Highlight Generation, Beat-Synchronization, WebAssembly FFmpeg, Web Audio API, Client-Side Rendering, Procedural VFX, Kinetic Typography, OpenAI Whisper, MediaPipe Face Tracking, Data Sovereignty.')
  ], { before: 100 }),
  new Paragraph({ children: [new PageBreak()] })
);

// 6. Table of Contents (Pages vi & vii)
let tocRows = [
  ['1', 'INTRODUCTION', '1'],
  ['', '1.1 Overview and Background', '1'],
  ['', '1.2 Problem Definition and Limitations of Existing Solutions', '2'],
  ['', '1.3 Objectives of the Project', '4'],
  ['', '1.4 Scope and Feasibility of the Project', '4'],
  ['', '1.5 Organization of the Report', '5'],
  ['2', 'LITERATURE SURVEY / REVIEW', '7'],
  ['', '2.1 Theoretical Foundations of Audio-Visual Beat Synchronization', '7'],
  ['', '2.2 Survey of Existing Automated Video Editing Frameworks', '8'],
  ['', '2.3 Evolution of Web Computing: WebAssembly and Client-Side Media Processing', '9'],
  ['', '2.4 Deep Learning in Speech Recognition and Computer Vision', '11'],
  ['', '2.5 Comparative Literature Survey & Research Gap Analysis', '12'],
  ['3', 'SYSTEM ANALYSIS', '14'],
  ['', '3.1 Introduction and Analytical Methodology', '14'],
  ['', '3.2 Existing System Analysis', '14'],
  ['', '3.3 Proposed System: The Client-First Decentralized Paradigm', '15'],
  ['', '3.4 Feasibility Study', '17'],
  ['', '3.5 System Architecture', '18'],
  ['', '3.6 System Requirements Specification (SRS)', '20'],
  ['4', 'SYSTEM DESIGN', '24'],
  ['', '4.1 Architectural Design Principles & Design Patterns', '24'],
  ['', '4.2 Comprehensive UML Modeling', '24'],
  ['', '4.3 Data Flow Modeling (DFD Level 0, Level 1 & Level 2)', '29'],
  ['', '4.4 Mathematical Formulations & Audio Digital Signal Processing', '30'],
  ['', '4.5 Dual-Pass FFmpeg WebAssembly Memory Architecture', '33'],
  ['', '4.6 Procedural VFX Mathematical Expressions & Filtergraph Compiler', '34'],
  ['', '4.7 Speech-to-Text Whisper Subtitle Engine', '36'],
  ['', '4.8 MediaPipe Dynamic 9:16 Face-Tracking Reframing', '36'],
  ['5', 'IMPLEMENTATION', '38'],
  ['', '5.1 Technology Stack & Architectural Setup', '38'],
  ['', '5.2 Core Implementation Algorithms & Production Code', '39'],
  ['', '5.3 Web UI Component Architecture & Timeline Canvas', '45'],
  ['', '5.4 Cross-Origin Isolation & Security Configuration', '45'],
  ['6', 'TESTING', '47'],
  ['', '6.1 Objectives and Test Strategy', '47'],
  ['', '6.2 Unit Testing', '47'],
  ['', '6.3 Integration Testing', '49'],
  ['', '6.4 Audio Beat Synchronization Validation', '50'],
  ['', '6.5 Whisper ASR Word Error Rate (WER) Evaluation', '51'],
  ['', '6.6 Performance, Memory & Stress Testing', '52'],
  ['', '6.7 Cross-Browser & Cross-Platform Compatibility Matrix', '52'],
  ['7', 'RESULTS AND DISCUSSION', '54'],
  ['', '7.1 Graphical User Interface Walkthrough & Features', '54'],
  ['', '7.2 Experimental Benchmark Results', '56'],
  ['', '7.3 Comparative Analysis with Commercial Platforms', '59'],
  ['', '7.4 Architectural Advantages & Technical Merits', '59'],
  ['', '7.5 Practical Industry & Commercial Applications', '60'],
  ['8', 'CONCLUSION AND FUTURE WORK', '61'],
  ['', '8.1 Summary of Stage-I Contributions', '61'],
  ['', '8.2 Practical Engineering Limitations Identified', '61'],
  ['', '8.3 Future Scope & Stage-II Development Roadmap', '62'],
  ['', 'REFERENCES', '64'],
  ['', 'APPENDIX A: INSTALLATION & DEVELOPER SETUP GUIDE', '66'],
  ['', 'APPENDIX B: PROCEDURAL FILTERGRAPH TRANSFORM TABLE', '69']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [run('TABLE OF CONTENTS', { bold: true, size: 28 })]
  }),
  academicTable(['S.NO', 'CONTENTS', 'PAGE NO.'], tocRows, [10, 75, 15]),
  new Paragraph({ children: [new PageBreak()] })
);

// 7. List of Figures (Page viii)
const lofRows = [
  ['3.1', 'Functional Flow Chart of the Automated Highlight & Beat-Synced Generation Process', '19'],
  ['3.2', 'High-Level Client-Server System Architecture of Vibe-Cuts', '19'],
  ['4.1', 'UML Use Case Diagram of the Vibe-Cuts System', '25'],
  ['4.2', 'UML Class Diagram Representing Core System Entities and Operations', '26'],
  ['4.3', 'UML Sequence Diagram for Asynchronous Beat Extraction and Dual-Pass Render', '27'],
  ['4.4', 'UML Activity Diagram Depicting Parallel Multithreaded Processing', '28'],
  ['7.1', 'Project Ingestion & Asset Library Dashboard', '54'],
  ['7.2', 'HomeScreen & Main Video Studio Editor', '54'],
  ['7.3', 'Audio Waveform & Beat Visualizer Interface', '55'],
  ['7.4', 'Cinematic VFX & Filter Customization Panel', '55'],
  ['7.5', 'Kinetic Captions & Whisper Subtitle Inspector', '56'],
  ['7.6', 'WASM Export & Multi-Format Render Panel', '56'],
  ['7.7', 'Audio Transient Waveform & Peak Detection Timing', '57'],
  ['7.8', 'Procedural Zoom & Glitch VFX Synchronization Waveform', '57'],
  ['7.9', 'Sub-Frame Subtitle Alignment & Word-Level Highlighting', '57'],
  ['7.10', 'System Performance Benchmark & Processing Latency Graph', '58']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 100 },
    children: [run('LIST OF FIGURES', { bold: true, size: 26, color: COLOR_BLACK })]
  }),
  academicTable(['Figure No.', 'Figure Title', 'Page No.'], lofRows, [18, 68, 14]),
  new Paragraph({ children: [new PageBreak()] })
);

// 8. List of Tables (Page ix)
const lotRows = [
  ['2.1', 'Comparative Literature Survey of Video Editing Systems', '12'],
  ['3.1', 'Hardware Requirements Specification', '22'],
  ['3.2', 'Software Requirements Specification', '23'],
  ['3.3', 'Functional Requirements Specification Matrix', '20'],
  ['3.4', 'Non-Functional Requirements & Performance Targets', '22'],
  ['4.1', 'Detailed Use Case Specification Matrix', '25'],
  ['4.2', 'Mathematical Filtergraph Transform Mapping Table', '34'],
  ['5.1', 'Software Module Decomposition and Responsibility Distribution', '39'],
  ['5.2', 'In-Browser SharedArrayBuffer Security Header Directives', '46'],
  ['6.1', 'Unit Test Cases Specification and Verification Results', '47'],
  ['6.2', 'System Integration Test Cases and End-to-End Validation', '49'],
  ['6.3', 'Whisper ASR Word Error Rate (WER) Acoustic Evaluation Matrix', '51'],
  ['6.4', 'Cross-Browser and Operating System Compatibility Matrix', '53'],
  ['7.1', 'Comprehensive Commercial Feature Matrix', '59'],
  ['7.2', 'Quantitative Rendering Performance and Latency Benchmarks', '58'],
  ['7.3', 'Memory Footprint Evaluation (WORKERFS vs MEMFS Linear Memory)', '58'],
  ['8.1', 'Stage-II Engineering Implementation Roadmap & Milestones', '63'],
  ['B.1', 'Comprehensive Mathematical Transform & Filtergraph Specification Table', '69']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 100 },
    children: [run('LIST OF TABLES', { bold: true, size: 26, color: COLOR_BLACK })]
  }),
  academicTable(['Table No.', 'Table Title', 'Page No.'], lotRows, [18, 68, 14]),
  new Paragraph({ children: [new PageBreak()] })
);

// 9. List of Abbreviations (Page x)
const abbrevRows = [
  ['AI', 'Artificial Intelligence'],
  ['API', 'Application Programming Interface'],
  ['ASR', 'Automatic Speech Recognition'],
  ['Biquad', 'Biquadratic Digital IIR Filter'],
  ['BPM', 'Beats Per Minute'],
  ['CCPA', 'California Consumer Privacy Act'],
  ['COOP', 'Cross-Origin-Opener-Policy'],
  ['COEP', 'Cross-Origin-Embedder-Policy'],
  ['CPU', 'Central Processing Unit'],
  ['CSS', 'Cascading Style Sheets'],
  ['DAW', 'Digital Audio Workstation'],
  ['DFD', 'Data Flow Diagram'],
  ['DOM', 'Document Object Model'],
  ['DSP', 'Digital Signal Processing'],
  ['EMA', 'Exponential Moving Average'],
  ['FFmpeg', 'Fast Forward MPEG Multimedia Framework'],
  ['FIFO', 'First-In, First-Out Memory Buffer'],
  ['FPS', 'Frames Per Second'],
  ['GDPR', 'General Data Protection Regulation'],
  ['GPU', 'Graphics Processing Unit'],
  ['GUI', 'Graphical User Interface'],
  ['HTML5', 'HyperText Markup Language 5'],
  ['IEEE', 'Institute of Electrical and Electronics Engineers'],
  ['MEMFS', 'In-Memory Virtual File System (Emscripten)'],
  ['NLE', 'Non-Linear Editing System'],
  ['ODF', 'Onset Detection Function'],
  ['PCM', 'Pulse Code Modulation'],
  ['POSIX', 'Portable Operating System Interface'],
  ['RMS', 'Root Mean Square Energy Envelope'],
  ['SAB', 'SharedArrayBuffer'],
  ['SRS', 'Software Requirements Specification'],
  ['STFT', 'Short-Time Fourier Transform'],
  ['UML', 'Unified Modeling Language'],
  ['VFX', 'Visual Effects'],
  ['WASM', 'WebAssembly Binary Instruction Format'],
  ['WER', 'Word Error Rate (Acoustic Evaluation Metric)'],
  ['WORKERFS', 'Web Worker File System (Zero-Copy Blob Access)']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 100 },
    children: [run('LIST OF ABBREVIATIONS', { bold: true, size: 26, color: COLOR_BLACK })]
  }),
  academicTable(['Abbreviation', 'Full Form / Description'], abbrevRows, [30, 70])
);

// -------------------------------------------------------------------------
// SECTION 2: BODY CHAPTERS (PARSING PROJECT_REPORT_DOCUMENTATION.MD)
// -------------------------------------------------------------------------
const bodyElements = [];

const fullMarkdown = fs.readFileSync(mdPath, 'utf8');
const bodyMarkdown = fullMarkdown.substring(fullMarkdown.indexOf('# CHAPTER 1: INTRODUCTION'));
const lines = bodyMarkdown.split('\n');

let inCode = false;
let codeBuffer = '';
let inTable = false;
let tableHeaders = [];
let tableRowsData = [];

// Image lookup
const figureImageMap = {
  '3.1': { file: 'figure_0.png', w: 490, h: 190, cap: 'Figure 3.1: Functional Flow Chart of the Automated Highlight & Beat-Synced Generation Process' },
  '3.2': { file: 'figure_1.png', w: 490, h: 170, cap: 'Figure 3.2: High-Level Client-Server System Architecture of Vibe-Cuts' },
  '4.1': { file: 'figure_2.png', w: 470, h: 175, cap: 'Figure 4.1: UML Use Case Diagram of the Vibe-Cuts System' },
  '4.2': { file: 'figure_3.png', w: 470, h: 170, cap: 'Figure 4.2: UML Class Diagram Representing Core System Entities and Operations' },
  '4.3': { file: 'figure_4.png', w: 470, h: 170, cap: 'Figure 4.3: UML Sequence Diagram for Asynchronous Beat Extraction and Dual-Pass Render' },
  '4.4': { file: 'figure_5.png', w: 470, h: 170, cap: 'Figure 4.4: UML Activity Diagram Depicting Parallel Multithreaded Processing' },
  '7.1': { file: 'figure_6.png', w: 470, h: 105, cap: 'Figure 7.1: Project Ingestion & Asset Library Dashboard' },
  '7.2': { file: 'figure_7.png', w: 470, h: 105, cap: 'Figure 7.2: HomeScreen & Main Video Studio Editor' },
  '7.3': { file: 'figure_8.png', w: 470, h: 105, cap: 'Figure 7.3: Audio Waveform & Beat Visualizer Interface' },
  '7.4': { file: 'figure_9.png', w: 470, h: 105, cap: 'Figure 7.4: Cinematic VFX & Filter Customization Panel' },
  '7.5': { file: 'figure_10.png', w: 470, h: 105, cap: 'Figure 7.5: Kinetic Captions & Whisper Subtitle Inspector' },
  '7.6': { file: 'figure_11.png', w: 470, h: 105, cap: 'Figure 7.6: WASM Export & Multi-Format Render Panel' },
  '7.7': { file: 'figure_12.png', w: 470, h: 90, cap: 'Figure 7.7: Audio Transient Waveform & Peak Detection Timing' },
  '7.8': { file: 'figure_13.png', w: 470, h: 90, cap: 'Figure 7.8: Procedural Zoom & Glitch VFX Synchronization Waveform' },
  '7.9': { file: 'figure_14.png', w: 470, h: 90, cap: 'Figure 7.9: Sub-Frame Subtitle Alignment & Word-Level Highlighting' },
  '7.10': { file: 'figure_15.png', w: 470, h: 90, cap: 'Figure 7.10: System Performance Benchmark & Processing Latency Graph' }
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

  // Figure Matchers
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
    // Table title ABOVE the table (Centered, bold) as per Template 2
    bodyElements.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 140, after: 60 },
      children: [new TextRun({ text: line.replace(/\*\*/g, ''), font: FONT_NAME, size: 22, bold: true, color: COLOR_BLACK })]
    }));
  } else if (/^\d+\.\s+[A-Z]/.test(line) || /^\d+\.\s+\*/.test(line)) {
    // References (IEEE Format) - 11pt as per Template 2
    bodyElements.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED,
      indent: { left: 400, hanging: 400 },
      spacing: { line: 260, before: 30, after: 30 },
      children: parseFormattedText(line, 22) // 11pt
    }));
  } else if (line.startsWith('- ') || line.startsWith('* ')) {
    bodyElements.push(p([run('• ', { bold: true }), ...parseFormattedText(line.replace(/^[-*]\s+/, ''), 24)], { indent: { left: 504 }, before: 30, after: 40 }));
  } else if (line.trim() === '---') {
    // Page break or divider
  } else if (line.trim() === '') {
    // Blank
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
  const stats = fs.statSync(outDocxPath);
  console.log('========================================================');
  console.log('SUCCESS! Updated Word Document (.docx) Generated:');
  console.log('Location: ', outDocxPath);
  console.log('Size:     ', stats.size, 'bytes (~' + (stats.size / 1024).toFixed(1) + ' KB)');
  console.log('========================================================');
}).catch(err => {
  console.error('Error generating docx:', err);
  process.exit(1);
});
