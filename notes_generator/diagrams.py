"""
High quality inline SVG diagram generators for Computer Networks study notes.
"""

def get_svg_wrapper(svg_str, fig_num, caption):
    return f"""
    <div class="diagram-container">
        {svg_str}
        <div class="diagram-caption">Fig {fig_num}: {caption}</div>
    </div>
    """

def fig_data_comm_components():
    svg = """
    <svg width="650" height="180" viewBox="0 0 650 180" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e40af" />
            </marker>
        </defs>
        <!-- Protocol Top -->
        <rect x="50" y="10" width="120" height="30" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="110" y="30" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#92400e" text-anchor="middle">Protocol Rule 1</text>
        
        <rect x="480" y="10" width="120" height="30" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="540" y="30" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#92400e" text-anchor="middle">Protocol Rule 2</text>
        
        <line x1="170" y1="25" x2="480" y2="25" stroke="#d97706" stroke-width="1.5" stroke-dasharray="4,4"/>
        <text x="325" y="20" font-family="'Segoe UI', sans-serif" font-size="10" fill="#b45309" text-anchor="middle">Governing Rules & Conventions</text>

        <!-- Sender -->
        <rect x="40" y="70" width="140" height="70" rx="6" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>
        <text x="110" y="100" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#1e3a8a" text-anchor="middle">SENDER</text>
        <text x="110" y="122" font-family="'Segoe UI', sans-serif" font-size="10" fill="#1e40af" text-anchor="middle">(PC, Phone, Camera)</text>

        <!-- Receiver -->
        <rect x="470" y="70" width="140" height="70" rx="6" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>
        <text x="540" y="100" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#1e3a8a" text-anchor="middle">RECEIVER</text>
        <text x="540" y="122" font-family="'Segoe UI', sans-serif" font-size="10" fill="#1e40af" text-anchor="middle">(Server, Workstation)</text>

        <!-- Transmission Medium -->
        <line x1="180" y1="105" x2="465" y2="105" stroke="#1e40af" stroke-width="3" marker-end="url(#arrow)"/>
        <text x="325" y="98" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#1e40af" text-anchor="middle">TRANSMISSION MEDIUM</text>
        <text x="325" y="124" font-family="'Segoe UI', sans-serif" font-size="9.5" fill="#475569" text-anchor="middle">(Cable, Optical Fiber, Wireless Waves)</text>

        <!-- Message Box floating on medium -->
        <rect x="275" y="132" width="100" height="32" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
        <text x="325" y="152" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d" text-anchor="middle">MESSAGE</text>
    </svg>
    """
    return get_svg_wrapper(svg, "1.1", "The Five Fundamental Components of Data Communication")

def fig_topologies():
    svg = """
    <svg width="680" height="230" viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg">
        <!-- 1. MESH -->
        <g transform="translate(10, 10)">
            <rect x="0" y="0" width="150" height="190" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
            <text x="75" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Mesh Topology</text>
            <line x1="45" y1="50" x2="105" y2="50" stroke="#64748b" stroke-width="1.5"/>
            <line x1="45" y1="50" x2="45" y2="120" stroke="#64748b" stroke-width="1.5"/>
            <line x1="45" y1="50" x2="105" y2="120" stroke="#64748b" stroke-width="1.5"/>
            <line x1="105" y1="50" x2="45" y2="120" stroke="#64748b" stroke-width="1.5"/>
            <line x1="105" y1="50" x2="105" y2="120" stroke="#64748b" stroke-width="1.5"/>
            <line x1="45" y1="120" x2="105" y2="120" stroke="#64748b" stroke-width="1.5"/>
            <circle cx="45" cy="50" r="12" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <circle cx="105" cy="50" r="12" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <circle cx="45" cy="120" r="12" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <circle cx="105" cy="120" r="12" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <text x="75" y="155" font-family="'Segoe UI', sans-serif" font-size="9" fill="#334155" text-anchor="middle">Dedicated point-to-point</text>
            <text x="75" y="172" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Links = n(n-1)/2</text>
        </g>

        <!-- 2. STAR -->
        <g transform="translate(175, 10)">
            <rect x="0" y="0" width="150" height="190" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
            <text x="75" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Star Topology</text>
            <rect x="58" y="75" width="34" height="26" rx="3" fill="#e2e8f0" stroke="#475569" stroke-width="1.5"/>
            <text x="75" y="92" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e293b" text-anchor="middle">HUB</text>
            <line x1="75" y1="75" x2="75" y2="45" stroke="#64748b" stroke-width="1.5"/>
            <line x1="75" y1="101" x2="75" y2="135" stroke="#64748b" stroke-width="1.5"/>
            <line x1="58" y1="88" x2="30" y2="88" stroke="#64748b" stroke-width="1.5"/>
            <line x1="92" y1="88" x2="120" y2="88" stroke="#64748b" stroke-width="1.5"/>
            <circle cx="75" cy="45" r="10" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <circle cx="75" cy="135" r="10" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <circle cx="30" cy="88" r="10" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <circle cx="120" cy="88" r="10" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <text x="75" y="160" font-family="'Segoe UI', sans-serif" font-size="9" fill="#334155" text-anchor="middle">Central Controller (Hub/Switch)</text>
            <text x="75" y="175" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Links = n</text>
        </g>

        <!-- 3. BUS -->
        <g transform="translate(340, 10)">
            <rect x="0" y="0" width="155" height="190" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
            <text x="77" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Bus Topology</text>
            <line x1="15" y1="90" x2="140" y2="90" stroke="#0f172a" stroke-width="4"/>
            <rect x="10" y="85" width="5" height="10" fill="#0f172a"/>
            <rect x="140" y="85" width="5" height="10" fill="#0f172a"/>
            <!-- Drop lines -->
            <line x1="35" y1="90" x2="35" y2="55" stroke="#64748b" stroke-width="1.5"/>
            <line x1="80" y1="90" x2="80" y2="55" stroke="#64748b" stroke-width="1.5"/>
            <line x1="120" y1="90" x2="120" y2="55" stroke="#64748b" stroke-width="1.5"/>
            <line x1="55" y1="90" x2="55" y2="125" stroke="#64748b" stroke-width="1.5"/>
            <line x1="100" y1="90" x2="100" y2="125" stroke="#64748b" stroke-width="1.5"/>
            <circle cx="35" cy="50" r="8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <circle cx="80" cy="50" r="8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <circle cx="120" cy="50" r="8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <circle cx="55" cy="130" r="8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <circle cx="100" cy="130" r="8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <text x="77" y="160" font-family="'Segoe UI', sans-serif" font-size="9" fill="#334155" text-anchor="middle">Backbone & Drop lines</text>
            <text x="77" y="175" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Multipoint connection</text>
        </g>

        <!-- 4. RING -->
        <g transform="translate(510, 10)">
            <rect x="0" y="0" width="155" height="190" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
            <text x="77" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Ring Topology</text>
            <circle cx="77" cy="90" r="42" fill="none" stroke="#64748b" stroke-width="2"/>
            <circle cx="77" cy="48" r="9" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <circle cx="119" cy="90" r="9" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <circle cx="77" cy="132" r="9" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <circle cx="35" cy="90" r="9" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
            <text x="77" y="160" font-family="'Segoe UI', sans-serif" font-size="9" fill="#334155" text-anchor="middle">Repeater loop (token flow)</text>
            <text x="77" y="175" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Unidirectional / Bidirectional</text>
        </g>
    </svg>
    """
    return get_svg_wrapper(svg, "1.2", "Fundamental Network Physical Topologies")

