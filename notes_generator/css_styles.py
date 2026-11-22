"""
CSS Stylesheet for Computer Networks Complete Study Notes Textbook PDF.
"""

CSS_CONTENT = """
@page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {
        content: counter(page);
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        font-size: 9pt;
        color: #64748b;
    }
    @bottom-left {
        content: "Computer Networks (BCS502) - Comprehensive Study Notes";
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #94a3b8;
    }
}

@page:first {
    margin-top: 0;
    @bottom-center { content: ""; }
    @bottom-left { content: ""; }
}

* {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}

body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}

/* Headings */
h1, h2, h3, h4, h5 {
    color: #0f2b5c;
    font-weight: 700;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
    line-height: 1.3;
}

h1.doc-title {
    font-size: 26pt;
    text-align: center;
    color: #0f2b5c;
    margin-top: 10px;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.doc-subtitle {
    font-size: 13pt;
    text-align: center;
    color: #0284c7;
    font-weight: 600;
    margin-bottom: 25px;
}

h1.module-title {
    font-size: 15pt;
    background: linear-gradient(135deg, #0f2b5c 0%, #1e40af 100%);
    color: #ffffff;
    padding: 10px 14px;
    border-radius: 4px;
    margin-top: 25px;
    margin-bottom: 16px;
    page-break-before: always;
    display: flex;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

h2.section-title {
    font-size: 12pt;
    color: #0f2b5c;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 10px;
    page-break-after: avoid;
}

h3.sub-section-title {
    font-size: 10.5pt;
    color: #1e40af;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}

h4 {
    font-size: 10pt;
    color: #334155;
    margin-top: 10px;
    margin-bottom: 4px;
    page-break-after: avoid;
}

p {
    margin-top: 0;
    margin-bottom: 8px;
    text-align: justify;
}

ul, ol {
    margin-top: 4px;
    margin-bottom: 10px;
    padding-left: 22px;
}

li {
    margin-bottom: 4px;
}

/* Code and Pre */
code {
    font-family: 'Consolas', 'Menlo', 'Courier New', monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    color: #b91c1c;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
}

pre {
    font-family: 'Consolas', monospace;
    font-size: 8.5pt;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 10px;
    margin: 8px 0;
    overflow-x: auto;
    page-break-inside: avoid;
}

/* Callouts and Boxes */
.eli5-box {
    background-color: #fefce8;
    border-left: 4.5px solid #eab308;
    border-radius: 4px;
    padding: 10px 14px;
    margin: 10px 0;
    page-break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.eli5-box .title {
    font-weight: 700;
    color: #854d0e;
    font-size: 9.5pt;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.key-point {
    background-color: #f0fdf4;
    border-left: 4.5px solid #22c55e;
    border-radius: 4px;
    padding: 9px 13px;
    margin: 10px 0;
    page-break-inside: avoid;
}

.key-point .title {
    font-weight: 700;
    color: #15803d;
    font-size: 9.5pt;
    margin-bottom: 4px;
}

.exam-tip {
    background-color: #eff6ff;
    border-left: 4.5px solid #3b82f6;
    border-radius: 4px;
    padding: 9px 13px;
    margin: 10px 0;
    page-break-inside: avoid;
}

.exam-tip .title {
    font-weight: 700;
    color: #1d4ed8;
    font-size: 9.5pt;
    margin-bottom: 4px;
}

.formula-box {
    background-color: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-left: 4.5px solid #64748b;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 8px 0;
    font-family: 'Consolas', monospace;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9pt;
    page-break-inside: avoid;
    background-color: #ffffff;
}

table th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 7px 10px;
    border: 1px solid #1e3a8a;
}

table td {
    padding: 6px 10px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
}

table tr:nth-child(even) {
    background-color: #f8fafc;
}

/* Diagrams */
.diagram-container {
    text-align: center;
    margin: 14px 0;
    page-break-inside: avoid;
}

.diagram-container svg {
    max-width: 100%;
    height: auto;
    filter: drop-shadow(0px 1px 2px rgba(0,0,0,0.06));
}

.diagram-caption {
    font-size: 8.5pt;
    font-style: italic;
    color: #475569;
    margin-top: 5px;
    font-weight: 500;
}

/* Metadata Block on Cover */
.course-meta-table {
    width: 100%;
    margin-bottom: 20px;
    border: 1px solid #cbd5e1;
    font-size: 9pt;
}

.course-meta-table td {
    padding: 6px 10px;
    border: 1px solid #cbd5e1;
}

.course-meta-table td.header-cell {
    background-color: #0f2b5c;
    color: #ffffff;
    font-weight: 700;
}

.toc-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 14px 18px;
    margin: 15px 0 25px 0;
}

.toc-card h3 {
    margin-top: 0;
    color: #0f2b5c;
    border-bottom: 2px solid #cbd5e1;
    padding-bottom: 4px;
}

.toc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    font-size: 9pt;
}

.page-break {
    page-break-before: always;
}

.highlight {
    background-color: #fef08a;
    padding: 1px 3px;
    border-radius: 2px;
}
"""
