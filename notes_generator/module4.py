"""
Module 4: Transport Layer - UDP, TCP Architecture, Connection Management, Flow Control, Error Control, and Congestion Control.
"""
from diagrams import fig_tcp_header, fig_tcp_handshake, fig_tcp_congestion

def get_module_4_content():
    content = r"""
    <h1 class="module-title">MODULE 4 &mdash; Transport Layer: UDP, TCP Architecture, Connection Management & Congestion Control</h1>

    <div class="eli5-box">
        <div class="title">💡 ELI5: What is the Transport Layer? (The Apartment Intercom & Phone Call)</div>
        An IP address gets a letter to your apartment building front door. But there are 100 people living in different apartments!
        The <b>Transport Layer</b> adds the <b>Port Number</b> &mdash; the apartment door number!
        Now consider how you communicate:
        • <b>UDP (User Datagram Protocol)</b> is like a <b>Postcard</b>: You scribble a message and drop it in the box. It's fast, has zero setup, but if rain ruins it or it gets lost, nobody tells you. Perfect for live video games where missing one frame isn't worth pausing the game!
        • <b>TCP (Transmission Control Protocol)</b> is like a <b>Phone Call</b>:
          1. You call and wait for them to answer ("Hello?" &rarr; "Hello, I hear you!" &rarr; "Great, let's talk!" &mdash; 3-Way Handshake).
          2. If a sentence gets cut off, they say "Can you repeat that?" (Error Control & Retransmission).
          3. If they talk too fast, you say "Slow down, I'm writing this down!" (Flow Control).
          4. When finished, you both say "Goodbye" and hang up (Connection Termination).
    </div>

    <h2 class="section-title">1. Introduction to Transport-Layer Services (Ch. 23.1 & 23.2)</h2>
    <p>
        The Transport Layer sits in the heart of the protocol stack. It bridges the gap between the application processes above and the lower physical/network communication facility below.
    </p>

    <h3 class="sub-section-title">1.1 Process-to-Process Communication & Port Numbers</h3>
    <p>
        While the network layer delivers packets between <i>hosts</i>, the transport layer delivers data between specific <i>processes (running programs)</i> on those hosts. A process is addressed by a <b>Port Number</b> (16-bit integer, range 0 to 65,535):
    </p>
    <ul>
        <li><b>Well-Known Ports (0 to 1023):</b> Assigned by IANA to standard universal server services (HTTP 80, HTTPS 443, DNS 53, FTP 20/21, SSH 22, SMTP 25).</li>
        <li><b>Registered Ports (1024 to 49,151):</b> Registered for specific commercial applications (e.g., MySQL 3306, PostgreSQL 5432).</li>
        <li><b>Dynamic / Ephemeral / Private Ports (49,152 to 65,535):</b> Temporary ports assigned automatically by the operating system to client programs when opening a connection.</li>
        <li><b>Socket Address:</b> The combination of an <code>IP Address + Port Number</code> (e.g., <code>192.168.1.50:8080</code>). Defines an unambiguous endpoint in a network communication.</li>
    </ul>

    <h3 class="sub-section-title">1.2 Multiplexing and Demultiplexing</h3>
    <ul>
        <li><b>Multiplexing (Sender):</b> The transport layer collects data segments from multiple active application processes, adds transport headers with source and destination port numbers, and passes them down to the single network layer.</li>
        <li><b>Demultiplexing (Receiver):</b> The transport layer receives datagrams from the network layer, inspects the destination port number in the header, and delivers each payload to the exact socket of the corresponding application process.</li>
    </ul>

    <h2 class="section-title">2. User Datagram Protocol &mdash; UDP (Ch. 24.1)</h2>
    <p>
        UDP is a <b>connectionless, unreliable, lightweight transport protocol</b>. It adds almost no overhead beyond port addressing and error detection.
    </p>

    <h3 class="sub-section-title">2.1 UDP Services and Characteristics</h3>
    <ul>
        <li><b>Connectionless:</b> No handshake or setup prior to data transmission. Every datagram is completely independent.</li>
        <li><b>Unreliable:</b> No acknowledgments, no retransmissions, no sequencing, and no flow or congestion control. If a packet is corrupted, it is discarded without warning.</li>
        <li><b>Preserves Message Boundaries:</b> Unlike TCP's byte stream, UDP delivers data in discrete datagrams &mdash; if an application writes 500 bytes to a UDP socket, the receiver reads exactly 500 bytes in a single read call.</li>
        <li><b>Minimal Header Overhead:</b> Fixed at only <b>8 bytes</b> (compared to TCP's minimum 20 bytes).</li>
    </ul>

    <h3 class="sub-section-title">2.2 UDP Datagram Header Format</h3>
    <table style="text-align:center;">
        <tr>
            <th colspan="2">Bits 0 &ndash; 15</th>
            <th colspan="2">Bits 16 &ndash; 31</th>
        </tr>
        <tr>
            <td colspan="2" style="background:#dbeafe;font-weight:bold;">Source Port Number (16 bits)</td>
            <td colspan="2" style="background:#dbeafe;font-weight:bold;">Destination Port Number (16 bits)</td>
        </tr>
        <tr>
            <td colspan="2" style="background:#dcfce7;font-weight:bold;">Total Length (16 bits) [Header + Data]</td>
            <td colspan="2" style="background:#fee2e2;font-weight:bold;">Checksum (16 bits) [Optional in IPv4, Mandatory in IPv6]</td>
        </tr>
        <tr>
            <td colspan="4" style="background:#f8fafc;font-weight:bold;padding:12px;">Data / Application Payload</td>
        </tr>
    </table>
    <p>
        <b>UDP Checksum Calculation:</b> Computed over a <b>12-byte Pseudo-header</b> (Source IP, Destination IP, All zeros, Protocol=17, UDP Length) + the 8-byte UDP header + application data (padded with zeros to an even multiple of 16 bits). The pseudo-header ensures that a misdelivered packet (with wrong destination IP) is caught and dropped!
    </p>

    <h3 class="sub-section-title">2.3 When is UDP Preferred over TCP?</h3>
    <ul>
        <li>Real-time multimedia streaming (VoIP, Zoom, live video) where delay jitter is unacceptable and late retransmitted packets are useless.</li>
        <li>Simple request-reply interactions (DNS queries, DHCP) where connection setup overhead would double transaction latency.</li>
        <li>Multicasting and broadcasting (TCP is strictly point-to-point unicast).</li>
    </ul>

    <h2 class="section-title">3. Transmission Control Protocol &mdash; TCP (Ch. 24.2 - 24.3)</h2>
    <p>
        TCP is a <b>connection-oriented, reliable, stream-delivery transport protocol</b>. It guarantees in-order, error-free delivery of bytes across an unreliable underlying IP network.
    </p>

    <h3 class="sub-section-title">3.1 TCP Services & Key Features</h3>
    <ul>
        <li><b>Stream Delivery Service:</b> TCP views data as an unstructured, continuous sequence of bytes (a byte stream), rather than distinct messages.</li>
        <li><b>Full-Duplex Communication:</b> Data can travel simultaneously in both directions between client and server over the same connection.</li>
        <li><b>Byte-Level Numbering:</b> Every single byte in the stream is assigned a unique 32-bit sequence number. If a segment carries bytes 5001 to 6000, its Sequence Number in the header is <code>5001</code>.</li>
        <li><b>Cumulative Acknowledgments:</b> The ACK number indicates the <b>next byte expected</b> by the receiver. An ACK of <code>6001</code> confirms receipt of all bytes up to 6000.</li>
    </ul>

    <h3 class="sub-section-title">3.2 TCP Segment Header Format</h3>
    <!-- FIG_TCP_HDR -->

    <ul>
        <li><b>Source Port (16b) & Destination Port (16b):</b> Identifies sending and receiving processes.</li>
        <li><b>Sequence Number (32b):</b> Byte offset of the first data byte in this segment.</li>
        <li><b>Acknowledgment Number (32b):</b> Next byte expected from the other party (valid only when ACK flag = 1).</li>
        <li><b>HLEN / Data Offset (4b):</b> Length of TCP header in 32-bit words ($5 \times 4 = 20$ bytes min, 60 bytes max).</li>
        <li><b>Control Flags (6 bits):</b>
            <ul>
                <li><b>URG:</b> Urgent Pointer is valid; data should be processed with priority.</li>
                <li><b>ACK:</b> Acknowledgment field is valid (set on almost every segment after handshake).</li>
                <li><b>PSH (Push):</b> Sender requests immediate transmission to application without waiting to fill buffer.</li>
                <li><b>RST (Reset):</b> Abruptly aborts and resets an invalid or rejected connection.</li>
                <li><b>SYN (Synchronize):</b> Synchronizes initial sequence numbers during connection establishment.</li>
                <li><b>FIN (Finish):</b> Sender has no more data to send; initiates graceful termination.</li>
            </ul>
        </li>
        <li><b>Window Size &mdash; $rwnd$ (16 bits):</b> Receiver's advertised buffer size in bytes for <b>Flow Control</b>.</li>
        <li><b>Checksum (16 bits):</b> Mandatory 16-bit one's complement sum over a 12-byte pseudo-header, TCP header, and data.</li>
        <li><b>Urgent Pointer (16 bits):</b> Offset to the end of urgent data if URG flag is set.</li>
    </ul>

    <h3 class="sub-section-title">3.3 TCP Connection Life Cycle</h3>
    <!-- FIG_TCP_HS -->

    <h4>1. Connection Establishment: The Three-Way Handshake</h4>
    <ol>
        <li><b>Step 1 (SYN from Client):</b> Client picks random Initial Sequence Number ($ISN_c = x$) and sends <code>SYN=1, seq=x</code>. Consumes 1 sequence number. No application data allowed.</li>
        <li><b>Step 2 (SYN + ACK from Server):</b> Server allocates buffers, picks its own $ISN_s = y$, and replies with <code>SYN=1, ACK=1, seq=y, ack=x+1</code>.</li>
        <li><b>Step 3 (ACK from Client):</b> Client confirms with <code>ACK=1, seq=x+1, ack=y+1</code>. May carry initial user data. Connection is now <b>ESTABLISHED</b>!</li>
    </ol>

    <div class="key-point">
        <div class="title">🔑 Why a 3-Way Handshake? (And what is SYN Flooding?)</div>
        A 2-way handshake is insufficient because delayed or duplicated SYN packets from old dead connections could arrive at the server, causing it to allocate resources for phantom sessions. The 3rd step proves to the server that the client is live and genuinely requested this connection.<br/>
        <b>SYN Flood Attack:</b> An attacker floods a server with thousands of fake SYNs with spoofed IPs, ignoring the SYN+ACK replies. The server leaves half-open connection tables until memory exhausts. <b>Defense:</b> <i>SYN Cookies</i> (server encodes connection parameters cryptographically into the server's sequence number $y$, allocating zero state memory until the client's valid 3rd ACK returns).
    </div>

    <h4>2. Connection Termination: The Four-Way Handshake</h4>
    <p>TCP is full-duplex, so each direction must be terminated independently:</p>
    <ol>
        <li><b>Client &rarr; Server (FIN):</b> Client sends <code>FIN=1, seq=u</code>. Client enters <code>FIN_WAIT_1</code>.</li>
        <li><b>Server &rarr; Client (ACK):</b> Server sends <code>ACK=1, ack=u+1</code>. Server enters <code>CLOSE_WAIT</code>; client enters <code>FIN_WAIT_2</code>. The connection is now <b>Half-Closed</b>: client can no longer send, but server can still transmit remaining data!</li>
        <li><b>Server &rarr; Client (FIN):</b> When finished, server sends <code>FIN=1, seq=w, ack=u+1</code>. Server enters <code>LAST_ACK</code>.</li>
        <li><b>Client &rarr; Server (ACK):</b> Client acknowledges with <code>ACK=1, ack=w+1</code> and enters <b>TIME_WAIT state for $2 \times \text{MSL}$</b> (Maximum Segment Lifetime, typically $2 \times 60s = 120s$).
            <br/><i>Why TIME_WAIT?</i> To ensure the final ACK reached the server (if lost, server retransmits FIN, which client can re-ACK), and to allow old delayed duplicate packets to die out in the network before a new connection reuses the same port!</li>
    </ol>

    <h2 class="section-title">4. TCP Flow Control & Silly Window Syndrome (Ch. 24.3.4)</h2>
    <p>
        Flow control matches the sender's transmission rate to the receiver's reading speed using a dynamic <b>Sliding Window</b>:
    </p>
    <ul>
        <li><b>Receiver Advertised Window ($rwnd$):</b> $rwnd = \text{Buffer Size} - (\text{Bytes Received} - \text{Bytes Read by App})$. The receiver reports $rwnd$ in every ACK.</li>
        <li><b>Zero Window Notification:</b> If the receiver buffer fills up, it advertises $rwnd = 0$, telling the sender to pause. Sender starts a <b>Persistence Timer</b> and periodically sends 1-byte <i>Window Probe</i> segments to check if buffer space has opened up.</li>
        <li><b>Silly Window Syndrome (SWS):</b> Occurs when data is transmitted in tiny fragments (e.g., 1 byte of data wrapped in a 40-byte TCP/IP header &mdash; 97% overhead!):
            <ul>
                <li><i>Receiver-Side SWS:</i> Occurs when a slow application reads data 1 byte at a time, causing the receiver to advertise a tiny 1-byte window. <b>Solution (Clark's Algorithm):</b> Force receiver to advertise $rwnd = 0$ until either half the buffer is empty or space for a full Maximum Segment Size (MSS) is available.</li>
                <li><i>Sender-Side SWS:</i> Occurs when an application generates tiny data chunks. <b>Solution (Nagle's Algorithm):</b> Send the first byte immediately. Buffer all subsequent tiny bytes until either: (1) a full MSS is accumulated, or (2) the ACK for the previous outstanding segment arrives.</li>
            </ul>
        </li>
    </ul>

    <h2 class="section-title">5. TCP Error Control (Ch. 24.3.6)</h2>
    <ul>
        <li><b>Retransmission Timeout (RTO):</b> Dynamically computed from smoothed Round Trip Time ($RTT_s$) using Jacobson's algorithm: $RTO = RTT_s + 4 \times RTT_d$.</li>
        <li><b>Karn's Algorithm:</b> Never calculate RTT samples for retransmitted segments (since you cannot tell if an ACK corresponds to the first or second transmission). On timeout, double the timeout value (Exponential Backoff).</li>
        <li><b>Fast Retransmit:</b> When a single segment is lost but subsequent segments arrive, the receiver sends duplicate ACKs. When the sender receives <b>3 Duplicate ACKs</b> for the same sequence number, it immediately retransmits the missing segment <i>without waiting for the RTO timer to expire</i>!</li>
    </ul>

    <h2 class="section-title">6. TCP Congestion Control (Ch. 24.3.7 - 24.3.9)</h2>
    <p>
        While flow control protects the receiver, <b>Congestion Control</b> protects the intermediate routers and network links from being overwhelmed by global traffic.
    </p>
    <div class="formula-box">
        <b>Effective Transmission Window:</b><br/>
        <b>Actual Window = min(rwnd, cwnd)</b><br/>
        Where:<br/>
        • <b>rwnd:</b> Receiver Advertised Window (Flow Control limit)<br/>
        • <b>cwnd:</b> Congestion Window maintained by sender (Congestion Control limit)
    </div>

    <!-- FIG_TCP_CC -->

    <h3 class="sub-section-title">6.1 The Four Core Congestion Control Phases</h3>
    <ol>
        <li><b>Phase 1 &mdash; Slow Start (Exponential Growth):</b>
            <ul>
                <li>Initial state: $cwnd = 1 \text{ MSS}$ (or 2 to 4 MSS).</li>
                <li>For <i>every ACK received</i>, $cwnd$ increases by 1 MSS: $cwnd \gets cwnd + 1 \text{ MSS}$.</li>
                <li>Over one Round Trip Time (RTT), $cwnd$ <b>doubles</b> ($1 \rightarrow 2 \rightarrow 4 \rightarrow 8 \rightarrow 16 \dots$).</li>
                <li>Slow start continues until $cwnd \ge ssthresh$ (Slow Start Threshold).</li>
            </ul>
        </li>
        <li><b>Phase 2 &mdash; Congestion Avoidance (Additive Increase):</b>
            <ul>
                <li>Once $cwnd \ge ssthresh$, exponential growth becomes dangerous. Growth shifts to a linear increase.</li>
                <li>$cwnd$ increases by <b>1 MSS per full RTT</b> (or $cwnd \gets cwnd + \frac{1}{cwnd}$ per ACK).</li>
                <li>This is the <b>Additive Increase</b> phase of <b>AIMD (Additive Increase Multiplicative Decrease)</b>.</li>
            </ul>
        </li>
        <li><b>Phase 3 &mdash; Fast Retransmit:</b>
            <ul>
                <li>Upon receiving <b>3 Duplicate ACKs</b>, sender concludes a packet was lost due to mild congestion, and immediately retransmits the missing segment.</li>
            </ul>
        </li>
        <li><b>Phase 4 &mdash; Fast Recovery: TCP Tahoe vs TCP Reno:</b>
            <ul>
                <li><b>TCP Tahoe (Legacy):</b> On either timeout or 3 Duplicate ACKs, sets $ssthresh = cwnd / 2$ and <b>resets $cwnd = 1 \text{ MSS}$</b>! Goes back to slow start. Harsh and overly penalizing.</li>
                <li><b>TCP Reno (Modern Standard):</b>
                    <ul>
                        <li>On Timeout (Severe Congestion): Sets $ssthresh = cwnd / 2$, resets $cwnd = 1$, enters Slow Start.</li>
                        <li>On 3 Duplicate ACKs (Mild Congestion): Enters <b>Fast Recovery</b>. Sets $ssthresh = cwnd / 2$, sets $cwnd = ssthresh + 3 \text{ MSS}$ (accounting for 3 buffered segments), and <b>skips slow start directly into Congestion Avoidance (linear growth)</b>! Preserves high throughput.</li>
                    </ul>
                </li>
            </ul>
        </li>
    </ol>
    """
    return (content.replace('<!-- FIG_TCP_HDR -->', fig_tcp_header()).replace('<!-- FIG_TCP_HS -->', fig_tcp_handshake()).replace('<!-- FIG_TCP_CC -->', fig_tcp_congestion()))