def fig_osi_vs_tcpip():
    svg = """
    <svg width="670" height="280" viewBox="0 0 670 280" xmlns="http://www.w3.org/2000/svg">
        <!-- OSI Model (Left) -->
        <text x="140" y="25" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f2b5c" text-anchor="middle">OSI Model (7 Layers)</text>
        <rect x="30" y="40" width="220" height="28" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
        <text x="140" y="58" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#1e40af" text-anchor="middle">7. Application Layer</text>

        <rect x="30" y="72" width="220" height="28" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
        <text x="140" y="90" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#1e40af" text-anchor="middle">6. Presentation Layer</text>

        <rect x="30" y="104" width="220" height="28" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
        <text x="140" y="122" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#1e40af" text-anchor="middle">5. Session Layer</text>

        <rect x="30" y="136" width="220" height="28" rx="4" fill="#e0e7ff" stroke="#4f46e5" stroke-width="1.5"/>
        <text x="140" y="154" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#3730a3" text-anchor="middle">4. Transport Layer</text>

        <rect x="30" y="168" width="220" height="28" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="140" y="186" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#92400e" text-anchor="middle">3. Network Layer</text>

        <rect x="30" y="200" width="220" height="28" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
        <text x="140" y="218" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#166534" text-anchor="middle">2. Data Link Layer</text>

        <rect x="30" y="232" width="220" height="28" rx="4" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
        <text x="140" y="250" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#334155" text-anchor="middle">1. Physical Layer</text>

        <!-- Middle Mapping Lines -->
        <path d="M 250 86 C 300 86, 300 70, 350 70" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>
        <path d="M 250 150 C 300 150, 300 130, 350 130" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>
        <path d="M 250 182 C 300 182, 300 172, 350 172" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>
        <path d="M 250 214 C 300 214, 300 214, 350 214" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>
        <path d="M 250 246 C 300 246, 300 250, 350 250" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>

        <!-- TCP/IP Model (Right) -->
        <text x="470" y="25" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f2b5c" text-anchor="middle">TCP/IP Protocol Suite (5 Layers)</text>
        <rect x="350" y="40" width="240" height="60" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
        <text x="470" y="66" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#1e40af" text-anchor="middle">5. Application Layer</text>
        <text x="470" y="85" font-family="'Segoe UI', sans-serif" font-size="9" fill="#1e3a8a" text-anchor="middle">(HTTP, FTP, DNS, SMTP, SSH) - [Data / Message]</text>

        <rect x="350" y="105" width="240" height="42" rx="4" fill="#e0e7ff" stroke="#4f46e5" stroke-width="1.5"/>
        <text x="470" y="125" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#3730a3" text-anchor="middle">4. Transport Layer</text>
        <text x="470" y="141" font-family="'Segoe UI', sans-serif" font-size="9" fill="#312e81" text-anchor="middle">(TCP, UDP) - [Segments / User Datagrams]</text>

        <rect x="350" y="152" width="240" height="42" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="470" y="172" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#92400e" text-anchor="middle">3. Network Layer</text>
        <text x="470" y="188" font-family="'Segoe UI', sans-serif" font-size="9" fill="#78350f" text-anchor="middle">(IPv4, IPv6, ICMP, Routing) - [Packets / Datagrams]</text>

        <rect x="350" y="199" width="240" height="34" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
        <text x="470" y="215" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#166534" text-anchor="middle">2. Data Link Layer</text>
        <text x="470" y="228" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#14532d" text-anchor="middle">(Ethernet, Wi-Fi, PPP, HDLC) - [Frames]</text>

        <rect x="350" y="238" width="240" height="30" rx="4" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
        <text x="470" y="253" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#334155" text-anchor="middle">1. Physical Layer</text>
        <text x="470" y="264" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#1e293b" text-anchor="middle">(Cables, Fiber, Radio signals) - [Bits / Signals]</text>
    </svg>
    """
    return get_svg_wrapper(svg, "1.3", "Comparison of the 7-Layer OSI Reference Model and 5-Layer TCP/IP Suite with PDUs")

def fig_packet_switching():
    svg = """
    <svg width="660" height="200" viewBox="0 0 660 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arr-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb" />
            </marker>
            <marker id="arr-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
            </marker>
        </defs>
        <!-- Datagram Approach (Left) -->
        <g transform="translate(10, 10)">
            <rect x="0" y="0" width="310" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="155" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Datagram Approach (Connectionless)</text>
            <!-- Hosts -->
            <rect x="15" y="65" width="45" height="35" rx="3" fill="#dbeafe" stroke="#2563eb"/>
            <text x="37" y="86" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#1e40af" text-anchor="middle">Src</text>
            <rect x="250" y="65" width="45" height="35" rx="3" fill="#dbeafe" stroke="#2563eb"/>
            <text x="272" y="86" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#1e40af" text-anchor="middle">Dst</text>
            <!-- Routers -->
            <circle cx="105" cy="50" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="105" y="54" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">R1</text>
            <circle cx="105" cy="115" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="105" y="119" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">R2</text>
            <circle cx="195" cy="80" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="195" y="84" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">R3</text>
            <!-- Independent paths -->
            <path d="M 60 75 L 92 53 M 119 50 L 181 74 M 209 80 L 250 80" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arr-blue)"/>
            <path d="M 60 88 L 92 112 M 119 115 L 181 87" stroke="#d97706" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arr-blue)"/>
            <text x="155" y="145" font-family="'Segoe UI', sans-serif" font-size="9" fill="#334155" text-anchor="middle">Packets 1, 2, 3 take different routes</text>
            <text x="155" y="160" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#64748b" text-anchor="middle">May arrive out-of-order; No setup delay</text>
        </g>

        <!-- Virtual-Circuit Approach (Right) -->
        <g transform="translate(340, 10)">
            <rect x="0" y="0" width="310" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="155" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Virtual-Circuit Approach (Connection-Oriented)</text>
            <!-- Hosts -->
            <rect x="15" y="65" width="45" height="35" rx="3" fill="#dcfce7" stroke="#16a34a"/>
            <text x="37" y="86" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#166534" text-anchor="middle">Src</text>
            <rect x="250" y="65" width="45" height="35" rx="3" fill="#dcfce7" stroke="#16a34a"/>
            <text x="272" y="86" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#166534" text-anchor="middle">Dst</text>
            <!-- Switches -->
            <circle cx="105" cy="50" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="105" y="54" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">S1</text>
            <circle cx="105" cy="115" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="105" y="119" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">S2</text>
            <circle cx="195" cy="80" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
            <text x="195" y="84" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">S3</text>
            <!-- Single pre-established virtual circuit -->
            <path d="M 60 75 L 92 53 L 181 76 L 250 80" stroke="#16a34a" stroke-width="3" fill="none" marker-end="url(#arr-green)"/>
            <text x="155" y="145" font-family="'Segoe UI', sans-serif" font-size="9" fill="#166534" font-weight="bold" text-anchor="middle">Single Fixed Path Established (VCI Table)</text>
            <text x="155" y="160" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#64748b" text-anchor="middle">Phase 1: Setup -> Phase 2: Transfer -> Phase 3: Teardown</text>
        </g>
    </svg>
    """
    return get_svg_wrapper(svg, "1.4", "Packet Switching: Datagram Networks vs Virtual-Circuit Networks")

