"""
Module 1: Introduction to Data Communications, Networks, Network Models, Physical Layer, and Switching.
"""
from diagrams import fig_data_comm_components, fig_topologies, fig_osi_vs_tcpip, fig_packet_switching

def get_module_1_content():
    content = r"""
    <h1 class="module-title">MODULE 1 &mdash; Introduction to Data Communications, Network Models, Physical Layer & Switching</h1>

    <div class="eli5-box">
        <div class="title">💡 ELI5 (Explain Like I'm 5): What is a Computer Network?</div>
        Imagine you and your best friend live across the street and want to talk without yelling. You connect a string between two tin cans (Physical Medium). When you speak (Sender), your voice makes vibrations (Message) that travel across the string to the friend's can (Receiver). But wait! What if you speak English and your friend only speaks Spanish? You won't understand each other! You must both agree on rules: "We will both speak English, one person talks at a time, and we say 'Over' when finished." Those agreed rules are called the <b>Protocol</b>. A computer network is just millions of computers doing this across the entire world!
    </div>

    <h2 class="section-title">1. Introduction to Data Communications (Ch. 1.1)</h2>
    <p>
        <b>Data Communications</b> is the exchange of data between two devices via some form of transmission medium (such as a wire cable or wireless radio waves). For data communication to be effective, the system must deliver data to the correct destination (<b>Delivery</b>), accurately without alterations (<b>Accuracy</b>), in a timely fashion without significant jitter (<b>Timeliness</b>), and with minimal variation in packet arrival times (<b>Jitter</b>).
    </p>

    <h3 class="sub-section-title">1.1 Five Fundamental Components of Data Communication</h3>
    <!-- FIG_1 -->
    <ul>
        <li><b>1. Message:</b> The information (data) to be communicated. Popular forms include text, numbers, images, audio, and video.</li>
        <li><b>2. Sender:</b> The device that creates and sends the data message (e.g., computer, smartphone, video camera).</li>
        <li><b>3. Receiver:</b> The device that receives the message (e.g., workstation, server, printer, television).</li>
        <li><b>4. Transmission Medium:</b> The physical path by which a message travels from sender to receiver (e.g., twisted-pair wire, coaxial cable, fiber-optic cable, or radio waves).</li>
        <li><b>5. Protocol:</b> A set of formal rules that govern data communications. It represents an agreement between communicating devices; without a protocol, two devices may be connected, but cannot communicate (like two humans who speak different languages).</li>
    </ul>

    <h3 class="sub-section-title">1.2 Data Representation & Data Flow</h3>
    <p>Information today comes in various digital formats:</p>
    <ul>
        <li><b>Text:</b> Represented as bit patterns using standard codes such as ASCII (7-bit), Unicode (UTF-8, UTF-16, UTF-32) allowing representation of symbols in any language.</li>
        <li><b>Numbers:</b> Converted directly to binary numbers for arithmetic processing.</li>
        <li><b>Images:</b> Represented as a matrix of pixels. Each pixel is assigned a bit pattern representing color and intensity (e.g., RGB 24-bit true color).</li>
        <li><b>Audio & Video:</b> Continuous analog signals converted into digital streams through sampling and quantization (PCM). Video is a sequence of continuous picture frames.</li>
    </ul>

    <h4>Direction of Data Flow: Simplex, Half-Duplex, and Full-Duplex</h4>
    <table>
        <tr>
            <th>Direction Mode</th>
            <th>Description & Channel Capacity</th>
            <th>Real-World Analogy</th>
            <th>Practical Examples</th>
        </tr>
        <tr>
            <td><b>Simplex</b></td>
            <td>Unidirectional communication. Only one device transmits, and the other can only receive. The entire channel capacity is dedicated to one direction.</td>
            <td>A one-way street; a television broadcast.</td>
            <td>Keyboards, traditional monitors, TV/Radio broadcasting.</td>
        </tr>
        <tr>
            <td><b>Half-Duplex</b></td>
            <td>Bidirectional, but only one device can transmit at any given instant. When one sends, the other must listen. Full capacity is used alternately.</td>
            <td>A narrow single-lane bridge where cars take turns.</td>
            <td>Walkie-talkies; early Ethernet hubs (CSMA/CD).</td>
        </tr>
        <tr>
            <td><b>Full-Duplex (Duplex)</b></td>
            <td>Simultaneous bidirectional transmission. Both stations can transmit and receive concurrently. The channel capacity is divided between the two directions.</td>
            <td>A two-lane highway with traffic flowing both ways.</td>
            <td>Telephone networks, modern switched Ethernet.</td>
        </tr>
    </table>

    <h2 class="section-title">2. Networks and Network Types (Ch. 1.2 & 1.3)</h2>
    <p>
        A <b>Network</b> is a set of devices (often referred to as nodes or hosts) connected by communication links. A node can be a computer, printer, switch, router, or any other device capable of sending and receiving data.
    </p>

    <h3 class="sub-section-title">2.1 Network Criteria</h3>
    <ul>
        <li><b>Performance:</b> Measured in terms of <b>Throughput</b> (actual data delivered successfully per unit time, bps) and <b>Delay / Latency</b> (time taken for a message to travel from sender to receiver, including propagation time, transmission time, queuing delay, and processing delay).</li>
        <li><b>Reliability:</b> Measured by frequency of failure, the time it takes to recover from a failure (<b>MTTR</b> &mdash; Mean Time To Repair), and the system's robustness in a catastrophe.</li>
        <li><b>Security:</b> Protecting data from unauthorized access, damage, viruses, and implementing data integrity and privacy policies.</li>
    </ul>

    <h3 class="sub-section-title">2.2 Physical Structures & Topologies</h3>
    <p>A network is defined by its type of connection and its physical topology:</p>
    <ul>
        <li><b>Point-to-Point Connection:</b> Provides a dedicated link between two devices. The entire channel capacity is reserved for transmission between those two endpoints.</li>
        <li><b>Multipoint (Multidrop) Connection:</b> A single communication link is shared simultaneously or in time-sharing mode by more than two devices.</li>
    </ul>

    <!-- FIG_2 -->

    <table>
        <tr>
            <th>Topology</th>
            <th>Link Formula & Complexity</th>
            <th>Key Advantages</th>
            <th>Disadvantages</th>
        </tr>
        <tr>
            <td><b>Mesh</b></td>
            <td>Dedicated point-to-point links.<br/><b>Number of duplex links = n(n - 1) / 2</b><br/><b>I/O ports per device = n - 1</b></td>
            <td>High fault tolerance (if one link fails, others work); dedicated privacy and security; no traffic congestion bottlenecks.</td>
            <td>Massive cable cost; heavy installation and maintenance burden; high hardware port cost.</td>
        </tr>
        <tr>
            <td><b>Star</b></td>
            <td>Each device connects to a central hub/switch via a dedicated point-to-point link.<br/><b>Number of links = n</b></td>
            <td>Easy to install and reconfigure; failure of one node does not affect others; centralized management and fault identification.</td>
            <td>Single point of failure (if central hub/switch fails, entire network goes down); requires more cable than bus.</td>
        </tr>
        <tr>
            <td><b>Bus</b></td>
            <td>Multipoint configuration. One long central cable (backbone) with tap/drop lines.<br/>Terminators at cable ends.</td>
            <td>Economical and simple to install; uses minimal cabling for small networks.</td>
            <td>Difficult fault detection; signal reflection at broken ends; backbone break halts whole network; heavy traffic causes high collisions.</td>
        </tr>
        <tr>
            <td><b>Ring</b></td>
            <td>Each device has a dedicated point-to-point connection with only two neighbors. Unidirectional token circulating loop.</td>
            <td>Easy to install and reconfigure; fault isolation is simplified by token-ring monitors.</td>
            <td>A break in the ring can disable the entire network (unless dual counter-rotating rings are deployed, as in FDDI).</td>
        </tr>
        <tr>
            <td><b>Hybrid</b></td>
            <td>Combines two or more basic topologies (e.g., Star-Bus or Star-Ring).</td>
            <td>Scalable and flexible; customized to institutional layout.</td>
            <td>Complex architecture and higher installation cost.</td>
        </tr>
    </table>

    <h3 class="sub-section-title">2.3 Network Categories (LAN, MAN, WAN)</h3>
    <ul>
        <li><b>Local Area Network (LAN):</b> Spans a small geographical area (an office, home, or university campus). Usually privately owned, operates with high data rates (100 Mbps to 10 Gbps) and very low error rates.</li>
        <li><b>Metropolitan Area Network (MAN):</b> Spans an entire city or town (e.g., cable television network across a city).</li>
        <li><b>Wide Area Network (WAN):</b> Provides long-distance transmission over large geographic areas (countries, continents). Typically comprised of:
            <ul>
                <li><i>Point-to-Point WAN:</i> Connects two specific communication devices through a leased line or transmission provider.</li>
                <li><i>Switched WAN:</i> A network connecting multiple end nodes through a mesh of packet/circuit switches (e.g., Asynchronous Transfer Mode - ATM, Frame Relay, or the core Internet).</li>
            </ul>
        </li>
        <li><b>Internetworks (The Internet):</b> An interconnection of two or more independent networks joined by internetworking devices (routers and gateways).</li>
    </ul>

    <h2 class="section-title">3. Network Models: Protocol Layering & OSI vs TCP/IP (Ch. 2.1 - 2.3)</h2>
    <div class="eli5-box">
        <div class="title">💡 ELI5: Why do we use Protocol Layering? (The Postal Service Analogy)</div>
        When you write a letter to your friend in another country:
        1. <b>Application Layer:</b> You write your message on paper.
        2. <b>Packaging:</b> You put it in an envelope and write the name and address.
        3. <b>Local Post Office:</b> Sorts the mail and decides the route.
        4. <b>Transport / Cargo Flight:</b> Flies the mail bag across oceans.
        The airplane pilot doesn't need to read your letter or understand English! The pilot only cares about flying the cargo bag. Layering creates modular independence: each layer solves one specific job and trusts the layer below it.
    </div>

    <h3 class="sub-section-title">3.1 Principles of Protocol Layering</h3>
    <ul>
        <li><b>Modularity:</b> Complex communication tasks are divided into smaller, self-contained sub-tasks.</li>
        <li><b>Explicit Interfaces:</b> Each layer provides well-defined services to the layer immediately above it and receives services from the layer below it.</li>
        <li><b>Independence:</b> An implementation at one layer can be swapped out (e.g., changing from Wi-Fi to Ethernet) without breaking the higher application layers.</li>
    </ul>

    <!-- FIG_3 -->

    <h3 class="sub-section-title">3.2 The 7-Layer OSI Reference Model</h3>
    <p>Developed by the International Organization for Standardization (ISO). From bottom to top:</p>
    <ol>
        <li><b>Layer 1 &mdash; Physical Layer:</b> Transmits raw bits over a physical transmission medium. Defines mechanical, electrical, and functional specifications (voltage levels, pin layouts, bit timing, data rates).</li>
        <li><b>Layer 2 &mdash; Data Link Layer (DLL):</b> Transforms an unreliable raw physical transmission facility into a reliable link. Groups bits into <b>Frames</b>. Handles physical (MAC) addressing, error detection & correction, flow control, and access control.</li>
        <li><b>Layer 3 &mdash; Network Layer:</b> Responsible for source-to-destination delivery of individual <b>Packets</b> across multiple networks. Provides logical addressing (IP addresses) and <b>Routing</b> (choosing the best path through intermediate routers).</li>
        <li><b>Layer 4 &mdash; Transport Layer:</b> Provides end-to-end (process-to-process) communication. Breaks application messages into <b>Segments</b>, assigns sequence numbers, manages flow control, error recovery, and port addressing (multiplexing/demultiplexing).</li>
        <li><b>Layer 5 &mdash; Session Layer:</b> Establishes, manages, and terminates communication sessions between applications. Provides dialog control (half-duplex/full-duplex) and synchronization checkpoints.</li>
        <li><b>Layer 6 &mdash; Presentation Layer:</b> Handles the syntax and semantics of the information exchanged. Responsible for <b>Translation</b> (character encoding like ASCII/Unicode), <b>Encryption/Decryption</b> (security), and <b>Compression</b>.</li>
        <li><b>Layer 7 &mdash; Application Layer:</b> Provides interfaces and protocols directly to user applications and network services (HTTP, FTP, SMTP, DNS).</li>
    </ol>

    <h3 class="sub-section-title">3.3 The 5-Layer TCP/IP Protocol Suite</h3>
    <p>
        The commercial Internet was built on the TCP/IP protocol suite. In TCP/IP, the Session and Presentation functions are handled within the Application layer itself, yielding a streamlined 5-layer model: <b>Application, Transport, Network (Internet), Data Link, and Physical</b>.
    </p>

    <div class="key-point">
        <div class="title">🔑 Addressing in the TCP/IP Protocol Suite (Crucial for Exams)</div>
        Four distinct levels of addresses are used across the TCP/IP layers:
        <ul>
            <li><b>1. Physical (MAC) Address:</b> 48-bit hardware address (e.g., <code>00:1A:2B:3C:4D:5E</code>) used by the Data Link Layer to deliver frames within the same local network link.</li>
            <li><b>2. Logical (IP) Address:</b> 32-bit (IPv4) or 128-bit (IPv6) global address (e.g., <code>192.168.1.1</code>) used by the Network Layer for global end-to-end packet delivery.</li>
            <li><b>3. Port Address:</b> 16-bit integer (e.g., Port 80 for HTTP, Port 53 for DNS) used by the Transport Layer to identify the specific application process running on a host.</li>
            <li><b>4. Specific (Application) Address:</b> User-friendly identifiers like URLs (<code>www.google.com</code>) or email addresses (<code>user@domain.com</code>) used at the Application Layer.</li>
        </ul>
    </div>

    <h2 class="section-title">4. Physical Layer: Transmission Media (Ch. 7.1 - 7.3)</h2>
    <p>
        Transmission media are located beneath the physical layer and are controlled by it. Media are broadly categorized into <b>Guided (Wired/Bounded)</b> and <b>Unguided (Wireless/Unbounded)</b>.
    </p>

    <h3 class="sub-section-title">4.1 Guided Media</h3>
    <table>
        <tr>
            <th>Cable Type</th>
            <th>Physical Structure & Principle</th>
            <th>Categories / Standards</th>
            <th>Advantages & Limitations</th>
        </tr>
        <tr>
            <td><b>Twisted-Pair Cable</b></td>
            <td>Two insulated copper conductors twisted around each other in a helical spiral. Twisting reduces electromagnetic interference (crosstalk) because noise affects both wires equally and cancels out differentially. Available as <b>UTP</b> (Unshielded) and <b>STP</b> (Shielded with metal foil).</td>
            <td>Cat 5 (100 MHz, 100 Mbps), Cat 5e (1 Gbps), Cat 6 (250 MHz, 10 Gbps up to 55m), Cat 6a.<br/>Connector: <b>RJ-45</b>.</td>
            <td><b>Pros:</b> Cheap, flexible, easy to install.<br/><b>Cons:</b> High attenuation over distance (repeater needed every 100m); lower bandwidth compared to fiber.</td>
        </tr>
        <tr>
            <td><b>Coaxial Cable</b></td>
            <td>Central solid copper conductor surrounded by an insulating dielectric layer, wrapped in a braided metal mesh outer conductor, encased in a plastic jacket. Inner conductor carries signals; outer shield acts as ground and blocks external EMI.</td>
            <td>RG-59 (75 &Omega;, TV), RG-58 (50 &Omega;, Thin Ethernet 10Base2), RG-11 (50 &Omega;, Thick Ethernet 10Base5).<br/>Connectors: <b>BNC, BNC T-connector, BNC Terminator</b>.</td>
            <td><b>Pros:</b> Higher bandwidth and better noise immunity than twisted-pair.<br/><b>Cons:</b> Bulky, difficult to install, more expensive.</td>
        </tr>
        <tr>
            <td><b>Fiber-Optic Cable</b></td>
            <td>Glass or plastic core surrounded by a glass cladding of lower refractive index ($n_2 < n_1$), enclosed in Kevlar strength fibers and a protective jacket. Transmits light pulses via <b>Total Internal Reflection (TIR)</b> whenever the angle of incidence exceeds the critical angle.</td>
            <td><b>Propagation Modes:</b><br/>• <i>Multimode Step-Index:</i> Light bounces at multiple angles; causes modal dispersion.<br/>• <i>Multimode Graded-Index:</i> Refractive index decreases gradually; light curves, reducing dispersion.<br/>• <i>Single-Mode:</i> Extremely narrow core (8-10 &mu;m); light travels straight along axis. Zero modal dispersion.<br/>Connectors: <b>SC, ST, LC</b>.</td>
            <td><b>Pros:</b> Immense bandwidth (Terabits/sec), ultra-low attenuation, complete immunity to electromagnetic interference (EMI), zero crosstalk, highly secure against tapping.<br/><b>Cons:</b> Expensive, fragile glass, requires specialized optical splicing equipment.</td>
        </tr>
    </table>

    <h3 class="sub-section-title">4.2 Unguided Media: Wireless Communication</h3>
    <ul>
        <li><b>Radio Waves (3 kHz to 1 GHz):</b> Omnidirectional (propagate in all directions). Can penetrate solid walls, making them ideal for indoor and outdoor mobile communication (AM/FM radio, cordless phones, cellular networks). Highly susceptible to interference.</li>
        <li><b>Microwaves (1 GHz to 300 GHz):</b> Unidirectional (focused narrow beams). Require clear <b>Line-of-Sight (LOS)</b> between transmitting and receiving antennas. Cannot penetrate walls. Used in:
            <ul>
                <li><i>Terrestrial Microwave:</i> Parabolic dish and horn antennas mounted on high towers (repeater spacing 30-50 km due to earth curvature).</li>
                <li><i>Satellite Microwave:</i> Geostationary satellites (altitude 35,786 km) act as microwave repeaters in the sky.</li>
            </ul>
        </li>
        <li><b>Infrared Waves (300 GHz to 400 THz):</b> Very high frequency, cannot penetrate opaque walls. Used for short-range line-of-sight communication (TV remote controls, IrDA wireless mouse), preventing interference between adjacent rooms.</li>
    </ul>

    <h2 class="section-title">5. Switching: Packet Switching and its Types (Ch. 8.3)</h2>
    <p>
        In large networks, a direct point-to-point connection between every pair of nodes is impossible. A switched network connects multiple devices through intermediate switching nodes. While circuit switching reserves a dedicated physical path (used in legacy telephone calls), modern data networks use <b>Packet Switching</b>.
    </p>

    <!-- FIG_4 -->

    <h3 class="sub-section-title">5.1 Datagram Networks (Connectionless)</h3>
    <ul>
        <li><b>Working Principle:</b> The message is divided into independent packets called <b>datagrams</b>. Each datagram contains the complete destination IP address in its header.</li>
        <li><b>Routing:</b> Each router evaluates the destination address of every packet independently and looks up its routing table to choose the next hop. Packets belonging to the same message may take different routes depending on network congestion and link failures.</li>
        <li><b>Characteristics:</b> No connection setup phase; packets may arrive out of order or be delayed; routers do not maintain per-connection state tables (highly fault-tolerant). This is the underlying architecture of the <b>Internet Protocol (IP)</b>.</li>
    </ul>

    <h3 class="sub-section-title">5.2 Virtual-Circuit Networks (Connection-Oriented)</h3>
    <ul>
        <li><b>Working Principle:</b> A single logical connection path called a <b>Virtual Circuit (VC)</b> is established between source and destination before data packets are transmitted.</li>
        <li><b>Three Phases:</b>
            <ol>
                <li><i>Setup Phase:</i> A setup frame travels from source to destination, establishing entries in the switching tables and assigning local <b>Virtual Circuit Identifiers (VCI)</b> at each switch.</li>
                <li><i>Data Transfer Phase:</i> Packets carry only the short VCI (not full 32-bit or 128-bit addresses). All packets follow the exact same pre-determined physical route in sequential order.</li>
                <li><i>Teardown Phase:</i> When communication ends, a teardown signal releases the table entries and bandwidth along the path.</li>
            </ol>
        </li>
        <li><b>Characteristics:</b> Guaranteed in-order packet arrival; predictable delay; but vulnerable to link failures (if a switch on the path crashes, the entire connection drops and must be re-established). Used in ATM, Frame Relay, and MPLS.</li>
    </ul>

    <div class="exam-tip">
        <div class="title">⭐ High-Yield Exam Comparison: Datagram vs Virtual Circuit Networks</div>
        <table>
            <tr>
                <th>Parameter</th>
                <th>Datagram Network</th>
                <th>Virtual-Circuit Network</th>
            </tr>
            <tr>
                <td><b>Connection setup</b></td>
                <td>None (immediate transmission)</td>
                <td>Mandatory setup & teardown phases</td>
            </tr>
            <tr>
                <td><b>Packet addressing</b></td>
                <td>Full Source & Destination IP addresses in each packet</td>
                <td>Short Virtual Circuit Identifier (VCI)</td>
            </tr>
            <tr>
                <td><b>Packet routing</b></td>
                <td>Each packet routed independently; paths may vary</td>
                <td>All packets follow the identical established path</td>
            </tr>
            <tr>
                <td><b>Arrival order</b></td>
                <td>Packets may arrive out-of-order</td>
                <td>Packets guaranteed to arrive in sequence</td>
            </tr>
            <tr>
                <td><b>Router state</b></td>
                <td>Stateless (no per-flow connection state stored)</td>
                <td>Stateful (switches store VCI translation tables)</td>
            </tr>
            <tr>
                <td><b>Effect of router crash</b></td>
                <td>Minimal: upcoming packets simply routed around failure</td>
                <td>Fatal: all active VCs passing through the router terminate</td>
            </tr>
        </table>
    </div>
    """
    return (content.replace('<!-- FIG_1 -->', fig_data_comm_components()).replace('<!-- FIG_2 -->', fig_topologies()).replace('<!-- FIG_3 -->', fig_osi_vs_tcpip()).replace('<!-- FIG_4 -->', fig_packet_switching()))
