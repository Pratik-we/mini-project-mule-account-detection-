"""
Quick Revision Summary Sheets and Likely University Exam Questions for Modules 1 to 5.
"""

def get_summary_and_questions_content():
    return """
    <h1 class="module-title">QUICK REVISION &mdash; One-Page High-Yield Summaries (Modules 1 &ndash; 5)</h1>

    <h2 class="section-title">Module 1 Quick Revision</h2>
    <table>
        <tr>
            <th>Concept</th>
            <th>Core Formula / Key Fact to Remember</th>
        </tr>
        <tr>
            <td><b>Data Comm 5 Components</b></td>
            <td>Message, Sender, Receiver, Transmission Medium, Protocol.</td>
        </tr>
        <tr>
            <td><b>Communication Modes</b></td>
            <td>Simplex (1-way), Half-Duplex (2-way alternate), Full-Duplex (2-way simultaneous).</td>
        </tr>
        <tr>
            <td><b>Mesh Topology Links</b></td>
            <td><b>Links = n(n - 1) / 2</b> | <b>I/O ports per device = n - 1</b> (Dedicated point-to-point).</td>
        </tr>
        <tr>
            <td><b>Star / Bus / Ring</b></td>
            <td>Star: $n$ links to central hub/switch. Bus: Backbone with tap lines. Ring: Repeater loop with token.</td>
        </tr>
        <tr>
            <td><b>OSI vs TCP/IP</b></td>
            <td>OSI = 7 layers (All People Seem To Need Data Processing). TCP/IP = 5 layers (Application, Transport, Network, Data Link, Physical).</td>
        </tr>
        <tr>
            <td><b>Four Addresses</b></td>
            <td>Physical (MAC 48b), Logical (IP 32/128b), Port (16b), Specific (URL / Email).</td>
        </tr>
        <tr>
            <td><b>Transmission Media</b></td>
            <td>Twisted Pair (crosstalk cancellation), Coaxial (shielded copper), Fiber (Total Internal Reflection $n_1 > n_2$).</td>
        </tr>
        <tr>
            <td><b>Packet Switching</b></td>
            <td>Datagram (Connectionless, independent routing, stateless) vs Virtual Circuit (Connection-oriented, 3 phases: setup, transfer, teardown, VCI tables).</td>
        </tr>
    </table>

    <h2 class="section-title">Module 2 Quick Revision</h2>
    <table>
        <tr>
            <th>Concept</th>
            <th>Core Formula / Key Fact to Remember</th>
        </tr>
        <tr>
            <td><b>Error Detection / Correction</b></td>
            <td>To detect $s$ errors: <b>$d_{min} \ge s + 1$</b> | To correct $t$ errors: <b>$d_{min} \ge 2t + 1$</b>.</td>
        </tr>
        <tr>
            <td><b>Bit Stuffing</b></td>
            <td>Delimiter flag = <code>01111110</code>. Transmit: stuff a <code>0</code> after five consecutive <code>1</code>s.</td>
        </tr>
        <tr>
            <td><b>CRC Checksum</b></td>
            <td>Append $n$ zeros (degree of divisor). Modulo-2 binary division (XOR). Remainder is CRC.</td>
        </tr>
        <tr>
            <td><b>Stop-and-Wait ARQ</b></td>
            <td>$S_w = 1, R_w = 1$. High idle delay.</td>
        </tr>
        <tr>
            <td><b>Go-Back-N (GBN)</b></td>
            <td><b>$S_w = 2^m - 1, R_w = 1$</b>. Cumulative ACK. Discards out-of-order frames; retransmits from lost frame.</td>
        </tr>
        <tr>
            <td><b>Selective Repeat (SR)</b></td>
            <td><b>$S_w = 2^{m-1}, R_w = 2^{m-1}$</b>. Individual ACK / NAK. Buffers out-of-order frames; retransmits ONLY damaged frame.</td>
        </tr>
        <tr>
            <td><b>HDLC Frames</b></td>
            <td>I-Frame (Data + Piggybacked ACK), S-Frame (Flow/Error control), U-Frame (Link management).</td>
        </tr>
        <tr>
            <td><b>ALOHA Throughput</b></td>
            <td>Pure ALOHA: Vulnerable time = $2 T_{fr}$, $S_{max} = 1/(2e) \approx 18.4\%$. Slotted ALOHA: Vulnerable time = $T_{fr}$, $S_{max} = 1/e \approx 36.8\%$.</td>
        </tr>
        <tr>
            <td><b>CSMA/CD Constraint</b></td>
            <td><b>$T_{fr} \ge 2 T_p$</b> or <b>$L_{min} \ge 2 \times \text{Propagation Delay} \times \text{Bandwidth}$</b> (Ethernet = 64 bytes).</td>
        </tr>
        <tr>
            <td><b>CSMA/CA (Wi-Fi)</b></td>
            <td>IFS (DIFS/SIFS), Contention Window, RTS/CTS handshake for Hidden Terminal, mandatory ACK.</td>
        </tr>
    </table>

    <h2 class="section-title">Module 3 Quick Revision</h2>
    <table>
        <tr>
            <th>Concept</th>
            <th>Core Formula / Key Fact to Remember</th>
        </tr>
        <tr>
            <td><b>Classful IPv4</b></td>
            <td>Class A: 0-127 (/8), Class B: 128-191 (/16), Class C: 192-223 (/24), Class D: 224-239 (Multicast), Class E: 240-255.</td>
        </tr>
        <tr>
            <td><b>CIDR & Subnetting</b></td>
            <td>Prefix /n. Host bits = $32 - n$. Total IPs = $2^{32-n}$. Usable hosts = $2^{32-n} - 2$.</td>
        </tr>
        <tr>
            <td><b>Private IP Ranges</b></td>
            <td>10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 (RFC 1918).</td>
        </tr>
        <tr>
            <td><b>IPv4 Fragmentation</b></td>
            <td>Fragment Offset = <b>(Byte offset) / 8</b>. MF=1 (more fragments follow), MF=0 (last).</td>
        </tr>
        <tr>
            <td><b>IPv6 Base Header</b></td>
            <td><b>Fixed 40 bytes</b>, 128-bit addresses, no header checksum, no router fragmentation, Extension Headers via Next Header.</td>
        </tr>
        <tr>
            <td><b>DVR vs LSR</b></td>
            <td>DVR: Bellman-Ford, exchange full table with neighbors, count-to-infinity solved by Split Horizon / Poison Reverse.<br/>LSR: Floods LSPs to all, builds LSDB, Dijkstra SPF tree.</td>
        </tr>
        <tr>
            <td><b>Routing Protocols</b></td>
            <td>RIP (Distance Vector, max 15 hops, UDP 520), OSPF (Link State, Bandwidth cost, Protocol 89), BGP (Path Vector, AS Path, TCP 179).</td>
        </tr>
    </table>

    <h2 class="section-title">Module 4 Quick Revision</h2>
    <table>
        <tr>
            <th>Concept</th>
            <th>Core Formula / Key Fact to Remember</th>
        </tr>
        <tr>
            <td><b>Transport Layer Role</b></td>
            <td>Process-to-process delivery using 16-bit Port numbers. Multiplexing / Demultiplexing.</td>
        </tr>
        <tr>
            <td><b>UDP Characteristics</b></td>
            <td>Connectionless, unreliable, 8-byte fixed header, message boundary preserved, no congestion control.</td>
        </tr>
        <tr>
            <td><b>TCP Characteristics</b></td>
            <td>Connection-oriented, reliable, stream delivery, full-duplex, 20-60 byte header, byte-stream sequence numbers.</td>
        </tr>
        <tr>
            <td><b>TCP Handshakes</b></td>
            <td>3-Way Setup: <code>SYN &rarr; SYN+ACK &rarr; ACK</code> | 4-Way Teardown: <code>FIN &rarr; ACK &rarr; FIN &rarr; ACK</code> ($2 \times \text{MSL}$ in TIME_WAIT).</td>
        </tr>
        <tr>
            <td><b>Flow Control & SWS</b></td>
            <td>Sliding window governed by $rwnd$. Silly Window Syndrome solved by <b>Clark's algorithm</b> (receiver) and <b>Nagle's algorithm</b> (sender).</td>
        </tr>
        <tr>
            <td><b>Congestion Control</b></td>
            <td><b>Window = min(rwnd, cwnd)</b>. Slow Start ($cwnd \times 2$ per RTT), Congestion Avoidance ($cwnd + 1$ per RTT).</td>
        </tr>
        <tr>
            <td><b>Tahoe vs Reno</b></td>
            <td>Tahoe: 3 dup ACKs drops $cwnd = 1$. Reno: Fast Recovery sets $ssthresh = cwnd/2, cwnd = ssthresh + 3$, skips to linear growth!</td>
        </tr>
    </table>

    <h2 class="section-title">Module 5 Quick Revision</h2>
    <table>
        <tr>
            <th>Concept</th>
            <th>Core Formula / Key Fact to Remember</th>
        </tr>
        <tr>
            <td><b>HTTP</b></td>
            <td>Stateless, Port 80 (HTTPS 443). HTTP/1.0 non-persistent ($2 \text{ RTT}$ per object); HTTP/1.1 persistent keep-alive & pipelining.</td>
        </tr>
        <tr>
            <td><b>FTP</b></td>
            <td>Two connections: Control (Port 21, persistent ASCII) and Data (Port 20 active, or ephemeral passive PASV).</td>
        </tr>
        <tr>
            <td><b>Electronic Mail</b></td>
            <td>SMTP (Port 25, Push, 7-bit ASCII). MIME (enables binary/attachments). POP3 (Port 110, simple download). IMAP4 (Port 143, permanent server sync).</td>
        </tr>
        <tr>
            <td><b>DNS Architecture</b></td>
            <td>Port 53 (UDP/TCP). Hierarchical tree: Root &rarr; TLD &rarr; Authoritative. Iterative vs Recursive resolution.</td>
        </tr>
        <tr>
            <td><b>DNS Records</b></td>
            <td>A (IPv4), AAAA (IPv6), CNAME (Alias), NS (Name server), MX (Mail exchange), PTR (Reverse IP &rarr; Name).</td>
        </tr>
        <tr>
            <td><b>TELNET vs SSH</b></td>
            <td>TELNET: Port 23, plaintext (unsecure), NVT. SSH: Port 22, full encryption, server authentication, user public key auth, port forwarding tunnels.</td>
        </tr>
    </table>

    <h1 class="module-title">LIKELY EXAM QUESTIONS &mdash; University Question Bank (Modules 1 &ndash; 5)</h1>

    <h2 class="section-title">Module 1 Likely Exam Questions</h2>
    <ol>
        <li><b>Explain the five components of data communication with a neat diagram.</b> (6 Marks)</li>
        <li><b>Differentiate between Simplex, Half-Duplex, and Full-Duplex transmission modes with suitable examples.</b> (5 Marks)</li>
        <li><b>Define Network Topology. Compare Mesh, Star, Bus, and Ring topologies with diagrams, link formulas, and advantages/disadvantages.</b> (10 Marks)</li>
        <li><b>Explain the 7 layers of the OSI reference model with neat diagrams and describe the functions of each layer.</b> (10 Marks)</li>
        <li><b>Compare the OSI reference model with the TCP/IP protocol suite. Explain the four levels of addresses used in TCP/IP.</b> (8 Marks)</li>
        <li><b>Discuss guided transmission media: compare Twisted-Pair, Coaxial, and Optical Fiber cables in terms of physical construction, bandwidth, and attenuation.</b> (8 Marks)</li>
        <li><b>Explain packet switching. Differentiate between the Datagram approach and Virtual-Circuit approach with diagrams.</b> (8 Marks)</li>
    </ol>

    <h2 class="section-title">Module 2 Likely Exam Questions</h2>
    <ol>
        <li><b>Explain the difference between error detection and error correction. State the minimum Hamming distance condition for detecting $s$ errors and correcting $t$ errors.</b> (6 Marks)</li>
        <li><b>What is CRC? Given dataword <code>100100</code> and divisor polynomial $x^3 + x + 1$, find the transmitted codeword using modulo-2 division. Show the error checking at receiver.</b> (8 Marks)</li>
        <li><b>Explain framing in the data link layer. Discuss bit-oriented framing and the bit stuffing mechanism with an example.</b> (6 Marks)</li>
        <li><b>Explain the working of Stop-and-Wait ARQ, Go-Back-N ARQ, and Selective Repeat ARQ with sliding window diagrams and sequence charts.</b> (10 Marks)</li>
        <li><b>Why is the maximum sender window size in Go-Back-N protocol $2^m - 1$ instead of $2^m$? Explain with an ambiguity scenario.</b> (6 Marks)</li>
        <li><b>Explain the frame format and three frame types (I-frame, S-frame, U-frame) of HDLC protocol.</b> (8 Marks)</li>
        <li><b>Differentiate between Pure ALOHA and Slotted ALOHA. Derive and compare their maximum theoretical throughputs and vulnerable times.</b> (8 Marks)</li>
        <li><b>Explain the CSMA/CD protocol. Why is there a minimum frame size limitation in CSMA/CD? State the mathematical expression.</b> (8 Marks)</li>
        <li><b>Explain how CSMA/CA avoids collisions in wireless networks using IFS, Contention Window, and RTS/CTS frames.</b> (7 Marks)</li>
        <li><b>Discuss the Point-to-Point Protocol (PPP) architecture, frame format, and transition phases.</b> (7 Marks)</li>
    </ol>

    <h2 class="section-title">Module 3 Likely Exam Questions</h2>
    <ol>
        <li><b>Explain IPv4 addressing. Compare Classful addressing with Classless Inter-Domain Routing (CIDR).</b> (7 Marks)</li>
        <li><b>An ISP is granted a block of addresses <code>192.168.1.0/24</code>. Allocate 4 equal subnets. Calculate the subnet mask, network address, usable host address range, and broadcast address for each subnet.</b> (8 Marks)</li>
        <li><b>Explain the concept of NAT (Network Address Translation). What are the RFC 1918 private address ranges? Explain Port Address Translation (NAPT).</b> (7 Marks)</li>
        <li><b>Draw the neat diagram of IPv4 Datagram Header and explain the function of every field.</b> (10 Marks)</li>
        <li><b>An IPv4 packet of 4020 bytes (20 bytes header) arrives at a router with MTU = 1500 bytes. Calculate the fragment sizes, flags (MF), and fragment offsets for each fragment.</b> (8 Marks)</li>
        <li><b>Draw the IPv6 base header format. Highlight five major technical advantages of IPv6 over IPv4.</b> (8 Marks)</li>
        <li><b>Explain Distance Vector Routing algorithm. What is the Count-to-Infinity problem and how is it mitigated using Split Horizon and Poison Reverse?</b> (8 Marks)</li>
        <li><b>Explain Link State Routing algorithm. Apply Dijkstra's Shortest Path First algorithm on a given network graph to compute the routing table.</b> (10 Marks)</li>
        <li><b>Compare RIP, OSPF, and BGP routing protocols with respect to algorithm, metric, scope, and transport layer protocol.</b> (8 Marks)</li>
        <li><b>Write a note on Multicast Routing and MOSPF.</b> (5 Marks)</li>
    </ol>

    <h2 class="section-title">Module 4 Likely Exam Questions</h2>
    <ol>
        <li><b>Explain transport-layer services: process-to-process delivery, port numbers, multiplexing, and demultiplexing.</b> (7 Marks)</li>
        <li><b>Draw the UDP header format. Explain why UDP is preferred over TCP for real-time applications despite being unreliable.</b> (7 Marks)</li>
        <li><b>Draw the TCP segment header format and explain the importance of Sequence Number, Acknowledgment Number, Window Size, and Flags.</b> (10 Marks)</li>
        <li><b>Explain TCP Connection Management: describe the Three-Way Handshake connection establishment and Four-Way Handshake connection termination with sequence diagrams.</b> (10 Marks)</li>
        <li><b>Why does TCP stay in TIME_WAIT state for $2 \times \text{MSL}$ during connection teardown?</b> (5 Marks)</li>
        <li><b>Explain TCP Flow Control. What is Silly Window Syndrome and how is it resolved by Clark's and Nagle's algorithms?</b> (8 Marks)</li>
        <li><b>Explain TCP Congestion Control. Distinguish between Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery. Compare TCP Tahoe with TCP Reno.</b> (10 Marks)</li>
    </ol>

    <h2 class="section-title">Module 5 Likely Exam Questions</h2>
    <ol>
        <li><b>Explain the client-server architecture. Discuss the standard socket system calls used to build a concurrent TCP client-server application.</b> (8 Marks)</li>
        <li><b>Explain the architecture of the World Wide Web and HTTP. Differentiate between Non-Persistent and Persistent HTTP with RTT timing diagrams.</b> (8 Marks)</li>
        <li><b>Explain the format of HTTP Request and Response messages. List five common HTTP status codes and their meanings.</b> (7 Marks)</li>
        <li><b>Explain the FTP architecture. Why does FTP use two separate connections (Control on Port 21 and Data on Port 20)? Differentiate between Active and Passive FTP.</b> (8 Marks)</li>
        <li><b>Explain the end-to-end architecture of Electronic Mail. Discuss the role of User Agent (UA), MTA (SMTP), and MAA (POP3/IMAP4).</b> (8 Marks)</li>
        <li><b>Why is SMTP limited to 7-bit ASCII? How does MIME solve this limitation for multimedia attachments?</b> (6 Marks)</li>
        <li><b>Compare POP3 and IMAP4 message access protocols.</b> (5 Marks)</li>
        <li><b>Explain the Domain Name System (DNS). Describe the hierarchical name space, DNS server hierarchy, and DNS resource records (A, CNAME, MX, NS, PTR).</b> (8 Marks)</li>
        <li><b>Differentiate between Iterative and Recursive DNS resolution with a neat sequence flow diagram.</b> (8 Marks)</li>
        <li><b>What is TELNET? Explain the Network Virtual Terminal (NVT) concept. Why is TELNET considered insecure?</b> (6 Marks)</li>
        <li><b>Explain the three-layer architecture of Secure Shell (SSH). Discuss SSH port forwarding (tunneling) and compare SSH with TELNET.</b> (8 Marks)</li>
    </ol>
    """