def fig_framing_bit_stuffing():
    svg = """
    <svg width="670" height="150" viewBox="0 0 670 150" xmlns="http://www.w3.org/2000/svg">
        <!-- Original Data -->
        <text x="20" y="30" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0f2b5c">Original User Data:</text>
        <rect x="180" y="15" width="460" height="26" rx="3" fill="#f1f5f9" stroke="#64748b" stroke-width="1"/>
        <text x="410" y="32" font-family="'Consolas', monospace" font-size="11" fill="#0f172a" text-anchor="middle">0 0 0 1 1 1 1 1 1 0 1 1 1 1 1 1 0</text>

        <!-- Arrow Stuffed -->
        <text x="80" y="75" font-family="'Segoe UI', sans-serif" font-size="10" font-style="italic" fill="#2563eb">After Bit Stuffing (Insert 0 after five consecutive 1s):</text>

        <!-- Stuffed Frame -->
        <rect x="20" y="90" width="110" height="32" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
        <text x="75" y="110" font-family="'Consolas', monospace" font-size="10.5" font-weight="bold" fill="#991b1b" text-anchor="middle">01111110 (Flag)</text>

        <rect x="135" y="90" width="400" height="32" rx="3" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
        <text x="335" y="110" font-family="'Consolas', monospace" font-size="11" fill="#0f172a" text-anchor="middle">
            0 0 0 1 1 1 1 1 <tspan fill="#dc2626" font-weight="bold">0</tspan> 1 0 1 1 1 1 1 <tspan fill="#dc2626" font-weight="bold">0</tspan> 1 0
        </text>

        <rect x="540" y="90" width="110" height="32" rx="3" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
        <text x="595" y="110" font-family="'Consolas', monospace" font-size="10.5" font-weight="bold" fill="#991b1b" text-anchor="middle">01111110 (Flag)</text>

        <text x="335" y="138" font-family="'Segoe UI', sans-serif" font-size="9" fill="#15803d" text-anchor="middle">Stuffed '0' bits (shown in red) prevent false flag pattern matches</text>
    </svg>
    """
    return get_svg_wrapper(svg, "2.1", "Bit-Oriented Framing and Bit Stuffing Mechanism")

def fig_crc_division():
    svg = """
    <svg width="650" height="190" viewBox="0 0 650 190" xmlns="http://www.w3.org/2000/svg">
        <!-- Division Layout -->
        <g transform="translate(40, 15)">
            <rect x="0" y="0" width="570" height="160" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="20" y="28" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#1e40af">Divisor: 1011  (Degree n = 3)</text>
            <text x="250" y="28" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#0f2b5c">Data: 100100  -> Append 3 zeros: 100100 000</text>

            <rect x="20" y="45" width="530" height="98" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
            <text x="35" y="68" font-family="'Consolas', monospace" font-size="11" fill="#334155">
                1011 ) 1 0 0 1 0 0 0 0 0  ( Quotient: 101011
            </text>
            <text x="80" y="86" font-family="'Consolas', monospace" font-size="11" fill="#dc2626">
                XOR   1 0 1 1
            </text>
            <text x="80" y="104" font-family="'Consolas', monospace" font-size="11" fill="#334155">
                --------------&gt; Modulo-2 Arithmetic (no carry, no borrow)
            </text>
            <text x="80" y="124" font-family="'Consolas', monospace" font-size="11" font-weight="bold" fill="#16a34a">
                Final Remainder (CRC Checksum) = 001  -&gt; Transmitted Frame = 100100 001
            </text>
        </g>
    </svg>
    """
    return get_svg_wrapper(svg, "2.2", "CRC Polynomial Modulo-2 Division Process")

