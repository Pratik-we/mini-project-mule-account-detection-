"""
Build Script: Compiles all modules and SVGs into a single HTML document and renders it to a textbook PDF using headless Chrome.
"""
import os
import subprocess
import tempfile

from css_styles import CSS_CONTENT
from module1 import get_module_1_content
from module2 import get_module_2_content
from module3 import get_module_3_content
from module4 import get_module_4_content
from module5 import get_module_5_content
from summary_and_questions import get_summary_and_questions_content

def build_html():
    cover_and_meta = """
    <div style="text-align: center; padding-top: 15px;">
        <div style="font-size: 11pt; font-weight: 700; color: #64748b; letter-spacing: 2px; text-transform: uppercase;">VTU 5th Semester &bull; Computer Science & Engineering</div>
        <h1 class="doc-title">COMPUTER NETWORKS</h1>
        <div class="doc-subtitle">Detailed Textbook & Comprehensive Study Notes &mdash; All Modules (1 to 5)</div>
    </div>

    <table class="course-meta-table">
        <tr>
            <td class="header-cell" style="width: 25%;">Course Title</td>
            <td style="width: 25%; font-weight: bold; color: #0f2b5c;">COMPUTER NETWORKS</td>
            <td class="header-cell" style="width: 25%;">Course Code</td>
            <td style="width: 25%; font-weight: bold; color: #0f2b5c;">BCS502</td>
        </tr>
        <tr>
            <td class="header-cell">Semester / Scheme</td>
            <td>5th Semester &bull; 2022/2026 Scheme</td>
            <td class="header-cell">CIE / SEE Marks</td>
            <td>50 / 50 (Total: 100 Marks)</td>
        </tr>
        <tr>
            <td class="header-cell">Credits / Hours</td>
            <td>04 Credits &bull; 40 Hours Theory + Lab</td>
            <td class="header-cell">Exam Duration</td>
            <td>03 Hours</td>
        </tr>
        <tr>
            <td class="header-cell">Primary Reference Text</td>
            <td colspan="3">Behrouz A. Forouzan, <i>Data Communications and Networking</i>, 5th Edition, McGraw-Hill.<br/>
            Larry L. Peterson & Bruce S. Davie, <i>Computer Networks: A Systems Approach</i>, 4th Edition.<br/>
            William Stallings, <i>Data and Computer Communication</i>, 10th Edition.</td>
        </tr>
    </table>

    <div class="toc-card">
        <h3>TABLE OF CONTENTS & MODULE OVERVIEW</h3>
        <div class="toc-grid">
            <div>
                <b>MODULE 1: Introduction, Models, Physical & Switching</b>
                <ul>
                    <li>1. Data Communications & 5 Components</li>
                    <li>2. Networks, Criteria & Topologies (Mesh, Star, Bus, Ring)</li>
                    <li>3. OSI 7-Layer Model vs TCP/IP 5-Layer Protocol Suite</li>
                    <li>4. Guided Media (Twisted-Pair, Coaxial, Fiber-Optics)</li>
                    <li>5. Unguided Media (Radio, Microwave, Infrared)</li>
                    <li>6. Packet Switching: Datagram vs Virtual Circuit</li>
                </ul>
                <b>MODULE 2: Data Link Layer & MAC</b>
                <ul>
                    <li>1. Error Detection/Correction, Block Coding, Hamming Distance</li>
                    <li>2. Cyclic Codes & CRC Modulo-2 Division Calculation</li>
                    <li>3. Internet Checksum & Framing (Bit Stuffing)</li>
                    <li>4. Flow & Error Control: Stop-and-Wait, GBN, Selective Repeat</li>
                    <li>5. HDLC Protocol & Frame Formats (I, S, U Frames)</li>
                    <li>6. MAC: Pure & Slotted ALOHA, CSMA, CSMA/CD, CSMA/CA</li>
                    <li>7. Point-to-Point Protocol (PPP) & Architecture</li>
                </ul>
                <b>MODULE 3: Network Layer & Routing</b>
                <ul>
                    <li>1. Network Layer Services & Packet Switching</li>
                    <li>2. IPv4 Addressing: Classful, CIDR Prefix, Subnetting, NAT</li>
                    <li>3. IPv4 Header Format & Fragmentation Calculations</li>
                    <li>4. IPv6 Base Header Format & Architectural Advantages</li>
                    <li>5. Routing Algorithms: DVR (Bellman-Ford), LSR (Dijkstra SPF), PVR</li>
                    <li>6. Practical Protocols: RIP (Hop count), OSPF (Link state), BGP</li>
                    <li>7. Multicast Routing & MOSPF</li>
                </ul>
            </div>
            <div>
                <b>MODULE 4: Transport Layer & TCP/UDP</b>
                <ul>
                    <li>1. Process-to-Process Delivery, Ports & Multiplexing</li>
                    <li>2. UDP Datagram Format, Checksum & Applications</li>
                    <li>3. TCP Stream Delivery, Byte Numbering & Segment Format</li>
                    <li>4. TCP Connection Life Cycle: 3-Way Handshake & 4-Way Teardown</li>
                    <li>5. TCP Flow Control, Zero Window & Silly Window Syndrome</li>
                    <li>6. TCP Error Control, Retransmissions & Fast Retransmit</li>
                    <li>7. TCP Congestion Control: AIMD, Slow Start, Tahoe vs Reno</li>
                </ul>
                <b>MODULE 5: Application Layer Protocols</b>
                <ul>
                    <li>1. Client-Server Architecture & Socket Programming</li>
                    <li>2. World Wide Web (WWW) & HTTP (HTTP/1.0 vs HTTP/1.1)</li>
                    <li>3. HTTP Request/Response Messages & Status Codes</li>
                    <li>4. FTP Two-Connection Architecture (Active vs Passive PASV)</li>
                    <li>5. Email Architecture: SMTP (Push), MIME, POP3 & IMAP4 (Pull)</li>
                    <li>6. Domain Name System (DNS): Hierarchy, Records, Iterative/Recursive</li>
                    <li>7. TELNET (NVT & Flaws) vs Secure Shell (SSH & Port Forwarding)</li>
                </ul>
                <b>QUICK REVISION & UNIVERSITY EXAM BANK</b>
                <ul>
                    <li>One-Page Summary & Formula Sheet (Modules 1 to 5)</li>
                    <li>50+ High-Yield University Exam Questions & Hints</li>
                </ul>
            </div>
        </div>
    </div>
    """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Computer Networks (BCS502) - Complete Study Notes</title>
    <style>
{CSS_CONTENT}
    </style>
