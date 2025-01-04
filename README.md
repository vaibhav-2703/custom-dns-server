<h2 id="🌐-custom-dns-server">🌐 Custom DNS Server</h2>
<p>A sleek and efficient Python-based DNS server. It resolves custom domains, supports multiple DNS record types, and forwards unresolved queries to an upstream server. Perfect for testing, learning, or lightweight usage.</p>
<h2 id="🚀-features">🚀 Features</h2>
<ul>
<li>Custom Domain Resolution: Resolve queries for your predefined domain (e.g., example.com).</li>
<li>DNS Record Support: Supports A, AAAA, MX, CNAME, SOA, NS.</li>
<li>Query Forwarding: Forwards unresolved queries to an upstream DNS server (1.1.1.1 by default).</li>
<li>Dual Protocol Support: Handles both UDP and TCP DNS requests.</li>
<li>Configurable: Easily modify domain, TTL, IP, and forwarder settings.</li>
<li>Multithreaded: Efficiently manages multiple queries simultaneously.</li>
</ul>
<h2 id="🛠️-installation">🛠️ Installation</h2>
<ul>
<li>Step 1: Clone the Repository</li>
</ul>
<pre><code>git clone https://github.com/yourusername/custom-dns-server.git
cd custom-dns-server
</code></pre>
<ul>
<li>Step 2: Install Dependencies</li>
</ul>
<p>Ensure Python 3.6+ is installed, then install the required libraries:</p>
<pre><code>pip install dnslib
</code></pre>
<h2 id="▶️-usage">▶️ Usage</h2>
<p>Start the DNS server with customizable options:</p>
<pre><code>python dnsss.py --udp --tcp --port 5053
</code></pre>
<ul>
<li>Available Arguments:</li>
</ul>
<pre><code>    --port: Specify the port to listen on (default: 5053).
    --udp: Enable the UDP protocol.
    --tcp: Enable the TCP protocol.
</code></pre>
<h3 id="⚠️-note-at-least-one-of---udp-or---tcp-must-be-specified">⚠️ Note: At least one of --udp or --tcp must be specified.</h3>
<h2 id="📋-how-it-works">📋 How It Works:</h2>
<pre><code>Custom Records:
    Predefined DNS records are used to handle queries for example.com and its subdomains.
    Examples:
        A Record: IPv4 address mapping.
        AAAA Record: IPv6 address mapping.
        MX Record: Mail server routing.
        CNAME Record: Alias to another domain.
        SOA Record: Administrative information.
        NS Record: Name servers.

Dynamic Query Forwarding:
    Queries that don’t match predefined records are forwarded to an upstream DNS server (1.1.1.1 by default).

Multithreading:
    Uses threading to handle multiple requests simultaneously, improving performance.
</code></pre>
<h2 id="🗃️-predefined-dns-records">🗃️ Predefined DNS Records</h2>
<pre><code>By default, the following DNS records are defined for example.com:
Record Type	Value
A	127.0.0.1
AAAA	(0,) * 16 (IPv6)
MX	mail.example.com
NS	ns1.example.com
CNAME	Alias for example.com
SOA	Primary domain server info
</code></pre>
<p>These can be customized in the script to suit your needs.</p>
<h2 id="🔧-configuration">🔧 Configuration</h2>
<p>Adjust the following constants in the script to personalize your DNS server:</p>
<pre><code>Domain Name: DOMAIN_NAME (e.g., mydomain.com.).
IP Address: IP_ADDRESS (e.g., 192.168.1.1).
TTL (Time to Live): TTL (e.g., 600 seconds).
Upstream Forwarder: FORWARDER (e.g., 1.1.1.1).
</code></pre>
<h2 id="🧪-testing">🧪 Testing</h2>
<pre><code>Using dig

dig @127.0.0.1 -p 5053 example.com

Using nslookup

nslookup example.com 127.0.0.1
</code></pre>
<h2 id="👩💻-contributing">👩‍💻 Contributing</h2>
<p>We welcome contributions! Follow these steps:</p>
<ul>
<li>Fork the repository.</li>
<li>Create a new branch:</li>
</ul>
<pre><code>git checkout -b feature-name
</code></pre>
<ul>
<li>Commit your changes:</li>
</ul>
<pre><code>git commit -m &quot;Add feature-name&quot;
</code></pre>
<ul>
<li>Push to your branch:</li>
</ul>
<pre><code>    git push origin feature-name
</code></pre>
<ul>
<li>Create a Pull Request.</li>
</ul>
<h2 id="📜-license">📜 License</h2>
<p>This project is licensed under the MIT License. See the LICENSE file for details.</p>
<h2 id="📖-acknowledgments">📖 Acknowledgments</h2>
<pre><code>Built using the powerful dnslib library.
Inspired by the need for a lightweight, customizable DNS server.
</code></pre>
<h2 id="🛡️-disclaimer">🛡️ Disclaimer</h2>
<p>This server is intended for educational and testing purposes. It is not optimized for production use and should not be deployed in environments requiring high security or performance.</p>