def fig_sliding_window_protocols():
    svg = """
    <svg width="680" height="230" viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arr-g" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
            </marker>
            <marker id="arr-r" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
            </marker>
        </defs>

        <!-- 1. Stop-and-Wait -->
        <g transform="translate(10, 10)">
            <rect x="0" y="0" width="205" height="195" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="102" y="20" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Stop-and-Wait ARQ</text>
            <line x1="35" y1="35" x2="35" y2="175" stroke="#94a3b8" stroke-width="2"/>
            <line x1="170" y1="35" x2="170" y2="175" stroke="#94a3b8" stroke-width="2"/>
            <text x="35" y="32" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#475569" text-anchor="middle">Tx</text>
            <text x="170" y="32" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#475569" text-anchor="middle">Rx</text>
            <!-- Frame 0 -->
            <line x1="35" y1="50" x2="168" y2="70" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <text x="102" y="55" font-family="'Segoe UI', sans-serif" font-size="8" fill="#166534" text-anchor="middle">Frame 0</text>
            <line x1="170" y1="75" x2="37" y2="95" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <text x="102" y="82" font-family="'Segoe UI', sans-serif" font-size="8" fill="#1e40af" text-anchor="middle">ACK 1</text>
            <!-- Frame 1 -->
            <line x1="35" y1="105" x2="168" y2="125" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <text x="102" y="112" font-family="'Segoe UI', sans-serif" font-size="8" fill="#166534" text-anchor="middle">Frame 1</text>
            <text x="102" y="160" font-family="'Segoe UI', sans-serif" font-size="8" fill="#64748b" text-anchor="middle">Window: Sw = 1, Rw = 1</text>
            <text x="102" y="175" font-family="'Segoe UI', sans-serif" font-size="8" font-weight="bold" fill="#dc2626" text-anchor="middle">Idle during propagation</text>
        </g>

        <!-- 2. Go-Back-N ARQ -->
        <g transform="translate(225, 10)">
            <rect x="0" y="0" width="220" height="195" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="110" y="20" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Go-Back-N ARQ (GBN)</text>
            <line x1="35" y1="35" x2="35" y2="175" stroke="#94a3b8" stroke-width="2"/>
            <line x1="185" y1="35" x2="185" y2="175" stroke="#94a3b8" stroke-width="2"/>
            <text x="35" y="32" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#475569" text-anchor="middle">Tx</text>
            <text x="185" y="32" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#475569" text-anchor="middle">Rx</text>
            <!-- Continuous send -->
            <line x1="35" y1="45" x2="183" y2="65" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <line x1="35" y1="60" x2="110" y2="73" stroke="#dc2626" stroke-width="1.5"/>
            <text x="125" y="75" font-family="'Segoe UI', sans-serif" font-size="8" fill="#dc2626">Frame 1 (LOST)</text>
            <line x1="35" y1="75" x2="183" y2="95" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <line x1="35" y1="90" x2="183" y2="110" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <!-- Receiver discards 2 and 3 -->
            <text x="110" y="132" font-family="'Segoe UI', sans-serif" font-size="8" fill="#dc2626" text-anchor="middle">Rx discards Frames 2 & 3</text>
            <line x1="35" y1="140" x2="183" y2="160" stroke="#ea580c" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <text x="110" y="152" font-family="'Segoe UI', sans-serif" font-size="7.5" fill="#c2410c" text-anchor="middle">Timeout! Retransmits 1, 2, 3</text>
            <text x="110" y="175" font-family="'Segoe UI', sans-serif" font-size="8" font-weight="bold" fill="#1e40af" text-anchor="middle">Sw = 2^m - 1, Rw = 1</text>
        </g>

        <!-- 3. Selective Repeat ARQ -->
        <g transform="translate(455, 10)">
            <rect x="0" y="0" width="215" height="195" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
            <text x="107" y="20" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Selective Repeat ARQ</text>
            <line x1="35" y1="35" x2="35" y2="175" stroke="#94a3b8" stroke-width="2"/>
            <line x1="180" y1="35" x2="180" y2="175" stroke="#94a3b8" stroke-width="2"/>
            <text x="35" y="32" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#475569" text-anchor="middle">Tx</text>
            <text x="180" y="32" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#475569" text-anchor="middle">Rx</text>
            <!-- Frame 1 lost -->
            <line x1="35" y1="45" x2="178" y2="65" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <line x1="35" y1="60" x2="105" y2="73" stroke="#dc2626" stroke-width="1.5"/>
            <line x1="35" y1="75" x2="178" y2="95" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <text x="107" y="112" font-family="'Segoe UI', sans-serif" font-size="8" fill="#15803d" text-anchor="middle">Rx buffers Frame 2; sends NAK 1</text>
            <!-- Retransmit ONLY Frame 1 -->
            <line x1="35" y1="125" x2="178" y2="145" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arr-g)"/>
            <text x="107" y="137" font-family="'Segoe UI', sans-serif" font-size="8" fill="#1d4ed8" text-anchor="middle">Retransmit ONLY Frame 1</text>
            <text x="107" y="160" font-family="'Segoe UI', sans-serif" font-size="8" fill="#64748b" text-anchor="middle">Highest efficiency; complex buffer</text>
            <text x="107" y="175" font-family="'Segoe UI', sans-serif" font-size="8" font-weight="bold" fill="#1e40af" text-anchor="middle">Sw = 2^(m-1), Rw = 2^(m-1)</text>
        </g>
    </svg>
    """
    return get_svg_wrapper(svg, "2.3", "Comparison of Sliding Window ARQ Protocols: Stop-and-Wait, Go-Back-N, and Selective Repeat")

def fig_mac_protocols():
    svg = """
    <svg width="670" height="200" viewBox="0 0 670 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Pure ALOHA vs Slotted ALOHA -->
        <g transform="translate(10, 10)">
            <rect x="0" y="0" width="310" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="155" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Pure ALOHA vs Slotted ALOHA</text>
            
            <rect x="20" y="45" width="270" height="50" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="30" y="62" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#b45309">Pure ALOHA:</text>
            <text x="30" y="76" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#334155">• Continuous time: Transmit whenever data is ready.</text>
            <text x="30" y="88" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#334155">• Vulnerable time = 2 x Tfr | Max Throughput S = 18.4%</text>

            <rect x="20" y="105" width="270" height="55" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="30" y="122" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#166534">Slotted ALOHA:</text>
            <text x="30" y="136" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#334155">• Discrete time slots of duration Tfr. Sync clock needed.</text>
            <text x="30" y="148" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#334155">• Vulnerable time = 1 x Tfr | Max Throughput S = 36.8% (Doubled!)</text>
        </g>

        <!-- CSMA/CD vs CSMA/CA -->
        <g transform="translate(340, 10)">
            <rect x="0" y="0" width="320" height="175" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="160" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0f2b5c" text-anchor="middle">CSMA/CD vs CSMA/CA</text>
            
            <rect x="15" y="45" width="290" height="50" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="25" y="62" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#1e40af">CSMA/CD (Wired Ethernet 802.3):</text>
            <text x="25" y="76" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#334155">• "Listen While Talk". Stop immediately upon collision.</text>
            <text x="25" y="88" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#334155">• Min Frame Size: Tfr &ge; 2 x Tp | Jamming signal sent.</text>

            <rect x="15" y="105" width="290" height="55" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
            <text x="25" y="122" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#7c3aed">CSMA/CA (Wireless Wi-Fi 802.11):</text>
            <text x="25" y="136" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#334155">• Cannot detect collision while transmitting (signal fade).</text>
            <text x="25" y="148" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#334155">• Uses IFS, Contention Window, RTS/CTS & ACK frames.</text>
        </g>
    </svg>
    """
    return get_svg_wrapper(svg, "2.4", "Random Access Protocols Comparison: ALOHA and CSMA Variants")

