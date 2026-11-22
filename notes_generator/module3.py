"""
Module 3: Network Layer - Services, Packet Switching, IPv4, IPv6, Subnetting, NAT, Routing Algorithms (DVR, LSR, PVR), Routing Protocols (RIP, OSPF, BGP), and Multicast (MOSPF).
"""
from diagrams import fig_ipv4_header, fig_ipv6_header, fig_dijkstra_graph

def get_module_3_content():
    content = r"""
    <h1 class="module-title">MODULE 3 &mdash; Network Layer: IPv4, IPv6, Subnetting, NAT, Unicast & Multicast Routing</h1>

    <div class="eli5-box">
        <div class="title">💡 ELI5: What is the Network Layer? (The GPS and Postal Van System)</div>
        If the Data Link Layer is your postman delivering an envelope to the very next house on your street, the <b>Network Layer</b> is the global logistics network!
        It puts an IP address on your envelope (e.g., "123 Country Road, Paris, France"). Even if the postman has never been to France, routers act like airport cargo hubs:
        1. Router in India looks at the destination "France" and forwards the packet to a European gateway router.
        2. Routing algorithms (like Google Maps / GPS) calculate the shortest, fastest path across multiple countries.
        3. If a road or underwater cable breaks, routers find an alternate highway automatically!
    </div>

    <h2 class="section-title">1. Network Layer Services & Packet Switching (Ch. 18.1 & 18.2)</h2>
    <p>
        The Network Layer is responsible for <b>host-to-host communication</b> across heterogeneous networks.
    </p>
    <ul>
        <li><b>Packetizing:</b> Encapsulates data from the transport layer into network datagrams at the source and decapsulates them at the destination without examining payload contents.</li>
        <li><b>Routing:</b> The process of discovering optimal paths from source to destination across multiple interconnected routers using distributed routing algorithms.</li>
        <li><b>Forwarding:</b> The action taken by a router when a packet arrives on an input link &mdash; looking up the destination IP in the local forwarding table and transferring the packet to the appropriate output interface buffer.</li>
        <li><b>Error & Flow Control:</b> Provided minimally at Layer 3 (mostly delegated to transport layer TCP); uses <b>ICMP</b> (Internet Control Message Protocol) to report delivery problems.</li>
    </ul>

    <h2 class="section-title">2. IPv4 Addressing: Classful, CIDR, Subnetting & NAT (Ch. 18.4)</h2>
    <p>
        An <b>IPv4 address</b> is a 32-bit binary number that uniquely and universally identifies the connection of a host or router interface to the Internet. Address space = $2^{32} = 4,294,967,296$ addresses ($\approx 4.3$ billion).
    </p>

    <h3 class="sub-section-title">2.1 Classful Addressing</h3>
    <p>Originally, the address space was divided into five classes (A, B, C, D, E):</p>
    <table>
        <tr>
            <th>Class</th>
            <th>First Octet Range (Binary / Dec)</th>
            <th>Default Subnet Mask</th>
            <th>NetID / HostID Bits</th>
            <th>Number of Networks & Hosts per Net</th>
            <th>Intended Use</th>
        </tr>
        <tr>
            <td><b>Class A</b></td>
            <td><code>0xxxxxxx</code> (0 &ndash; 127)</td>
            <td><code>255.0.0.0</code> (/8)</td>
            <td>8 bits NetID, 24 bits HostID</td>
            <td>$2^7 = 128$ nets;<br/>$2^{24}-2 \approx 16.7$ million hosts/net</td>
            <td>Massive global organizations</td>
        </tr>
        <tr>
            <td><b>Class B</b></td>
            <td><code>10xxxxxx</code> (128 &ndash; 191)</td>
            <td><code>255.255.0.0</code> (/16)</td>
            <td>16 bits NetID, 16 bits HostID</td>
            <td>$2^{14} = 16,384$ nets;<br/>$2^{16}-2 = 65,534$ hosts/net</td>
            <td>Medium-to-large universities & corporations</td>
        </tr>
        <tr>
            <td><b>Class C</b></td>
            <td><code>110xxxxx</code> (192 &ndash; 223)</td>
            <td><code>255.255.255.0</code> (/24)</td>
            <td>24 bits NetID, 8 bits HostID</td>
            <td>$2^{21} \approx 2$ million nets;<br/>$2^8-2 = 254$ hosts/net</td>
            <td>Small businesses and local networks</td>
        </tr>
        <tr>
            <td><b>Class D</b></td>
            <td><code>1110xxxx</code> (224 &ndash; 239)</td>
            <td>None (No NetID/HostID)</td>
            <td>&mdash;</td>
            <td>Single flat multicast address space</td>
            <td><b>Multicasting</b></td>
        </tr>
        <tr>
            <td><b>Class E</b></td>
            <td><code>1111xxxx</code> (240 &ndash; 255)</td>
            <td>None</td>
            <td>&mdash;</td>
            <td>&mdash;</td>
            <td>Reserved for experimental / future use</td>
        </tr>
    </table>

    <h3 class="sub-section-title">2.2 Classless Addressing (CIDR &mdash; Classless Inter-Domain Routing)</h3>
    <p>
        Classful addressing wasted billions of addresses (e.g., an organization needing 1,000 addresses had to take a Class B with 65,534 addresses, wasting 98%!). In 1993, <b>CIDR</b> abolished rigid classes:
    </p>
    <ul>
        <li><b>Slash Notation (/n):</b> Addresses are written as <code>a.b.c.d/n</code>, where $n$ is the <b>prefix length</b> (number of bits assigned to the network prefix).</li>
        <li><b>Host Bits:</b> $32 - n$. Total addresses in block = $2^{32 - n}$. Usable host addresses = $2^{32 - n} - 2$.</li>
        <li><b>Network Address (First Address):</b> Bitwise AND between IP address and the Subnet Mask. Represents the entire network block.</li>
        <li><b>Direct Broadcast Address (Last Address):</b> Host bits are all set to <code>1</code>. Used to broadcast to all hosts in that subnet.</li>
    </ul>

    <div class="exam-tip">
        <div class="title">⭐ Worked Numerical: Subnet Design and Calculation</div>
        <b>Problem:</b> An organization is assigned the block <code>192.168.10.0/24</code>. The network administrator needs to create <b>4 equal subnets</b>. Find the new subnet mask, subnet prefix, and address range for each subnet.<br/>
        <b>Solution:</b><br/>
        1. Original prefix $n = 24$. To create 4 subnets, we need $2^k \ge 4 \implies k = 2$ additional subnet bits.<br/>
        2. New subnet prefix: $n' = 24 + 2 = \mathbf{/26}$.<br/>
        3. Subnet mask in binary: <code>11111111.11111111.11111111.11000000</code> $\implies \mathbf{255.255.255.192}$.<br/>
        4. Total addresses per subnet = $2^{32 - 26} = 2^6 = 64$ addresses ($64 - 2 = 62$ usable hosts).<br/>
        <b>Subnet Breakdown:</b>
        <ul>
            <li><b>Subnet 0:</b> Network ID: <code>192.168.10.0/26</code> | Usable Range: <code>192.168.10.1</code> to <code>192.168.10.62</code> | Broadcast: <code>192.168.10.63</code></li>
            <li><b>Subnet 1:</b> Network ID: <code>192.168.10.64/26</code> | Usable Range: <code>192.168.10.65</code> to <code>192.168.10.126</code> | Broadcast: <code>192.168.10.127</code></li>
            <li><b>Subnet 2:</b> Network ID: <code>192.168.10.128/26</code> | Usable Range: <code>192.168.10.129</code> to <code>192.168.10.190</code> | Broadcast: <code>192.168.10.191</code></li>
            <li><b>Subnet 3:</b> Network ID: <code>192.168.10.192/26</code> | Usable Range: <code>192.168.10.193</code> to <code>192.168.10.254</code> | Broadcast: <code>192.168.10.255</code></li>
        </ul>
    </div>

    <h3 class="sub-section-title">2.3 Network Address Translation (NAT / NAPT)</h3>
    <p>
        To prevent global IPv4 address exhaustion, <b>RFC 1918</b> reserved specific blocks for private internal networks:
    </p>
    <ul>
        <li><code>10.0.0.0/8</code> (10.0.0.0 &ndash; 10.255.255.255) &mdash; Single large private enterprise block.</li>
        <li><code>172.16.0.0/12</code> (172.16.0.0 &ndash; 172.31.255.255) &mdash; 16 contiguous private blocks.</li>
        <li><code>192.168.0.0/16</code> (192.168.0.0 &ndash; 192.255.255.255) &mdash; 256 contiguous home/office blocks.</li>
    </ul>
    <p>
        These private addresses cannot be routed across the public Internet. A <b>NAT router</b> sits at the network border and translates internal private IP addresses into a single registered public IP address using <b>Port Address Translation (NAPT / PAT)</b>:
    </p>
    <ul>
        <li><b>NAT Translation Table:</b> Maps tuples <code>(Private IP, Private Port) &harr; (Public IP, Assigned External Port)</code>.</li>
        <li><b>Outbound:</b> Router replaces internal source IP (e.g., <code>192.168.1.15:4500</code>) with public IP (e.g., <code>203.0.113.5:8001</code>) and records mapping.</li>
        <li><b>Inbound:</b> When replies return to port <code>8001</code>, NAT router looks up table and forwards packet to <code>192.168.1.15:4500</code>.</li>
        <li><b>Pros:</b> Conserves public IPv4 addresses; provides security (internal network invisible to outside scanners).<br/>
            <b>Cons:</b> Violates end-to-end network principle; breaks peer-to-peer protocols (VoIP, BitTorrent) without STUN/TURN relays.</li>
    </ul>

    <h2 class="section-title">3. IPv4 and IPv6 Datagram Formats (Ch. 18.4 & 22.2)</h2>

    <h3 class="sub-section-title">3.1 IPv4 Datagram Header</h3>
    <!-- FIG_IPV4 -->

    <ul>
        <li><b>VER (4 bits):</b> Version number; always <code>4</code> (binary <code>0100</code>).</li>
        <li><b>HLEN (4 bits):</b> Header Length in 4-byte (32-bit) words. Min value is 5 ($5 \times 4 = 20$ bytes without options); max value is 15 ($15 \times 4 = 60$ bytes).</li>
        <li><b>Service Type / DSCP (8 bits):</b> Quality of Service (QoS) classification (precedence, delay, throughput, reliability).</li>
        <li><b>Total Length (16 bits):</b> Entire length of datagram (Header + Data) in bytes. Maximum possible IPv4 datagram size = $2^{16} - 1 = 65,535$ bytes.</li>
        <li><b>Identification (16 bits):</b> Unique ID assigned by sender to identify all fragments belonging to the same original datagram.</li>
        <li><b>Flags (3 bits):</b>
            <ul>
                <li>Bit 0: Reserved (must be 0).</li>
                <li>Bit 1: <b>DF (Don't Fragment):</b> If 1, routers are forbidden from fragmenting. If MTU is too small, packet is dropped and ICMP "Fragmentation Needed" is sent.</li>
                <li>Bit 2: <b>MF (More Fragments):</b> If 1, more fragments follow. If 0, this is the last fragment.</li>
            </ul>
        </li>
        <li><b>Fragment Offset (13 bits):</b> Relative position of this fragment's data within the original unfragmented payload, <b>measured in units of 8 bytes</b>.</li>
        <li><b>Time to Live &mdash; TTL (8 bits):</b> Hop counter to prevent packets from looping endlessly. Every router decrements TTL by 1. When TTL reaches 0, the packet is discarded and an ICMP "Time Exceeded" is returned to the sender (used by <code>traceroute</code>).</li>
        <li><b>Protocol (8 bits):</b> Identifies the higher transport-layer protocol: <b>1 = ICMP, 6 = TCP, 17 = UDP, 89 = OSPF</b>.</li>
        <li><b>Header Checksum (16 bits):</b> Protects against header corruption during transit. Recomputed at every router because TTL changes!</li>
        <li><b>Source IP (32 bits) & Destination IP (32 bits):</b> IPv4 addresses of sender and final receiver.</li>
    </ul>

    <div class="exam-tip">
        <div class="title">⭐ Worked Numerical: IPv4 Fragmentation and Offset Calculation</div>
        <b>Problem:</b> An IPv4 datagram with Total Length = 4020 bytes (20-byte header + 4000-byte data) arrives at a router whose outgoing link has an <b>MTU (Maximum Transmission Unit) = 1500 bytes</b>. Show the fragment breakdown.<br/>
        <b>Rule:</b> Data size in each fragment must be a multiple of 8 bytes (since Fragment Offset is scaled by 8).<br/>
        Max data per fragment $\le 1500 - 20 = 1480$ bytes. 1480 is divisible by 8 ($1480 / 8 = 185$).<br/>
        <b>Fragment 1:</b><br/>
        • Total Length = $1480 + 20 = 1500$ bytes | Data bytes: $0 \dots 1479$ (1480 bytes)<br/>
        • Flags: $\text{MF} = 1$ (more fragments follow) | <b>Fragment Offset = $0 / 8 = 0$</b><br/>
        <b>Fragment 2:</b><br/>
        • Total Length = $1480 + 20 = 1500$ bytes | Data bytes: $1480 \dots 2959$ (1480 bytes)<br/>
        • Flags: $\text{MF} = 1$ | <b>Fragment Offset = $1480 / 8 = 185$</b><br/>
        <b>Fragment 3:</b><br/>
        • Remaining data = $4000 - 2960 = 1040$ bytes | Total Length = $1040 + 20 = 1060$ bytes<br/>
        • Flags: $\text{MF} = 0$ (last fragment!) | <b>Fragment Offset = $2960 / 8 = 370$</b>
    </div>

    <h3 class="sub-section-title">3.2 IPv6 Datagram Header & Enhancements</h3>
    <p>
        IPv6 addresses the total exhaustion of 32-bit IPv4 by offering <b>128-bit addresses</b> ($2^{128} \approx 3.4 \times 10^{38}$ addresses &mdash; enough to assign millions of IPs to every atom on Earth!).
    </p>

    <!-- FIG_IPV6 -->

    <h4>Key Advantages of IPv6 over IPv4:</h4>
    <ul>
        <li><b>Fixed 40-byte Base Header:</b> Eliminates HLEN and options parsing. Routers process headers in hardware at wire speed.</li>
        <li><b>No Header Checksum:</b> Checksums are handled at Data Link (CRC) and Transport (TCP/UDP). Removing it eliminates recomputing checksums at every hop!</li>
        <li><b>No Router-level Fragmentation:</b> Routers never fragment packets. End-hosts use <b>Path MTU Discovery</b>. If packet is too large, router sends ICMPv6 "Packet Too Big".</li>
        <li><b>Extension Headers:</b> Inserted between base header and payload via a daisy-chain <b>Next Header</b> pointer (Hop-by-hop options, Routing, Fragment, ESP, AH).</li>
        <li><b>Built-in Security:</b> Mandatory support for <b>IPsec</b> (Encryption and Authentication).</li>
    </ul>

    <h2 class="section-title">4. Routing Algorithms: DVR, LSR, and PVR (Ch. 20.1 - 20.3)</h2>
    <p>
        Routing protocols allow routers to continuously share knowledge of network topology and calculate the least-cost path to every destination.
    </p>

    <h3 class="sub-section-title">4.1 Distance Vector Routing (DVR & Bellman-Ford)</h3>
    <ul>
        <li><b>Philosophy:</b> <i>"Tell your neighbors about the entire world."</i></li>
        <li>Each router maintains a vector (table) of distances: <code>Cost to every destination, Next-hop router</code>.</li>
        <li><b>Bellman-Ford Equation:</b> $D_x(y) = \min_v \{ c(x, v) + D_v(y) \}$, where $v$ ranges over all neighbors of $x$.</li>
        <li><b>Count-to-Infinity Problem:</b> Good news (link cost decrease) propagates rapidly, but bad news (link failure or cost increase) propagates extremely slowly through loops because routers advertise paths to each other that depend on each other.
            <br/><b>Solutions:</b>
            <ul>
                <li><i>Split Horizon:</i> Do not advertise a route back to the neighbor from whom it was learned.</li>
                <li><i>Poison Reverse:</i> Advertise that route back to that neighbor with cost = $\infty$ (infinity).</li>
            </ul>
        </li>
    </ul>

    <h3 class="sub-section-title">4.2 Link State Routing (LSR & Dijkstra's Algorithm)</h3>
    <ul>
        <li><b>Philosophy:</b> <i>"Tell the entire world about your immediate neighbors."</i></li>
        <li><b>Five Steps of Link State Routing:</b>
            <ol>
                <li><i>Neighbor Discovery:</i> Router sends <code>HELLO</code> packets on all links to discover direct neighbors.</li>
                <li><i>Link Cost Measurement:</i> Router measures delay or bandwidth cost to each neighbor (e.g., using echo packets).</li>
                <li><i>LSP Construction:</i> Router builds a <b>Link State Packet (LSP)</b> containing its ID, sequence number, age, and list of direct neighbors with link costs.</li>
                <li><i>Reliable Flooding:</i> Floods the LSP to <i>every other router</i> in the network. Every router builds an identical <b>Link State Database (LSDB)</b> &mdash; a complete network topology map.</li>
                <li><i>Dijkstra's SPF Computation:</i> Each router independently runs <b>Dijkstra's Shortest Path First</b> algorithm on the LSDB, producing a shortest path tree with itself as the root.</li>
            </ol>
        </li>
    </ul>

    <!-- FIG_DIJKSTRA -->

    <div class="exam-tip">
        <div class="title">⭐ Step-by-Step Dijkstra Algorithm Trace (Source Node A)</div>
        Let graph be: Neighbors of A: B(cost 2), C(cost 5). From B: D(cost 3), C(cost 1). From C: E(cost 2). From D: Z(cost 1). From E: Z(cost 4).<br/>
        <table>
            <tr>
                <th>Step</th>
                <th>Confirmed Set $N$</th>
                <th>$D(B), p(B)$</th>
                <th>$D(C), p(C)$</th>
                <th>$D(D), p(D)$</th>
                <th>$D(E), p(E)$</th>
                <th>$D(Z), p(Z)$</th>
            </tr>
            <tr>
                <td><b>0</b></td>
                <td>{A}</td>
                <td><b>2, A</b></td>
                <td>5, A</td>
                <td>&infin;</td>
                <td>&infin;</td>
                <td>&infin;</td>
            </tr>
            <tr>
                <td><b>1</b></td>
                <td>{A, B}</td>
                <td>(Permanent: 2)</td>
                <td>$\min(5, 2+1) = \mathbf{3, B}$</td>
                <td>$2+3 = \mathbf{5, B}$</td>
                <td>&infin;</td>
                <td>&infin;</td>
            </tr>
            <tr>
                <td><b>2</b></td>
                <td>{A, B, C}</td>
                <td>(Permanent)</td>
                <td>(Permanent: 3)</td>
                <td>5, B</td>
                <td>$3+2 = \mathbf{5, C}$</td>
                <td>&infin;</td>
            </tr>
            <tr>
                <td><b>3</b></td>
                <td>{A, B, C, D}</td>
                <td>(Permanent)</td>
                <td>(Permanent)</td>
                <td>(Permanent: 5)</td>
                <td>5, C</td>
                <td>$5+1 = \mathbf{6, D}$</td>
            </tr>
            <tr>
                <td><b>4</b></td>
                <td>{A, B, C, D, E}</td>
                <td>(Permanent)</td>
                <td>(Permanent)</td>
                <td>(Permanent)</td>
                <td>(Permanent: 5)</td>
                <td>$\min(6, 5+4) = \mathbf{6, D}$</td>
            </tr>
            <tr>
                <td><b>5</b></td>
                <td>{A, B, C, D, E, Z}</td>
                <td colspan="5">Shortest path from <b>A &rarr; Z</b> is <b>A &rarr; B &rarr; D &rarr; Z</b> with <b>Total Cost = 6</b>!</td>
            </tr>
        </table>
    </div>

    <h3 class="sub-section-title">4.3 Path Vector Routing (PVR)</h3>
    <p>
        Used for inter-domain routing where distance vector and link state fail due to scalability and policy conflicts. Instead of advertising costs, routers advertise the <b>entire sequence of Autonomous Systems (AS Path)</b> traversed to reach the destination:
    </p>
    <ul>
        <li><b>Loop Prevention:</b> If a router sees its own AS number in the advertised AS Path, it immediately drops the advertisement, preventing loops completely.</li>
        <li><b>Policy Enforcement:</b> Allows network providers to refuse traffic from competitors or prefer paths based on economic agreements rather than pure shortest hop count.</li>
    </ul>

    <h2 class="section-title">5. Unicast Routing Protocols in Practice: RIP, OSPF, and BGP (Ch. 20.3)</h2>
    <table>
        <tr>
            <th>Protocol</th>
            <th>Type & Algorithm</th>
            <th>Metric Used</th>
            <th>Domain / Scope</th>
            <th>Transport Layer Protocol & Port</th>
        </tr>
        <tr>
            <td><b>RIP (v1, v2)</b><br/>Routing Information Protocol</td>
            <td>Distance Vector (Bellman-Ford)</td>
            <td><b>Hop Count</b><br/>(Max 15 hops; 16 = &infin; unreachable)</td>
            <td>Intra-AS (IGP) for small networks</td>
            <td><b>UDP Port 520</b> (Periodic broadcast/multicast every 30s)</td>
        </tr>
        <tr>
            <td><b>OSPF</b><br/>Open Shortest Path First</td>
            <td>Link State (Dijkstra SPF)</td>
            <td><b>Cost &prop; $\frac{10^8}{\text{Bandwidth}}$</b></td>
            <td>Intra-AS (IGP) for large enterprise networks</td>
            <td>Directly over IP (<b>Protocol 89</b>) &mdash; no transport overhead!</td>
        </tr>
        <tr>
            <td><b>BGP (BGP-4)</b><br/>Border Gateway Protocol</td>
            <td>Path Vector (PVR)</td>
            <td>Policy & AS Path length</td>
            <td><b>Inter-AS (EGP)</b> &mdash; Gluing the global Internet</td>
            <td><b>TCP Port 179</b> (Reliable permanent connection)</td>
        </tr>
    </table>

    <h3 class="sub-section-title">5.1 Open Shortest Path First (OSPF) Details</h3>
    <ul>
        <li><b>Hierarchical Area Structure:</b> Large Autonomous Systems are subdivided into <b>Areas</b>. Area 0 is the <b>Backbone Area</b>. All other areas must connect to Area 0 through <b>Area Border Routers (ABR)</b>. Routers connecting to external ASs are <b>Autonomous System Boundary Routers (ASBR)</b>.</li>
        <li><b>OSPF Packet Types:</b>
            <ol>
                <li><i>Hello (Type 1):</i> Establishes and maintains neighbor relationships; elects Designated Router (DR) and Backup DR (BDR).</li>
                <li><i>Database Description - DBD (Type 2):</i> Summarizes LSDB contents during adjacency initialization.</li>
                <li><i>Link State Request - LSR (Type 3):</i> Requests full details of specific outdated LSPs.</li>
                <li><i>Link State Update - LSU (Type 4):</i> Transmits newly advertised LSPs (reliable flooding).</li>
                <li><i>Link State Acknowledgment - LSAck (Type 5):</i> Explicitly acknowledges received LSUs.</li>
            </ol>
        </li>
    </ul>

    <h2 class="section-title">6. Multicasting Routing: MOSPF (Ch. 21.3.2)</h2>
    <ul>
        <li><b>Unicast vs Broadcast vs Multicast:</b> Unicast = 1-to-1; Broadcast = 1-to-All; Multicast = 1-to-Group (delivers one stream to multiple designated receivers without replicating packets across shared links).</li>
        <li><b>Multicast Trees:</b>
            <ul>
                <li><i>Source-Based Tree:</i> A separate shortest path distribution tree is calculated for each source sending to the group.</li>
                <li><i>Group-Shared Tree:</i> A single shared rendezvous point / core router acts as the root of the tree for all sources.</li>
            </ul>
        </li>
        <li><b>MOSPF (Multicast OSPF):</b> An extension of OSPF for multicasting. Routers broadcast a new <b>Group-Membership LSA</b> detailing which multicast groups have active listeners on their subnets. When a multicast packet arrives from source $S$ to group $G$, the router computes an on-demand Dijkstra shortest-path source-based tree rooted at $S$ to forward packets only down branches leading to active group members.</li>
    </ul>
    """
    return (content.replace('<!-- FIG_IPV4 -->', fig_ipv4_header()).replace('<!-- FIG_IPV6 -->', fig_ipv6_header()).replace('<!-- FIG_DIJKSTRA -->', fig_dijkstra_graph()))
