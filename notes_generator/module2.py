"""
Module 2: Data Link Layer - Error Detection and Correction, DLC Services, Protocols, HDLC, MAC, Checksum, and PPP.
"""
from diagrams import fig_framing_bit_stuffing, fig_crc_division, fig_sliding_window_protocols, fig_mac_protocols

def get_module_2_content():
    content = r"""
    <h1 class="module-title">MODULE 2 &mdash; Data Link Layer: Error Detection & Correction, DLC, HDLC, MAC & PPP</h1>

    <div class="eli5-box">
        <div class="title">💡 ELI5: What does the Data Link Layer do?</div>
        Imagine you are passing a secret note to a friend sitting two rows ahead in a noisy classroom. If someone coughs or bumps the paper, a letter might get smudged (<b>Transmission Error</b>).
        To fix this:
        1. <b>Framing:</b> You write [START] and [END] on the note so your friend knows where it begins and ends.
        2. <b>Error Detection:</b> You write at the bottom: "There are 15 words in this note." If your friend counts only 14, they know a word got erased!
        3. <b>Flow Control:</b> You don't throw 50 notes at once &mdash; you wait until your friend reads the first one and nods (ACK) before passing the next.
        4. <b>Media Access:</b> Everyone in the room shares the same air. If two kids talk at the exact same second, it's a collision! You need rules like raising your hand before speaking.
    </div>

    <h2 class="section-title">1. Error Detection and Correction (Ch. 10.1 - 10.4)</h2>
    <p>
        Networks transmit electromagnetic signals across physical media. Noise, electromagnetic radiation, and physical line defects can alter signal voltage levels, causing transmitted <code>0</code>s to invert to <code>1</code>s and vice versa.
    </p>

    <h3 class="sub-section-title">1.1 Types of Errors</h3>
    <ul>
        <li><b>Single-Bit Error:</b> Only one bit in a given data unit (byte or packet) is corrupted. Relatively rare in serial communications because noise pulses typically last longer than the duration of a single bit.</li>
        <li><b>Burst Error:</b> Two or more bits in the data unit are corrupted. The length of the burst is measured from the first corrupted bit to the last corrupted bit (even if intermediate bits in between are intact). Burst errors are common in high-speed networks where a brief noise spike lasts across hundreds of bits.</li>
    </ul>

    <h3 class="sub-section-title">1.2 Redundancy, Detection vs Correction</h3>
    <p>
        To detect or correct errors, we must append extra bits to the original data &mdash; known as <b>Redundant Bits</b>. The receiver uses these redundant bits to verify the integrity of the data.
    </p>
    <ul>
        <li><b>Error Detection:</b> The receiver can only determine <i>if</i> an error occurred. The receiver discards the corrupted frame and asks the sender to retransmit (<b>ARQ &mdash; Automatic Repeat Request</b>). Used when error rates are low (fiber, wired LANs).</li>
        <li><b>Forward Error Correction (FEC):</b> The receiver determines not only that an error occurred, but precisely <i>which bit positions</i> flipped, allowing immediate correction without retransmission. Used in satellite links, wireless networks with high round-trip delays, and real-time streaming where retransmission is too slow.</li>
    </ul>

    <h3 class="sub-section-title">1.3 Block Coding & Hamming Distance</h3>
    <p>
        In block coding, we divide the message into $k$-bit datawords. We add $r$ redundant bits to each block to produce an $n$-bit codeword, where $n = k + r$. The code is designated as $(n, k)$.
    </p>
    <ul>
        <li><b>Hamming Distance $d(x, y)$:</b> The number of bit positions in which two codewords of equal length differ. Computed by taking the bitwise <code>XOR</code> of the two codewords and counting the number of <code>1</code>s (Hamming weight).
            <br/><i>Example:</i> $x = 10101, y = 11100$. $x \oplus y = 01001 \rightarrow$ Hamming distance = 2.
        </li>
        <li><b>Minimum Hamming Distance ($d_{min}$):</b> The smallest Hamming distance between all possible valid codeword pairs in a code set.</li>
    </ul>

    <div class="formula-box">
        <b>Crucial Theorem for Error Detection & Correction:</b><br/>
        • To detect up to 's' errors: <b>d_min &ge; s + 1</b><br/>
        • To correct up to 't' errors: <b>d_min &ge; 2t + 1</b>
    </div>
    <p>
        <i>Why?</i> If $d_{min} = 3$: Any single bit flip produces an invalid codeword ($s=2$ errors detected because distance from any valid codeword is at least 1). If 1 bit flips ($t=1$), the invalid word is closer to the original valid word (distance 1) than any other valid word (distance $\ge 2$), allowing unambiguous correction.
    </p>

    <h3 class="sub-section-title">1.4 Cyclic Codes and Cyclic Redundancy Check (CRC)</h3>
    <p>
        Cyclic codes are a category of linear block codes where cyclically shifting any valid codeword produces another valid codeword. The most powerful and ubiquitous cyclic code used in networks (Ethernet, Wi-Fi, HDLC) is the <b>Cyclic Redundancy Check (CRC)</b>.
    </p>
    <ul>
        <li><b>Generator Polynomial $G(x)$:</b> The divisor used in modulo-2 arithmetic. A polynomial such as $x^3 + x + 1$ translates into the binary bit pattern <code>1011</code> (highest power $x^3 \rightarrow 1$, $x^2 \rightarrow 0$, $x^1 \rightarrow 1$, $x^0 \rightarrow 1$).</li>
        <li><b>Encoding Algorithm (Sender):</b>
            <ol>
                <li>Let the dataword have $k$ bits and the divisor have $n+1$ bits (degree $n$).</li>
                <li>Append $n$ zeros to the right of the dataword.</li>
                <li>Divide the augmented dataword by the divisor using <b>Modulo-2 Binary Division</b> (bitwise XOR, no carries, no borrows).</li>
                <li>The resulting $n$-bit remainder is the <b>CRC Checksum</b>.</li>
                <li>Replace the appended $n$ zeros with this remainder to form the transmitted codeword.</li>
            </ol>
        </li>
        <li><b>Decoding Algorithm (Receiver):</b>
            <ol>
                <li>Divide the received codeword by the identical divisor using modulo-2 division.</li>
                <li>If the remainder is <b>all zeros (000)</b>, the frame is accepted (no error detected).</li>
                <li>If the remainder is non-zero, an error occurred; the frame is discarded.</li>
            </ol>
        </li>
    </ul>

    <!-- FIG_CRC -->

    <div class="exam-tip">
        <div class="title">⭐ Worked Numerical: CRC Generation & Checking</div>
        <b>Problem:</b> Given Dataword = <code>100100</code> and Divisor Polynomial = $x^3 + x + 1$ (Divisor = <code>1011</code>, degree $n=3$). Find the transmitted codeword and verify error detection.<br/>
        <b>Step 1:</b> Append $n=3$ zeros to dataword: <code>100100 000</code>.<br/>
        <b>Step 2: Modulo-2 Division:</b><br/>
        <code>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;101011  (Quotient)<br/>
        1011 | 100100000<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1011<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;001000000<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1011<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0011000<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1011<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;01110<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1011<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0101 (Remainder / CRC = 001)<br/>
        </code>
        <b>Transmitted Codeword:</b> <code>100100 001</code>.<br/>
        <b>Receiver Check:</b> Receiver divides <code>100100001</code> by <code>1011</code>. The remainder evaluates to <code>0000</code>. Packet accepted!
    </div>

    <h3 class="sub-section-title">1.5 Internet Checksum</h3>
    <p>
        The traditional <b>Checksum</b> is used primarily by network and transport layer protocols (IPv4, TCP, UDP).
    </p>
    <ul>
        <li><b>Sender Algorithm:</b>
            <ol>
                <li>Divide the message into 16-bit words.</li>
                <li>Add all 16-bit words together using <b>One's Complement Addition</b> (if a carry out occurs from the 16th bit, wrap it around and add it to the sum).</li>
                <li>Take the one's complement (invert all bits: $0 \rightarrow 1, 1 \rightarrow 0$) of the final sum. This is the checksum.</li>
                <li>Append the checksum to the payload.</li>
            </ol>
        </li>
        <li><b>Receiver Algorithm:</b>
            <ol>
                <li>Sum all received 16-bit words including the checksum using one's complement arithmetic.</li>
                <li>Take the complement of the total. If the result is <b>all 0s (0x0000)</b>, accept the packet. Otherwise, reject.</li>
            </ol>
        </li>
    </ul>

    <h2 class="section-title">2. Data Link Control (DLC) Services (Ch. 11.1 - 11.4)</h2>
    <p>
        Data Link Control handles the design of node-to-node communication across a single physical link.
    </p>

    <h3 class="sub-section-title">2.1 Framing & Bit Stuffing</h3>
    <p>
        Since physical media deliver continuous streams of raw bits, the Data Link Layer must demarcate the start and end of each transmission unit. This is called <b>Framing</b>.
    </p>
    <ul>
        <li><b>Character-Oriented (Byte-Oriented) Framing:</b> Uses a special 8-bit character flag (e.g., <code>SYN</code> or <code>FLAG</code>) at the start and end. If the user data itself contains the flag character, a <b>Byte Stuffing</b> mechanism inserts an escape character (<code>DLE</code> &mdash; Data Link Escape) immediately before it.</li>
        <li><b>Bit-Oriented Framing & Bit Stuffing:</b> Uses a unique delimiter flag pattern <code>01111110</code> (six consecutive 1s surrounded by 0s) at the beginning and end of the frame.
            <br/><b>Bit Stuffing Rule:</b> Whenever the transmitter detects <b>five consecutive 1s</b> in the data stream, it automatically stuffs a <code>0</code> immediately after the fifth <code>1</code>, regardless of what the next bit is. The receiver detects any pattern of five <code>1</code>s followed by a <code>0</code> and automatically strips the <code>0</code>, restoring the exact original payload.
        </li>
    </ul>

    <!-- FIG_FRAME -->

    <h3 class="sub-section-title">2.2 Flow Control & Error Control</h3>
    <ul>
        <li><b>Flow Control:</b> Prevents a fast sender from overwhelming a slow receiver's input buffer. Uses feedback: the receiver sends permission (acknowledgments or window size updates) allowing the sender to transmit more data.</li>
        <li><b>Error Control:</b> Detects corrupted, lost, or duplicated frames and triggers retransmissions. Implemented using <b>ARQ (Automatic Repeat Request)</b>, sequence numbers, positive acknowledgments (ACK), and retransmission timers.</li>
    </ul>

    <h3 class="sub-section-title">2.3 Data Link Layer Protocols: Stop-and-Wait, Go-Back-N, and Selective Repeat</h3>
    <!-- FIG_SLIDE -->

    <table>
        <tr>
            <th>Feature</th>
            <th>Stop-and-Wait ARQ</th>
            <th>Go-Back-N ARQ (GBN)</th>
            <th>Selective Repeat ARQ (SR)</th>
        </tr>
        <tr>
            <td><b>Sender Window Size ($S_w$)</b></td>
            <td>$1$</td>
            <td><b>$2^m - 1$</b> (where $m$ is sequence number bits)</td>
            <td><b>$2^{m-1}$</b></td>
        </tr>
        <tr>
            <td><b>Receiver Window Size ($R_w$)</b></td>
            <td>$1$</td>
            <td>$1$ (Accepts in-order only)</td>
            <td><b>$2^{m-1}$</b> (Accepts out-of-order)</td>
        </tr>
        <tr>
            <td><b>Acknowledgment Type</b></td>
            <td>Individual ACK for frame</td>
            <td><b>Cumulative ACK</b> (ACK $n$ confirms all frames up to $n-1$)</td>
            <td><b>Individual ACK / NAK</b> for specific damaged frames</td>
        </tr>
        <tr>
            <td><b>On Frame Loss / Damage</b></td>
            <td>Sender times out and retransmits the single frame</td>
            <td>Sender retransmits the lost frame <b>AND all subsequent frames</b> sent in the window!</td>
            <td>Sender retransmits <b>ONLY the lost / damaged frame</b></td>
        </tr>
        <tr>
            <td><b>Receiver Buffering</b></td>
            <td>None (1 frame capacity)</td>
            <td>None (discards all out-of-order frames)</td>
            <td>Full buffer allocated for out-of-order frames</td>
        </tr>
        <tr>
            <td><b>Channel Utilization</b></td>
            <td>Very Poor ($\approx \frac{1}{1 + 2a}$)</td>
            <td>High over clean lines; drops on noisy links</td>
            <td>Maximum efficiency; ideal for noisy, high-delay channels</td>
        </tr>
    </table>

    <div class="key-point">
        <div class="title">🔑 Why is Send Window Size in GBN at most $2^m - 1$?</div>
        If $m=2$ (sequence numbers 0, 1, 2, 3), suppose we allowed $S_w = 2^2 = 4$. The sender transmits frames 0, 1, 2, 3. The receiver accepts all and sends cumulative ACK 0 (requesting frame 0 of the next round). If this ACK is lost, the sender times out and retransmits frames 0, 1, 2, 3. The receiver, expecting <i>new</i> frames 0, 1, 2, 3, would mistakenly accept the retransmitted frames as brand new data!
        By capping $S_w \le 2^m - 1$, the old and new windows never overlap, eliminating ambiguity.
    </div>

    <h2 class="section-title">3. High-Level Data Link Control (HDLC) (Ch. 11.3)</h2>
    <p>
        HDLC is a bit-oriented synchronous data link protocol developed by ISO. It supports both half-duplex and full-duplex communication over point-to-point and multipoint links.
    </p>
    <ul>
        <li><b>Transfer Modes:</b>
            <ul>
                <li><b>Normal Response Mode (NRM):</b> Unbalanced configuration with one primary station and one or more secondary stations. Secondary can transmit only in response to a poll from the primary.</li>
                <li><b>Asynchronous Balanced Mode (ABM):</b> Balanced point-to-point configuration where either station can initiate transmission without authorization (used in modern links).</li>
            </ul>
        </li>
        <li><b>HDLC Frame Format:</b>
            <table style="text-align:center;">
                <tr>
                    <td style="background:#fee2e2;font-weight:bold;">Flag (8b)</td>
                    <td style="background:#dbeafe;font-weight:bold;">Address (8b+)</td>
                    <td style="background:#fef3c7;font-weight:bold;">Control (8 or 16b)</td>
                    <td style="background:#dcfce7;font-weight:bold;">Information Field (Variable)</td>
                    <td style="background:#f3e8ff;font-weight:bold;">FCS (16 or 32b)</td>
                    <td style="background:#fee2e2;font-weight:bold;">Flag (8b)</td>
                </tr>
                <tr>
                    <td><code>01111110</code></td>
                    <td>Secondary address</td>
                    <td>Defines Frame Type</td>
                    <td>User Data (in I-frames)</td>
                    <td>CRC-CCITT</td>
                    <td><code>01111110</code></td>
                </tr>
            </table>
        </li>
        <li><b>Three Types of HDLC Frames (Determined by Control Field):</b>
            <ul>
                <li><b>Information Frames (I-Frames):</b> Carry user data from higher layers plus flow/error control information piggybacked (Send sequence number $N(S)$ and Receive sequence number $N(R)$). First bit is <code>0</code>.</li>
                <li><b>Supervisory Frames (S-Frames):</b> Do not carry user data. Carry flow and error control commands (ACK, NAK, Receive Ready &mdash; RR, Receive Not Ready &mdash; RNR, Reject &mdash; REJ, Selective Reject &mdash; SREJ). First two bits are <code>10</code>.</li>
                <li><b>Unnumbered Frames (U-Frames):</b> Used for link management, session initialization, and disconnect commands (SABM, DISC, UA). First two bits are <code>11</code>.</li>
            </ul>
        </li>
    </ul>

    <h2 class="section-title">4. Media Access Control (MAC) (Ch. 12.1 - 12.2)</h2>
    <p>
        When multiple stations share a single broadcast transmission medium, their signals will collide if they transmit concurrently. Media Access Control (MAC) protocols coordinate which device is allowed to transmit.
    </p>

    <!-- FIG_MAC -->

    <h3 class="sub-section-title">4.1 Random Access Protocols</h3>
    <h4>1. ALOHA Protocols</h4>
    <ul>
        <li><b>Pure ALOHA:</b> Whenever a station has data, it transmits immediately. If two stations transmit overlapping frames, a collision occurs and frames are destroyed. Stations wait a random backoff time before retransmitting.
            <br/><b>Vulnerable Time = $2 \times T_{fr}$</b>. Maximum theoretical throughput: $S_{max} = \frac{1}{2e} \approx 0.184$ (<b>18.4%</b>).
        </li>
        <li><b>Slotted ALOHA:</b> Time is divided into discrete slots equal to $T_{fr}$. A station can transmit only at the beginning of a time slot. Synchronized clocks are required.
            <br/><b>Vulnerable Time = $1 \times T_{fr}$</b>. Maximum throughput: $S_{max} = \frac{1}{e} \approx 0.368$ (<b>36.8% &mdash; double that of Pure ALOHA!</b>).
        </li>
    </ul>

    <h4>2. CSMA (Carrier Sense Multiple Access)</h4>
    <p>
        Principle: <i>"Sense before transmit"</i> (or <i>"Listen before speaking"</i>). A station monitors the channel to verify if it is idle or busy.
    </p>
    <ul>
        <li><b>1-Persistent CSMA:</b> If channel is idle, transmit immediately with probability 1. If busy, keep continuously sensing until it becomes idle, then transmit. High collision probability if two stations were waiting for the same channel to free up.</li>
        <li><b>Non-Persistent CSMA:</b> If idle, transmit immediately. If busy, wait a random amount of time and sense again. Reduces collisions significantly, but introduces idle channel wastage.</li>
        <li><b>p-Persistent CSMA:</b> Used in slotted channels. If idle, transmit with probability $p$; with probability $(1-p)$, wait for the next slot. Minimizes collisions while maximizing channel utilization.</li>
    </ul>

    <h4>3. CSMA/CD (Collision Detection &mdash; IEEE 802.3 Wired Ethernet)</h4>
    <p>
        Principle: <i>"Listen while talking"</i>. Stations monitor the cable voltage while transmitting. If the observed voltage doubles (signaling collision), transmission is halted immediately, a <b>32-bit Jamming Signal</b> is broadcast to alert all nodes, and the station executes the <b>Binary Exponential Backoff</b> algorithm ($0 \le k \le 2^c - 1$, wait $k \times 512$ bit times).
    </p>
    <div class="formula-box">
        <b>Minimum Frame Size Condition in CSMA/CD:</b><br/>
        To ensure a transmitting station detects collisions before finishing transmission:<br/>
        <b>T_frame &ge; 2 &times; T_propagation</b> &nbsp;&implies;&nbsp; <b>L_min &ge; 2 &times; Propagation_Delay &times; Bandwidth</b><br/>
        For standard 10 Mbps Ethernet: Minimum frame size = 64 bytes (512 bits).
    </div>

    <h4>4. CSMA/CA (Collision Avoidance &mdash; IEEE 802.11 Wireless LAN)</h4>
    <p>
        In wireless networks, collision detection is impossible because a station's own high-power transmission drowns out any weak incoming collision signal from another station. Hence, collisions must be avoided before they occur:
    </p>
    <ul>
        <li><b>Interframe Space (IFS):</b> Station waits until the channel is idle for a duration equal to IFS (e.g., DIFS).</li>
        <li><b>Contention Window:</b> Expands exponentially if collisions occur; counts down when the channel is idle.</li>
        <li><b>RTS/CTS Handshake:</b> Solves the <b>Hidden Terminal Problem</b>. Sender broadcasts a short <i>Request to Send (RTS)</i> frame. Receiver responds with a <i>Clear to Send (CTS)</i> frame. All neighboring nodes overhearing CTS silence their transmitters for the reserved duration (NAV &mdash; Network Allocation Vector).</li>
        <li><b>Mandatory Acknowledgments (ACK):</b> Every transmitted data frame must be explicitly acknowledged by the receiver.</li>
    </ul>

    <h3 class="sub-section-title">4.2 Controlled Access Protocols</h3>
    <ul>
        <li><b>Reservation:</b> Stations divide time into intervals with a reservation frame preceding data frames. Each station reserves a slot in advance by setting a bit.</li>
        <li><b>Polling:</b> One primary station and multiple secondary stations. The primary uses <i>Poll</i> to ask secondaries if they have data to send, and <i>Select</i> when sending data to a secondary.</li>
        <li><b>Token Passing:</b> Stations are organized in a logical ring. A special small frame called the <b>Token</b> circulates from station to station. Only the node currently possessing the token is permitted to transmit data. After transmitting or when its Token Holding Timer expires, it forwards the token to its downstream neighbor. Eliminates collisions completely.</li>
    </ul>

    <h2 class="section-title">5. Point-to-Point Protocol (PPP) (Ch. 11.4)</h2>
    <p>
        The <b>Point-to-Point Protocol (PPP)</b> is the dominant data link protocol used for establishing direct connections between two nodes (e.g., home PC to Internet Service Provider over DSL, cable modem, or leased lines).
    </p>
    <ul>
        <li><b>Services Provided by PPP:</b> Framing, bit/byte stuffing, link quality testing, authentication (PAP/CHAP), network layer protocol negotiation and multiplexing (IPv4, IPv6, AppleTalk).</li>
        <li><b>Services NOT Provided:</b> No flow control (relies on higher layers), no error correction (simple CRC error detection only; damaged frames are silently dropped), no addressing (simple point-to-point link).</li>
        <li><b>PPP Architecture:</b>
            <ul>
                <li><b>LCP (Link Control Protocol):</b> Responsible for establishing, configuring, testing, and terminating the data link.</li>
                <li><b>Authentication Protocols:</b> <b>PAP</b> (Password Authentication Protocol &mdash; plain text 2-way handshake) and <b>CHAP</b> (Challenge Handshake Authentication Protocol &mdash; secure 3-way handshake with MD5 hashing).</li>
                <li><b>NCP (Network Control Protocols):</b> Multiple protocols (like IPCP) that configure network-layer settings (e.g., dynamically assigning IP addresses to the client).</li>
            </ul>
        </li>
        <li><b>PPP Transition Phases:</b> <code>Dead &rarr; Establish (LCP) &rarr; Authenticate (PAP/CHAP) &rarr; Network (NCP) &rarr; Open (Data Transfer) &rarr; Terminate &rarr; Dead</code>.</li>
    </ul>
    """
    return (content.replace('<!-- FIG_CRC -->', fig_crc_division()).replace('<!-- FIG_FRAME -->', fig_framing_bit_stuffing()).replace('<!-- FIG_SLIDE -->', fig_sliding_window_protocols()).replace('<!-- FIG_MAC -->', fig_mac_protocols()))