def fig_ipv4_header():
    svg = """
    <svg width="670" height="220" viewBox="0 0 670 220" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="650" height="200" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="335" y="26" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0f2b5c" text-anchor="middle">IPv4 Datagram Header Format (32 Bits Wide / 20 to 60 Bytes)</text>

        <!-- Bit numbers -->
        <text x="30" y="42" font-family="'Consolas', monospace" font-size="8.5" fill="#64748b">0</text>
        <text x="110" y="42" font-family="'Consolas', monospace" font-size="8.5" fill="#64748b">4</text>
        <text x="190" y="42" font-family="'Consolas', monospace" font-size="8.5" fill="#64748b">8</text>
        <text x="335" y="42" font-family="'Consolas', monospace" font-size="8.5" fill="#64748b">16</text>
        <text x="640" y="42" font-family="'Consolas', monospace" font-size="8.5" fill="#64748b" text-anchor="end">31</text>

        <!-- Row 1: VER, HLEN, Service, Total Length -->
        <rect x="25" y="48" width="80" height="28" fill="#dbeafe" stroke="#2563eb"/>
        <text x="65" y="66" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">VER (4b)</text>

        <rect x="105" y="48" width="80" height="28" fill="#dbeafe" stroke="#2563eb"/>
        <text x="145" y="66" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">HLEN (4b)</text>

        <rect x="185" y="48" width="160" height="28" fill="#e0e7ff" stroke="#4338ca"/>
        <text x="265" y="66" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#312e81" text-anchor="middle">Service Type / DiffServ (8b)</text>

        <rect x="345" y="48" width="300" height="28" fill="#dcfce7" stroke="#16a34a"/>
        <text x="495" y="66" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#166534" text-anchor="middle">Total Length in Bytes (16 bits)</text>

        <!-- Row 2: Identification, Flags, Fragment Offset -->
        <rect x="25" y="76" width="320" height="28" fill="#fef3c7" stroke="#d97706"/>
        <text x="185" y="94" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#92400e" text-anchor="middle">Identification (16 bits)</text>

        <rect x="345" y="76" width="60" height="28" fill="#fed7aa" stroke="#ea580c"/>
        <text x="375" y="94" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#9a3412" text-anchor="middle">Flags (3b)</text>

        <rect x="405" y="76" width="240" height="28" fill="#fed7aa" stroke="#ea580c"/>
        <text x="525" y="94" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#9a3412" text-anchor="middle">Fragmentation Offset (13 bits)</text>

        <!-- Row 3: TTL, Protocol, Header Checksum -->
        <rect x="25" y="104" width="160" height="28" fill="#fee2e2" stroke="#dc2626"/>
        <text x="105" y="122" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">Time to Live - TTL (8b)</text>

        <rect x="185" y="104" width="160" height="28" fill="#f3e8ff" stroke="#9333ea"/>
        <text x="265" y="122" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#6b21a8" text-anchor="middle">Protocol (8b: TCP=6, UDP=17)</text>

        <rect x="345" y="104" width="300" height="28" fill="#ccfbf1" stroke="#0d9488"/>
        <text x="495" y="122" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#115e59" text-anchor="middle">Header Checksum (16 bits)</text>

        <!-- Row 4: Source IP Address -->
        <rect x="25" y="132" width="620" height="26" fill="#e0f2fe" stroke="#0284c7"/>
        <text x="335" y="149" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#0369a1" text-anchor="middle">Source IP Address (32 bits)</text>

        <!-- Row 5: Destination IP Address -->
        <rect x="25" y="158" width="620" height="26" fill="#e0f2fe" stroke="#0284c7"/>
        <text x="335" y="175" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#0369a1" text-anchor="middle">Destination IP Address (32 bits)</text>

        <!-- Row 6: Options + Padding -->
        <rect x="25" y="184" width="620" height="20" fill="#f1f5f9" stroke="#94a3b8" stroke-dasharray="3,3"/>
        <text x="335" y="198" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">Options & Padding (0 to 40 bytes, optional)</text>
    </svg>
    """
    return get_svg_wrapper(svg, "3.1", "IPv4 Datagram Header Field Layout (Standard 20-byte base)")

def fig_ipv6_header():
    svg = """
    <svg width="670" height="175" viewBox="0 0 670 175" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="8" width="650" height="158" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="335" y="24" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0f2b5c" text-anchor="middle">IPv6 Fixed Base Header (40 Bytes Fixed Length / 32 Bits Wide)</text>

        <!-- Row 1: VER, Traffic Class, Flow Label -->
        <rect x="25" y="32" width="80" height="26" fill="#dbeafe" stroke="#2563eb"/>
        <text x="65" y="49" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">VER (4b)</text>

        <rect x="105" y="32" width="160" height="26" fill="#e0e7ff" stroke="#4338ca"/>
        <text x="185" y="49" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#312e81" text-anchor="middle">Traffic Class (8b)</text>

        <rect x="265" y="32" width="380" height="26" fill="#fef3c7" stroke="#d97706"/>
        <text x="455" y="49" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#92400e" text-anchor="middle">Flow Label (20 bits)</text>

        <!-- Row 2: Payload Length, Next Header, Hop Limit -->
        <rect x="25" y="58" width="320" height="26" fill="#dcfce7" stroke="#16a34a"/>
        <text x="185" y="75" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#166534" text-anchor="middle">Payload Length (16 bits)</text>

        <rect x="345" y="58" width="160" height="26" fill="#f3e8ff" stroke="#9333ea"/>
        <text x="425" y="75" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#6b21a8" text-anchor="middle">Next Header (8 bits)</text>

        <rect x="505" y="58" width="140" height="26" fill="#fee2e2" stroke="#dc2626"/>
        <text x="575" y="75" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">Hop Limit (8 bits)</text>

        <!-- Row 3: Source Address (128 bits) -->
        <rect x="25" y="84" width="620" height="34" fill="#e0f2fe" stroke="#0284c7"/>
        <text x="335" y="105" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">Source IP Address (128 bits / 16 bytes)</text>

        <!-- Row 4: Destination Address (128 bits) -->
        <rect x="25" y="118" width="620" height="34" fill="#e0f2fe" stroke="#0284c7"/>
        <text x="335" y="139" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">Destination IP Address (128 bits / 16 bytes)</text>
    </svg>
    """
    return get_svg_wrapper(svg, "3.2", "IPv6 Base Header Layout (Streamlined 8 fields)")