</head>
<body>
{cover_and_meta}
{get_module_1_content()}
{get_module_2_content()}
{get_module_3_content()}
{get_module_4_content()}
{get_module_5_content()}
{get_summary_and_questions_content()}
</body>
</html>
"""
    return full_html

def main():
    print("Generating Complete HTML textbook content...")
    html_content = build_html()
    html_file = os.path.abspath("Computer_Networks_Complete_Study_Notes.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML generated at: {html_file} (Size: {os.path.getsize(html_file):,} bytes)")

    pdf_file = os.path.abspath("Computer_Networks_Complete_Study_Notes_Modules_1_to_5.pdf")
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome):
        chrome = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    print(f"Using browser: {chrome}")
    tmpdir = tempfile.mkdtemp()
    cmd = [
        chrome,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        f"--user-data-dir={tmpdir}",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]

    print("Rendering to PDF with Chrome headless (this generates high-resolution vector textbook pages)...")
    res = subprocess.run(cmd, capture_output=True, timeout=60)
    print(f"Browser Exit Code: {res.returncode}")
    if os.path.exists(pdf_file):
        size_kb = os.path.getsize(pdf_file) / 1024
        print(f"SUCCESS! PDF created at:\n{pdf_file}\nFile Size: {size_kb:.1f} KB")
    else:
        print("ERROR: PDF was not generated.")

if __name__ == "__main__":
    main()
