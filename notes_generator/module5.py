"""
Module 5: Application Layer - Client-Server Programming, HTTP & WWW, FTP, Electronic Mail, DNS, TELNET, and SSH.
"""
from diagrams import fig_dns_resolution, fig_email_architecture

def get_module_5_content():
    content = r"""
    <h1 class="module-title">MODULE 5 &mdash; Application Layer: HTTP, FTP, Email, DNS, TELNET & SSH</h1>

    <div class="eli5-box">
        <div class="title">💡 ELI5: What is the Application Layer? (The Restaurant Analogy)</div>
        All the lower layers (Physical, Data Link, Network, Transport) are like the kitchen staff, trucks, roads, and delivery boxes.
        The <b>Application Layer</b> is the actual meal and the menu you interact with!
        • When you order a burger (<b>HTTP</b>), the waiter brings you a web page with pictures and text.
        • When you send a letter to the chef (<b>Email</b>), the postman drops it in the kitchen mailbox.
        • When you look up a restaurant in the phone directory (<b>DNS</b>), you translate the name "Joe's Diner" into an actual street address (IP address).
        • When you log into the kitchen's computer securely from home (<b>SSH</b>), you use a locked, encrypted tunnel so nobody can spy on the secret recipes!
    </div>

    <h2 class="section-title">1. Introduction to the Application Layer & Client-Server Programming (Ch. 25.1 & 25.2)</h2>
    <p>
        The Application Layer is the top layer in both the OSI and TCP/IP protocol suites. It provides network services directly to end-user software programs.
    </p>

    <h3 class="sub-section-title">1.1 Application Architectures</h3>
    <ul>
        <li><b>Client-Server Architecture:</b> A centralized, dedicated host called the <b>Server</b> is always turned on and listens on a well-known port. Multiple <b>Clients</b> initiate contact with the server to request resources. Clients do not communicate directly with each other (e.g., Web servers, Email servers, Database servers).</li>
        <li><b>Peer-to-Peer (P2P) Architecture:</b> There is no central dedicated server. Arbitrary pairs of connected end-hosts called <b>peers</b> communicate directly with each other and share resources (storage, bandwidth). Highly scalable, but harder to manage and secure (e.g., BitTorrent).</li>
        <li><b>Hybrid Architecture:</b> Combines both paradigms &mdash; a central server handles authentication and directory indexing, while file transfers take place directly peer-to-peer (e.g., Skype, early Napster).</li>
    </ul>

    <h3 class="sub-section-title">1.2 Client-Server Programming via Sockets</h3>
    <p>
        A <b>Socket</b> is the software abstraction and Application Programming Interface (API) between an application process and the underlying transport layer.
    </p>
    <ul>
        <li><b>TCP Socket Life Cycle:</b>
            <ol>
                <li><i>Server:</i> Calls <code>socket()</code> &rarr; <code>bind()</code> to port &rarr; <code>listen()</code> for incoming requests &rarr; <code>accept()</code> (blocks waiting for a client).</li>
                <li><i>Client:</i> Calls <code>socket()</code> &rarr; <code>connect()</code> to server IP and port (triggers TCP 3-way handshake).</li>
                <li><i>Data Exchange:</i> Both sides call <code>send()</code> / <code>write()</code> and <code>recv()</code> / <code>read()</code> over the established full-duplex stream.</li>
                <li><i>Termination:</i> Calling <code>close()</code> tears down the connection (4-way handshake).</li>
            </ol>
        </li>
        <li><b>Concurrent vs Iterative Servers:</b>
            <ul>
                <li><i>Iterative Server:</i> Handles one client request to completion before accepting the next client. Inefficient if requests take long.</li>
                <li><i>Concurrent Server:</i> The main process accepts incoming connections and immediately spawns a new child thread/process to handle that specific client, returning to listen on the main port. Enables serving thousands of concurrent clients.</li>
            </ul>
        </li>
    </ul>

    <h2 class="section-title">2. World Wide Web (WWW) and HTTP (Ch. 26.1)</h2>
    <p>
        The <b>World Wide Web</b> is a distributed client-server information repository where documents (web pages) are linked together via <b>Hyperlinks</b>. A web client is called a <b>Browser</b>; a web server is called an <b>HTTP Server</b>.
    </p>

    <h3 class="sub-section-title">2.1 Uniform Resource Locator (URL)</h3>
    <p>A standard identifier used to locate web resources: <code>protocol://host:port/path?query#fragment</code></p>
    <ul>
        <li><i>protocol:</i> Transfer protocol (e.g., <code>http</code>, <code>https</code>).</li>
        <li><i>host:</i> Domain name or IP address of the server (e.g., <code>www.example.com</code>).</li>
        <li><i>port:</i> Optional port number (default 80 for HTTP, 443 for HTTPS).</li>
        <li><i>path:</i> Hierarchical location of the file on the server (e.g., <code>/courses/cn/notes.html</code>).</li>
    </ul>

    <h3 class="sub-section-title">2.2 HTTP: Hypertext Transfer Protocol</h3>
    <p>
        HTTP is a stateless, application-level request-reply protocol running over <b>TCP (Port 80)</b>.
    </p>
    <ul>
        <li><b>Stateless Nature:</b> The server maintains no memory of past client requests. If a client requests the same web page 10 times in a second, the server treats each request as a completely new transaction. State is preserved using <b>Cookies</b> (small state tokens stored on the client browser).</li>
        <li><b>Non-Persistent vs Persistent HTTP:</b>
            <ul>
                <li><b>Non-Persistent HTTP (HTTP/1.0):</b> A brand new TCP connection is opened for <i>every single object</i> (HTML file, image, CSS script). Each object requires $2 \times \text{RTT} + \text{transmission time}$ ($1 \text{ RTT}$ for TCP handshake $+ 1 \text{ RTT}$ for HTTP request/response). Massive server overhead and latency.</li>
                <li><b>Persistent HTTP (HTTP/1.1):</b> The server leaves the TCP connection open after sending a response. Multiple subsequent requests and responses can be transferred over the <b>same single TCP connection</b>. Supports <b>Pipelining</b> (sending multiple requests back-to-back without waiting for previous replies).</li>
            </ul>
        </li>
    </ul>

    <h3 class="sub-section-title">2.3 HTTP Request and Response Messages</h3>
    <h4>HTTP Request Message Format:</h4>
    <pre>
GET /index.html HTTP/1.1                &larr; Request Line (Method, URL, Version)
Host: www.vtu.ac.in                     &larr; Header Lines (Key: Value)
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml
Connection: keep-alive
[CRLF]                                  &larr; Empty Blank Line (Separates header & body)
[Optional Entity Body for POST/PUT]     &larr; Entity Body (Form data, JSON, uploads)
    </pre>

    <h4>HTTP Request Methods:</h4>
    <ul>
        <li><b>GET:</b> Requests a resource from the server. Payload returned in entity body. Idempotent and safe.</li>
        <li><b>POST:</b> Submits data (form input, file uploads) to be processed by the server. Not idempotent.</li>
        <li><b>HEAD:</b> Identical to GET, but server returns <i>only the headers</i> without the entity body (used to check file size or modification date).</li>
        <li><b>PUT:</b> Uploads a replacement file to the specified URI.</li>
        <li><b>DELETE:</b> Deletes the specified file on the server.</li>
    </ul>

    <h4>HTTP Response Message & Status Codes:</h4>
    <pre>
HTTP/1.1 200 OK                         &larr; Status Line (Version, Status Code, Phrase)
Date: Fri, 20 Nov 2026 12:00:00 GMT     &larr; Header Lines
Server: Apache/2.4.41 (Ubuntu)
Content-Type: text/html; charset=UTF-8
Content-Length: 4096
[CRLF]                                  &larr; Blank Line
&lt;html&gt;&lt;body&gt;Welcome to VTU!&lt;/body&gt;&lt;/html&gt; &larr; Response Body (Web page content)
    </pre>

    <div class="key-point">
        <div class="title">🔑 Standard HTTP Status Code Classes</div>
        <ul>
            <li><b>1xx (Informational):</b> Request received, continuing process (e.g., <code>100 Continue</code>).</li>
            <li><b>2xx (Success):</b> Action successfully received and understood (e.g., <code>200 OK</code>, <code>201 Created</code>).</li>
            <li><b>3xx (Redirection):</b> Further action needed to complete request (e.g., <code>301 Moved Permanently</code>, <code>304 Not Modified</code> for web cache validation).</li>
            <li><b>4xx (Client Error):</b> Request contains bad syntax or cannot be fulfilled (e.g., <code>400 Bad Request</code>, <code>403 Forbidden</code>, <code>404 Not Found</code>).</li>
            <li><b>5xx (Server Error):</b> Server failed to fulfill an apparently valid request (e.g., <code>500 Internal Server Error</code>, <code>502 Bad Gateway</code>, <code>503 Service Unavailable</code>).</li>
        </ul>
    </div>

    <h2 class="section-title">3. File Transfer Protocol &mdash; FTP (Ch. 26.2)</h2>
    <p>
        FTP is the standard client-server protocol used for copying files from one host to another over TCP.
    </p>

    <h3 class="sub-section-title">3.1 Two-Connection Architecture: Control vs Data Connection</h3>
    <p>Unlike HTTP which transfers commands and data over the same connection, FTP establishes <b>two separate parallel TCP connections</b>:</p>
    <table>
        <tr>
            <th>Connection</th>
            <th>Default Port</th>
            <th>Persistence</th>
            <th>Function & Characteristics</th>
        </tr>
        <tr>
            <td><b>Control Connection</b></td>
            <td><b>Port 21</b></td>
            <td><b>Persistent</b> for entire session</td>
            <td>Transmits user credentials, navigation commands (<code>USER</code>, <code>PASS</code>, <code>CWD</code>), and 3-digit server status codes. Carries 7-bit ASCII control traffic (called <i>Out-of-Band</i> control).</td>
        </tr>
        <tr>
            <td><b>Data Connection</b></td>
            <td><b>Port 20</b> (Active) or Dynamic (Passive)</td>
            <td><b>Non-Persistent</b> (opens and closes per file)</td>
            <td>Transfers the actual raw file data or directory listings. A new data connection is opened whenever a file transfer is requested (<code>RETR</code>, <code>STOR</code>, <code>LIST</code>) and closed as soon as the file ends.</td>
        </tr>
    </table>

    <h3 class="sub-section-title">3.2 Active Mode vs Passive Mode</h3>
    <ul>
        <li><b>Active Mode (Traditional):</b> Client connects to server Port 21 and tells the server its own client data port using the <code>PORT</code> command. The server initiates an outbound TCP connection from <b>Port 20</b> back to the client's port.
            <br/><i>The Firewall Problem:</i> Client-side firewalls and NAT routers block unsolicited incoming connections from the server!</li>
        <li><b>Passive Mode (PASV &mdash; Modern Standard):</b> The client sends the <code>PASV</code> command. The server opens an ephemeral high-numbered port (e.g., 50201) and informs the client. The <b>client initiates both the control and data connections</b>, bypassing client firewall blocks completely!</li>
    </ul>

    <h2 class="section-title">4. Electronic Mail: SMTP, MIME, POP3, and IMAP4 (Ch. 26.3)</h2>
    <!-- FIG_EMAIL -->

    <h3 class="sub-section-title">4.1 Email Architecture & Components</h3>
    <ul>
        <li><b>User Agent (UA):</b> The software program used by the human to compose, read, and reply to messages (e.g., Thunderbird, Outlook, Gmail web app).</li>
        <li><b>Mail Transfer Agent (MTA):</b> Background server software that pushes email across the Internet from source server to destination server (e.g., Postfix, Sendmail, Exim).</li>
        <li><b>Message Access Agent (MAA):</b> Server software that authenticates users and delivers stored messages from the server mailbox to the client's User Agent (POP3, IMAP4).</li>
        <li><b>Spool & Mailbox:</b> The spool stores outgoing emails waiting to be dispatched; the mailbox holds incoming unread emails for that specific user.</li>
    </ul>

    <h3 class="sub-section-title">4.2 Simple Mail Transfer Protocol (SMTP)</h3>
    <p>
        SMTP is a <b>Push Protocol</b> operating on <b>TCP Port 25</b> (submission port 587).
    </p>
    <ul>
        <li>Used to push emails from sender's UA to sender's mail server, and between intermediate mail servers across the Internet.</li>
        <li><b>7-Bit ASCII Limitation:</b> SMTP was originally designed only for plain English text. It cannot transmit binary files, images, attachments, or non-English alphabets directly.</li>
        <li><b>SMTP Handshake Commands:</b>
            <pre>
S: 220 mail.receiver.com ESMTP Postfix
C: HELO mail.sender.com
S: 250 Hello mail.sender.com, pleased to meet you
C: MAIL FROM: &lt;alice@sender.com&gt;
S: 250 2.1.0 Ok
C: RCPT TO: &lt;bob@receiver.com&gt;
S: 250 2.1.5 Ok
C: DATA
S: 354 End data with &lt;CR&gt;&lt;LF&gt;.&lt;CR&gt;&lt;LF&gt;
C: Subject: Computer Networks Notes
C: Hello Bob, here are the Module 1-5 notes!
C: .
S: 250 2.0.0 Ok: queued as 4QZ9
C: QUIT
S: 221 Bye
            </pre>
        </li>
    </ul>

    <h3 class="sub-section-title">4.3 MIME (Multipurpose Internet Mail Extensions)</h3>
    <p>
        MIME transforms non-ASCII binary attachments (PDFs, images, audio, international characters) into 7-bit ASCII format so that legacy SMTP servers can transmit them without modification.
    </p>
    <ul>
        <li><b>MIME Headers Added:</b>
            <ul>
                <li><code>MIME-Version: 1.0</code></li>
                <li><code>Content-Type: image/png</code> (or <code>application/pdf</code>, <code>multipart/mixed</code>)</li>
                <li><code>Content-Transfer-Encoding: base64</code> (encodes binary data using 64 printable ASCII characters).</li>
            </ul>
        </li>
    </ul>

    <h3 class="sub-section-title">4.4 Message Access Protocols: POP3 vs IMAP4</h3>
    <p>SMTP cannot be used to pull emails to a mobile phone or laptop because user devices are not always powered on and have dynamically changing IP addresses. A <b>Pull Protocol</b> is required:</p>
    <table>
        <tr>
            <th>Feature</th>
            <th>POP3 (Post Office Protocol v3)</th>
            <th>IMAP4 (Internet Message Access Protocol v4)</th>
        </tr>
        <tr>
            <td><b>Default Port</b></td>
            <td><b>Port 110</b> (SSL/TLS 995)</td>
            <td><b>Port 143</b> (SSL/TLS 993)</td>
        </tr>
        <tr>
            <td><b>Storage Location</b></td>
            <td>Downloads emails to local machine; deletes from server (or download-and-keep).</td>
            <td><b>Stores all emails permanently on the server</b>.</td>
        </tr>
        <tr>
            <td><b>Multiple Device Sync</b></td>
            <td>Very poor &mdash; if read on laptop, status does not sync to phone.</td>
            <td><b>Seamless synchronization</b> across phones, tablets, and PCs.</td>
        </tr>
        <tr>
            <td><b>Folder Organization</b></td>
            <td>Folders exist only on the local PC.</td>
            <td>Users can create, rename, and organize folders <b>directly on server</b>.</td>
        </tr>
        <tr>
            <td><b>Partial Download</b></td>
            <td>Must download the full email and all attachments.</td>
            <td>Can download <b>only headers</b> or view text without downloading large attachments.</td>
        </tr>
    </table>

    <h2 class="section-title">5. Domain Name System &mdash; DNS (Ch. 26.4)</h2>
    <p>
        Humans prefer intuitive textual domain names (<code>www.google.com</code>), but network routers require 32-bit (IPv4) or 128-bit (IPv6) numerical IP addresses. The <b>Domain Name System (DNS)</b> is a hierarchical, distributed database that translates domain names into IP addresses and vice versa, operating on <b>UDP and TCP Port 53</b>.
    </p>

    <h3 class="sub-section-title">5.1 The Hierarchical Domain Name Space</h3>
    <ul>
        <li><b>Root Domain (<code>.</code>):</b> The top of the tree, denoted by an unnamed string or dot.</li>
        <li><b>Top-Level Domains (TLD):</b>
            <ul>
                <li><i>Generic TLDs (gTLD):</i> <code>.com</code> (commercial), <code>.edu</code> (education), <code>.org</code> (non-profit), <code>.gov</code>, <code>.net</code>.</li>
                <li><i>Country-Code TLDs (ccTLD):</i> <code>.in</code> (India), <code>.uk</code> (UK), <code>.jp</code> (Japan), <code>.us</code>.</li>
            </ul>
        </li>
        <li><b>Second-Level Domains:</b> Assigned to organizations under a TLD (e.g., <code>vtu.ac.in</code>, <code>google.com</code>).</li>
        <li><b>FQDN vs PQDN:</b>
            <ul>
                <li><i>Fully Qualified Domain Name (FQDN):</i> Ends with a dot, specifying full path from leaf to root (e.g., <code>www.vtu.ac.in.</code>).</li>
                <li><i>Partially Qualified Domain Name (PQDN):</i> Incomplete relative domain name (e.g., <code>www</code> or <code>vtu</code>).</li>
            </ul>
        </li>
    </ul>

    <h3 class="sub-section-title">5.2 Types of DNS Servers & Resolution</h3>
    <!-- FIG_DNS -->

    <ul>
        <li><b>1. Root Name Servers:</b> 13 logical root server addresses (named <code>[a-m].root-servers.net</code>), replicated worldwide using anycast routing. They know the addresses of all TLD servers.</li>
        <li><b>2. TLD Name Servers:</b> Responsible for specific TLDs (e.g., all <code>.com</code> or <code>.in</code> domains). Direct queries to authoritative servers.</li>
        <li><b>3. Authoritative Name Servers:</b> Maintained by organizations or DNS hosting providers; holds the definitive master records for that domain. Divided into <b>Primary (Master)</b> and <b>Secondary (Slave)</b> servers for fault tolerance.</li>
        <li><b>4. Local DNS Resolver:</b> Maintained by your ISP or campus. Intercepts client queries, checks local cache, and navigates the global hierarchy on the client's behalf.</li>
    </ul>

    <h3 class="sub-section-title">5.3 DNS Resource Records (RR)</h3>
    <p>The DNS database stores entries called Resource Records formatted as: <code>(Name, Value, Type, TTL)</code></p>
    <table>
        <tr>
            <th>Record Type</th>
            <th>Meaning</th>
            <th>Example Record</th>
        </tr>
        <tr>
            <td><b>A</b></td>
            <td>IPv4 Host Address mapping</td>
            <td><code>vtu.ac.in. &nbsp;IN &nbsp;A &nbsp;14.139.155.234</code></td>
        </tr>
        <tr>
            <td><b>AAAA</b></td>
            <td>IPv6 Host Address mapping</td>
            <td><code>google.com. &nbsp;IN &nbsp;AAAA &nbsp;2607:f8b0:4005:805::200e</code></td>
        </tr>
        <tr>
            <td><b>CNAME</b></td>
            <td>Canonical Name (Alias for true host)</td>
            <td><code>www.vtu.ac.in. &nbsp;IN &nbsp;CNAME &nbsp;vtu.ac.in.</code></td>
        </tr>
        <tr>
            <td><b>NS</b></td>
            <td>Authoritative Name Server for zone</td>
            <td><code>vtu.ac.in. &nbsp;IN &nbsp;NS &nbsp;ns1.vtu.ac.in.</code></td>
        </tr>
        <tr>
            <td><b>MX</b></td>
            <td>Mail Exchange server for domain</td>
            <td><code>vtu.ac.in. &nbsp;IN &nbsp;MX &nbsp;10 mail.vtu.ac.in.</code></td>
        </tr>
        <tr>
            <td><b>PTR</b></td>
            <td>Pointer for <b>Reverse DNS Lookup</b> (IP &rarr; Name)</td>
            <td><code>234.155.139.14.in-addr.arpa. &nbsp;IN &nbsp;PTR &nbsp;vtu.ac.in.</code></td>
        </tr>
        <tr>
            <td><b>SOA</b></td>
            <td>Start of Authority (Zone parameters, refresh timer)</td>
            <td>Specifies master server, admin email, serial number, TTL.</td>
        </tr>
        <tr>
            <td><b>TXT</b></td>
            <td>Arbitrary text (SPF records, domain verification)</td>
            <td><code>v=spf1 include:_spf.google.com ~all</code></td>
        </tr>
    </table>

    <h2 class="section-title">6. TELNET & Secure Shell &mdash; SSH (Ch. 26.5 & 26.6)</h2>

    <h3 class="sub-section-title">6.1 TELNET (Teletype Network)</h3>
    <p>
        TELNET is a legacy client-server application developed in 1969 to allow a user on a local computer to log into and execute commands on a remote computer across TCP <b>Port 23</b>.
    </p>
    <ul>
        <li><b>Network Virtual Terminal (NVT):</b> To enable heterogeneous terminals to communicate with different operating systems, TELNET invented the NVT. The client translates local keystrokes into standard NVT characters; the server converts NVT characters into the host operating system's internal character format.</li>
        <li><b>Command Embedding:</b> Uses a special escape byte called <b>IAC (Interpret As Command &mdash; byte value 255 / 0xFF)</b> to send out-of-band signals (e.g., interrupt process, suspend).</li>
        <li><b>Fatal Flaw &mdash; Complete Lack of Security:</b> TELNET transmits <b>all data in plaintext</b> &mdash; including user passwords and root terminal commands. Any eavesdropper running a packet sniffer (Wireshark) on the local network or public Wi-Fi can capture usernames and passwords in clear text!</li>
    </ul>

    <h3 class="sub-section-title">6.2 Secure Shell (SSH)</h3>
    <p>
        <b>SSH</b> was designed as a cryptographically secure, encrypted replacement for TELNET, rlogin, and FTP. Operates over <b>TCP Port 22</b>.
    </p>
    <h4>SSH Three-Layer Architecture:</h4>
    <ol>
        <li><b>SSH Transport Layer Protocol:</b> Establishes a secure, confidential communication channel over an insecure network. Handles:
            <ul>
                <li><i>Server Authentication:</i> Server proves its identity using host public keys (preventing man-in-the-middle attacks).</li>
                <li><i>Key Exchange:</i> Uses Diffie-Hellman to negotiate a shared session key without transmitting it over the wire.</li>
                <li><i>Symmetric Encryption:</i> Encrypts all data payload (AES, ChaCha20).</li>
                <li><i>Data Integrity:</i> Every packet includes an HMAC (Hash-based Message Authentication Code) to prevent packet tampering.</li>
            </ul>
        </li>
        <li><b>SSH User Authentication Protocol:</b> Runs on top of the transport layer to authenticate the human client to the server:
            <ul>
                <li><i>Password Authentication:</i> Transmitted securely inside the encrypted channel.</li>
                <li><i>Public-Key Authentication:</i> Client generates an asymmetric key pair (RSA or Ed25519). The public key is stored in the server's <code>~/.ssh/authorized_keys</code>. The client proves ownership of the private key via digital signature challenge &mdash; eliminates passwords entirely!</li>
            </ul>
        </li>
        <li><b>SSH Connection Protocol:</b> Multiplexes multiple logical communication channels over the single encrypted connection:
            <ul>
                <li>Interactive terminal shell sessions.</li>
                <li>Remote single-command execution.</li>
                <li>Secure file transfer (SFTP, SCP).</li>
                <li><b>Port Forwarding / SSH Tunneling:</b>
                    <ul>
                        <li><i>Local Port Forwarding (<code>ssh -L</code>):</i> Forwards a port from client PC through the encrypted SSH tunnel to a private server inside a firewall.</li>
                        <li><i>Remote Port Forwarding (<code>ssh -R</code>):</i> Forwards a port on the remote server back to a local development machine.</li>
                    </ul>
                </li>
            </ul>
        </li>
    </ol>

    <div class="exam-tip">
        <div class="title">⭐ High-Yield Exam Comparison: TELNET vs SSH</div>
        <table>
            <tr>
                <th>Feature</th>
                <th>TELNET</th>
                <th>SSH (Secure Shell)</th>
            </tr>
            <tr>
                <td><b>Port Number</b></td>
                <td><b>Port 23</b></td>
                <td><b>Port 22</b></td>
            </tr>
            <tr>
                <td><b>Data Security & Encryption</b></td>
                <td>No encryption (Plaintext transmission of passwords and commands)</td>
                <td><b>Full end-to-end encryption</b> (AES, 3DES, ChaCha20)</td>
            </tr>
            <tr>
                <td><b>Data Integrity</b></td>
                <td>None (Vulnerable to packet tampering & injection)</td>
                <td>Cryptographic <b>HMAC</b> on every packet</td>
            </tr>
            <tr>
                <td><b>Authentication</b></td>
                <td>Plaintext password only</td>
                <td>Public-key cryptography (Ed25519/RSA), Passwords, Kerberos</td>
            </tr>
            <tr>
                <td><b>Port Forwarding / Tunneling</b></td>
                <td>Not supported</td>
                <td><b>Fully supported</b> (Local, Remote, and Dynamic SOCKS proxy)</td>
            </tr>
            <tr>
                <td><b>Modern Recommendation</b></td>
                <td>Obsolete and deprecated (never use over public networks)</td>
                <td>Universal industry standard for remote administration</td>
            </tr>
        </table>
    </div>
    """
    return (content.replace('<!-- FIG_DNS -->', fig_dns_resolution()).replace('<!-- FIG_EMAIL -->', fig_email_architecture()))