def fig_dijkstra_graph():
    svg = """
    <svg width="650" height="180" viewBox="0 0 650 180" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="5" width="630" height="168" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <!-- Links with weights -->
        <line x1="120" y1="90" x2="240" y2="40" stroke="#64748b" stroke-width="2"/>
        <text x="175" y="55" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#b91c1c">2</text>

        <line x1="120" y1="90" x2="240" y2="140" stroke="#64748b" stroke-width="2"/>
        <text x="175" y="130" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#b91c1c">5</text>

        <line x1="240" y1="40" x2="380" y2="40" stroke="#64748b" stroke-width="2"/>
        <text x="310" y="32" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#b91c1c">3</text>

        <line x1="240" y1="40" x2="240" y2="140" stroke="#64748b" stroke-width="2"/>
        <text x="248" y="95" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#b91c1c">1</text>

        <line x1="240" y1="140" x2="380" y2="140" stroke="#64748b" stroke-width="2"/>
        <text x="310" y="155" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#b91c1c">2</text>

        <line x1="380" y1="40" x2="500" y2="90" stroke="#64748b" stroke-width="2"/>
        <text x="445" y="55" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#b91c1c">1</text>

        <line x1="380" y1="140" x2="500" y2="90" stroke="#64748b" stroke-width="2"/>
        <text x="445" y="130" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#b91c1c">4</text>

        <!-- Nodes -->
        <circle cx="120" cy="90" r="18" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
        <text x="120" y="96" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">A</text>

        <circle cx="240" cy="40" r="18" fill="#10b981" stroke="#047857" stroke-width="2"/>
        <text x="240" y="46" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">B</text>

        <circle cx="240" cy="140" r="18" fill="#10b981" stroke="#047857" stroke-width="2"/>
        <text x="240" y="146" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">C</text>

        <circle cx="380" cy="40" r="18" fill="#10b981" stroke="#047857" stroke-width="2"/>
        <text x="380" y="46" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">D</text>

        <circle cx="380" cy="140" r="18" fill="#10b981" stroke="#047857" stroke-width="2"/>
        <text x="380" y="146" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">E</text>

        <circle cx="500" cy="90" r="18" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
        <text x="500" y="96" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">Z</text>

        <text x="570" y="85" font-family="'Segoe UI', sans-serif" font-size="9" fill="#1e3a8a" font-weight="bold">Source: Node A</text>
        <text x="570" y="105" font-family="'Segoe UI', sans-serif" font-size="9" fill="#15803d">Target: Node Z</text>
    </svg>
    """
    return get_svg_wrapper(svg, "3.3", "Network Graph Model for Dijkstra's Shortest Path First (SPF) Algorithm")

def fig_tcp_header():
    svg = """
    <svg width="670" height="210" viewBox="0 0 670 210" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="8" width="650" height="195" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="335" y="24" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0f2b5c" text-anchor="middle">TCP Segment Header Format (32 Bits Wide / 20 to 60 Bytes)</text>

        <!-- Row 1: Source & Destination Port -->
        <rect x="25" y="32" width="310" height="28" fill="#dbeafe" stroke="#2563eb"/>
        <text x="180" y="50" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#1e40af" text-anchor="middle">Source Port (16 bits)</text>

        <rect x="335" y="32" width="310" height="28" fill="#dbeafe" stroke="#2563eb"/>
        <text x="490" y="50" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#1e40af" text-anchor="middle">Destination Port (16 bits)</text>

        <!-- Row 2: Sequence Number -->
        <rect x="25" y="60" width="620" height="28" fill="#e0e7ff" stroke="#4338ca"/>
        <text x="335" y="78" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#312e81" text-anchor="middle">Sequence Number (32 bits) - Byte stream offset</text>

        <!-- Row 3: Acknowledgement Number -->
        <rect x="25" y="88" width="620" height="28" fill="#dcfce7" stroke="#16a34a"/>
        <text x="335" y="106" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#166534" text-anchor="middle">Acknowledgement Number (32 bits) - Next expected byte</text>

        <!-- Row 4: HLEN, Reserved, Flags, Window Size -->
        <rect x="25" y="116" width="75" height="28" fill="#fef3c7" stroke="#d97706"/>
        <text x="62" y="134" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#92400e" text-anchor="middle">HLEN (4b)</text>

        <rect x="100" y="116" width="75" height="28" fill="#f1f5f9" stroke="#94a3b8"/>
        <text x="137" y="134" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">Res (6b)</text>

        <rect x="175" y="116" width="160" height="28" fill="#fed7aa" stroke="#ea580c"/>
        <text x="255" y="134" font-family="'Consolas', monospace" font-size="8.5" font-weight="bold" fill="#9a3412" text-anchor="middle">U A P R S F</text>

        <rect x="335" y="116" width="310" height="28" fill="#ccfbf1" stroke="#0d9488"/>
        <text x="490" y="134" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#115e59" text-anchor="middle">Window Size (16 bits) - Flow Control rwnd</text>

        <!-- Row 5: Checksum & Urgent Pointer -->
        <rect x="25" y="144" width="310" height="28" fill="#fee2e2" stroke="#dc2626"/>
        <text x="180" y="162" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#991b1b" text-anchor="middle">Checksum (16 bits)</text>

        <rect x="335" y="144" width="310" height="28" fill="#f3e8ff" stroke="#9333ea"/>
        <text x="490" y="162" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="bold" fill="#6b21a8" text-anchor="middle">Urgent Pointer (16 bits)</text>

        <!-- Row 6: Options -->
        <rect x="25" y="172" width="620" height="20" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="3,3"/>
        <text x="335" y="186" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">Options & Padding (MSS, Window Scale, SACK, Timestamp)</text>
    </svg>
    """
    return get_svg_wrapper(svg, "4.1", "TCP Segment Header Layout (Detailed 32-bit field structure)")

def fig_tcp_handshake():
    svg = """
    <svg width="660" height="230" viewBox="0 0 660 230" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arr-b" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#1d4ed8" />
            </marker>
        </defs>
        <!-- 3-Way Handshake (Left) -->
        <g transform="translate(10, 10)">
            <rect x="0" y="0" width="310" height="205" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="155" y="20" font-family="'Segoe UI', sans-serif" font-size="11.5" font-weight="bold" fill="#0f2b5c" text-anchor="middle">3-Way Handshake (Establishment)</text>
            <line x1="50" y1="35" x2="50" y2="185" stroke="#94a3b8" stroke-width="2"/>
            <line x1="260" y1="35" x2="260" y2="185" stroke="#94a3b8" stroke-width="2"/>
            <text x="50" y="32" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Client</text>
            <text x="260" y="32" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Server</text>
            
            <!-- 1. SYN -->
            <line x1="50" y1="55" x2="258" y2="80" stroke="#1d4ed8" stroke-width="2" marker-end="url(#arr-b)"/>
            <text x="155" y="63" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">1. SYN=1, seq=x</text>

            <!-- 2. SYN + ACK -->
            <line x1="260" y1="95" x2="52" y2="120" stroke="#1d4ed8" stroke-width="2" marker-end="url(#arr-b)"/>
            <text x="155" y="103" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">2. SYN=1, ACK=1, seq=y, ack=x+1</text>

            <!-- 3. ACK -->
            <line x1="50" y1="135" x2="258" y2="160" stroke="#1d4ed8" stroke-width="2" marker-end="url(#arr-b)"/>
            <text x="155" y="143" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">3. ACK=1, seq=x+1, ack=y+1</text>

            <text x="155" y="185" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#15803d" text-anchor="middle">CONNECTION ESTABLISHED</text>
        </g>

        <!-- 4-Way Teardown (Right) -->
        <g transform="translate(340, 10)">
            <rect x="0" y="0" width="310" height="205" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="155" y="20" font-family="'Segoe UI', sans-serif" font-size="11.5" font-weight="bold" fill="#0f2b5c" text-anchor="middle">4-Way Handshake (Teardown)</text>
            <line x1="50" y1="35" x2="50" y2="185" stroke="#94a3b8" stroke-width="2"/>
            <line x1="260" y1="35" x2="260" y2="185" stroke="#94a3b8" stroke-width="2"/>
            <text x="50" y="32" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Client</text>
            <text x="260" y="32" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Server</text>

            <!-- 1. FIN -->
            <line x1="50" y1="50" x2="258" y2="70" stroke="#dc2626" stroke-width="1.5" marker-end="url(#arr-b)"/>
            <text x="155" y="56" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#991b1b" text-anchor="middle">1. FIN=1, seq=u</text>

            <!-- 2. ACK -->
            <line x1="260" y1="78" x2="52" y2="98" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-b)"/>
            <text x="155" y="84" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#166534" text-anchor="middle">2. ACK=1, ack=u+1 (Half-Closed)</text>

            <!-- 3. Server FIN -->
            <line x1="260" y1="110" x2="52" y2="130" stroke="#dc2626" stroke-width="1.5" marker-end="url(#arr-b)"/>
            <text x="155" y="116" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#991b1b" text-anchor="middle">3. FIN=1, seq=w, ack=u+1</text>

            <!-- 4. Client ACK -->
            <line x1="50" y1="138" x2="258" y2="158" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-b)"/>
            <text x="155" y="144" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#166534" text-anchor="middle">4. ACK=1, ack=w+1</text>

            <text x="155" y="185" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#dc2626" text-anchor="middle">TIME_WAIT (2 MSL) -> CLOSED</text>
        </g>
    </svg>
    """
    return get_svg_wrapper(svg, "4.2", "TCP Connection Life Cycle: 3-Way Handshake and 4-Way Connection Teardown")

def fig_tcp_congestion():
    svg = """
    <svg width="660" height="210" viewBox="0 0 660 210" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="5" width="640" height="195" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="330" y="22" font-family="'Segoe UI', sans-serif" font-size="11.5" font-weight="bold" fill="#0f2b5c" text-anchor="middle">TCP Congestion Control Dynamics (Tahoe vs Reno)</text>

        <!-- Axes -->
        <line x1="50" y1="165" x2="620" y2="165" stroke="#334155" stroke-width="1.5"/>
        <line x1="50" y1="165" x2="50" y2="35" stroke="#334155" stroke-width="1.5"/>
        <text x="615" y="180" font-family="'Segoe UI', sans-serif" font-size="9" fill="#475569" text-anchor="end">Transmission Rounds (RTT)</text>
        <text x="45" y="32" font-family="'Segoe UI', sans-serif" font-size="9" fill="#475569">cwnd (MSS)</text>

        <!-- ssthresh horizontal threshold line -->
        <line x1="50" y1="95" x2="620" y2="95" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4"/>
        <text x="58" y="90" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#64748b">ssthresh = 16</text>

        <!-- Slow Start curve (exponential) -->
        <path d="M 50 165 Q 110 160, 160 95" fill="none" stroke="#2563eb" stroke-width="2.5"/>
        <text x="100" y="145" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#1d4ed8">Slow Start (2^n)</text>

        <!-- Congestion Avoidance line (linear) -->
        <line x1="160" y1="95" x2="280" y2="55" stroke="#16a34a" stroke-width="2.5"/>
        <text x="210" y="65" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#15803d">Additive Increase (+1)</text>

        <!-- Drop at round 10 -->
        <circle cx="280" cy="55" r="4" fill="#dc2626"/>
        <text x="280" y="45" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#dc2626" text-anchor="middle">3 Dup ACKs</text>

        <!-- TCP Tahoe: Drop to 1 -->
        <line x1="280" y1="55" x2="285" y2="165" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="2,2"/>
        <path d="M 285 165 Q 325 160, 360 120" fill="none" stroke="#dc2626" stroke-width="2"/>
        <text x="320" y="150" font-family="'Segoe UI', sans-serif" font-size="8" fill="#991b1b">Tahoe: cwnd=1</text>

        <!-- TCP Reno: Fast Recovery drop to ssthresh/2 and linear -->
        <line x1="280" y1="55" x2="290" y2="115" stroke="#ea580c" stroke-width="2"/>
        <line x1="290" y1="115" x2="450" y2="75" stroke="#ea580c" stroke-width="2.5"/>
        <text x="380" y="100" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#ea580c">Reno: Fast Recovery (cwnd = ssthresh)</text>
    </svg>
    """
    return get_svg_wrapper(svg, "4.3", "TCP Congestion Control: Slow Start, Additive Increase, Tahoe vs Reno Recovery")

def fig_dns_resolution():
    svg = """
    <svg width="670" height="230" viewBox="0 0 670 230" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arr-m" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#0f2b5c" />
            </marker>
        </defs>
        <rect x="10" y="8" width="650" height="212" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="335" y="24" font-family="'Segoe UI', sans-serif" font-size="11.5" font-weight="bold" fill="#0f2b5c" text-anchor="middle">DNS Resolution: Recursive vs Iterative Query Flow</text>

        <!-- Client -->
        <rect x="25" y="80" width="85" height="45" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
        <text x="67" y="100" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Client PC</text>
        <text x="67" y="114" font-family="'Segoe UI', sans-serif" font-size="8" fill="#1e3a8a" text-anchor="middle">(Resolver)</text>

        <!-- Local DNS Server -->
        <rect x="170" y="80" width="105" height="45" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
        <text x="222" y="100" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#166534" text-anchor="middle">Local DNS</text>
        <text x="222" y="114" font-family="'Segoe UI', sans-serif" font-size="8" fill="#14532d" text-anchor="middle">(ISP / Campus)</text>

        <!-- Root Server -->
        <rect x="360" y="38" width="125" height="36" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
        <text x="422" y="56" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#991b1b" text-anchor="middle">1. Root DNS Server</text>
        <text x="422" y="68" font-family="'Segoe UI', sans-serif" font-size="8" fill="#7f1d1d" text-anchor="middle">(.)</text>

        <!-- TLD Server -->
        <rect x="360" y="90" width="125" height="36" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="422" y="108" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#92400e" text-anchor="middle">2. TLD Server</text>
        <text x="422" y="120" font-family="'Segoe UI', sans-serif" font-size="8" fill="#78350f" text-anchor="middle">(.com, .edu, .in)</text>

        <!-- Authoritative Server -->
        <rect x="360" y="142" width="135" height="36" rx="4" fill="#e0e7ff" stroke="#4338ca" stroke-width="1.5"/>
        <text x="427" y="160" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#312e81" text-anchor="middle">3. Authoritative DNS</text>
        <text x="427" y="172" font-family="'Segoe UI', sans-serif" font-size="8" fill="#1e1b4b" text-anchor="middle">(example.com)</text>

        <!-- Recursive Client-Local query -->
        <line x1="110" y1="95" x2="168" y2="95" stroke="#0f2b5c" stroke-width="1.5" marker-end="url(#arr-m)"/>
        <text x="140" y="90" font-family="'Segoe UI', sans-serif" font-size="8" fill="#0f2b5c" text-anchor="middle">Query</text>
        <line x1="168" y1="112" x2="112" y2="112" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-m)"/>
        <text x="140" y="125" font-family="'Segoe UI', sans-serif" font-size="8" fill="#166534" text-anchor="middle">IP Answer</text>

        <!-- Iterative steps -->
        <path d="M 275 88 L 358 55" stroke="#dc2626" stroke-width="1.2" marker-end="url(#arr-m)"/>
        <path d="M 358 62 L 275 95" stroke="#dc2626" stroke-width="1.2" stroke-dasharray="2,2" marker-end="url(#arr-m)"/>

        <path d="M 275 100 L 358 102" stroke="#d97706" stroke-width="1.2" marker-end="url(#arr-m)"/>
        <path d="M 358 112 L 275 110" stroke="#d97706" stroke-width="1.2" stroke-dasharray="2,2" marker-end="url(#arr-m)"/>

        <path d="M 275 115 L 358 152" stroke="#4338ca" stroke-width="1.2" marker-end="url(#arr-m)"/>
        <path d="M 358 162 L 275 125" stroke="#4338ca" stroke-width="1.2" stroke-dasharray="2,2" marker-end="url(#arr-m)"/>

        <!-- Legend / Notes -->
        <text x="560" y="85" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#0f2b5c">Iterative Lookup:</text>
        <text x="560" y="100" font-family="'Segoe UI', sans-serif" font-size="8" fill="#334155">1. Ask Root -> TLD referral</text>
        <text x="560" y="115" font-family="'Segoe UI', sans-serif" font-size="8" fill="#334155">2. Ask TLD -> Auth referral</text>
        <text x="560" y="130" font-family="'Segoe UI', sans-serif" font-size="8" fill="#334155">3. Ask Auth -> Final IP</text>
        <text x="560" y="145" font-family="'Segoe UI', sans-serif" font-size="8" fill="#16a34a">Local DNS caches result</text>
    </svg>
    """
    return get_svg_wrapper(svg, "5.1", "Domain Name System (DNS) Hierarchical Resolution Flow")

def fig_email_architecture():
    svg = """
    <svg width="670" height="175" viewBox="0 0 670 175" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arr-e" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#0f2b5c" />
            </marker>
        </defs>
        <rect x="10" y="8" width="650" height="158" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="335" y="24" font-family="'Segoe UI', sans-serif" font-size="11.5" font-weight="bold" fill="#0f2b5c" text-anchor="middle">Internet Electronic Mail Architecture & Protocols</text>

        <!-- Sender UA -->
        <rect x="25" y="60" width="85" height="45" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
        <text x="67" y="80" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Sender UA</text>
        <text x="67" y="94" font-family="'Segoe UI', sans-serif" font-size="8" fill="#1e3a8a" text-anchor="middle">(Outlook, Gmail)</text>

        <!-- Sender Mail Server (MTA) -->
        <rect x="170" y="60" width="105" height="55" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="222" y="80" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#92400e" text-anchor="middle">Sender Mail Server</text>
        <text x="222" y="93" font-family="'Segoe UI', sans-serif" font-size="8" fill="#78350f" text-anchor="middle">(MTA Client / Spool)</text>

        <!-- Recipient Mail Server (MTA) -->
        <rect x="390" y="60" width="115" height="55" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
        <text x="447" y="80" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#92400e" text-anchor="middle">Receiver Mail Server</text>
        <text x="447" y="93" font-family="'Segoe UI', sans-serif" font-size="8" fill="#78350f" text-anchor="middle">(MTA Server / Mailbox)</text>

        <!-- Receiver UA -->
        <rect x="555" y="60" width="85" height="45" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
        <text x="597" y="80" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">Receiver UA</text>
        <text x="597" y="94" font-family="'Segoe UI', sans-serif" font-size="8" fill="#1e3a8a" text-anchor="middle">(User Agent)</text>

        <!-- Flow 1: SMTP -->
        <line x1="110" y1="82" x2="168" y2="82" stroke="#0f2b5c" stroke-width="1.8" marker-end="url(#arr-e)"/>
        <text x="140" y="75" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="bold" fill="#2563eb" text-anchor="middle">SMTP (Push)</text>

        <!-- Flow 2: SMTP over Internet -->
        <line x1="275" y1="82" x2="388" y2="82" stroke="#0f2b5c" stroke-width="2" marker-end="url(#arr-e)"/>
        <text x="332" y="75" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="bold" fill="#16a34a" text-anchor="middle">SMTP (Port 25)</text>
        <text x="332" y="100" font-family="'Segoe UI', sans-serif" font-size="7.5" fill="#64748b" text-anchor="middle">Internet MTA-to-MTA</text>

        <!-- Flow 3: POP3 / IMAP -->
        <line x1="505" y1="82" x2="553" y2="82" stroke="#0f2b5c" stroke-width="1.8" marker-end="url(#arr-e)"/>
        <text x="530" y="75" font-family="'Segoe UI', sans-serif" font-size="8" font-weight="bold" fill="#dc2626" text-anchor="middle">POP3 / IMAP</text>
        <text x="530" y="100" font-family="'Segoe UI', sans-serif" font-size="7.5" fill="#991b1b" text-anchor="middle">(Pull Access)</text>

        <text x="335" y="145" font-family="'Segoe UI', sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">Key Rule: SMTP is a PUSH protocol (client to server). POP3/IMAP are PULL protocols (user retrieves from server).</text>
    </svg>
    """
    return get_svg_wrapper(svg, "5.2", "End-to-End Electronic Mail Architecture: Push vs Pull Stages")
