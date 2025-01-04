import argparse
import datetime
import sys
import time
import threading
import traceback
import socketserver
import struct
import socket
from dnslib import DNSRecord, DNSHeader, QTYPE, RR, A, AAAA, MX, SOA, NS, CNAME

# ============================
# Constants and Configurations
# ============================
DOMAIN_NAME = 'example.com.'
IP_ADDRESS = '127.0.0.1'
TTL = 300  # Time to live in seconds
FORWARDER = '1.1.1.1'  # Upstream DNS server

try:
    from dnslib import *
except ImportError:
    print("Missing dependency dnslib. Install it using `pip install dnslib`.")
    sys.exit(2)


class DomainName(str):
    """Helper class for flexible domain string handling."""
    def __getattr__(self, item):
        return DomainName(item + '.' + self)


D = DomainName(DOMAIN_NAME)

# DNS Records
soa_record = SOA(
    mname=D.ns1,  # Primary name server
    rname=D.admin,  # Admin email
    times=(
        2025010101,  # Serial number
        3600,        # Refresh
        10800,       # Retry
        86400,       # Expire
        3600,        # Minimum TTL
    )
)
ns_records = [NS(D.ns1), NS(D.ns2)]

# Predefined DNS records
records = {
    D: [A(IP_ADDRESS), AAAA((0,) * 16), MX(D.mail), soa_record] + ns_records,
    D.ns1: [A(IP_ADDRESS)],
    D.ns2: [A(IP_ADDRESS)],
    D.mail: [A(IP_ADDRESS)],
    D.admin: [CNAME(D)],
}


# ============================
# Helper Functions
# ============================
def forward_dns_query(data):
    """Forward the DNS query to the upstream server."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (FORWARDER, 53))
        response, _ = sock.recvfrom(512)
        return response
    except Exception as e:
        print(f"Failed to forward DNS query: {e}")
        return None


def dns_response(data):
    """Generate a DNS response for the incoming request."""
    try:
        request = DNSRecord.parse(data)
        reply = DNSRecord(
            DNSHeader(id=request.header.id, qr=1, aa=1, ra=1),
            q=request.q
        )

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        resolved = False

        # Check for records in the predefined list
        if qname == D or qname.endswith('.' + D):
            for name, rrs in records.items():
                if name == qname:
                    for rdata in rrs:
                        if qtype in ['*', rdata.__class__.__name__]:
                            reply.add_answer(
                                RR(rname=request.q.qname, rtype=getattr(QTYPE, rdata.__class__.__name__), 
                                   rclass=1, ttl=TTL, rdata=rdata))
                            resolved = True

            # Add authority and additional sections
            for rdata in ns_records:
                reply.add_ar(RR(rname=D, rtype=QTYPE.NS, rclass=1, ttl=TTL, rdata=rdata))
            reply.add_auth(RR(rname=D, rtype=QTYPE.SOA, rclass=1, ttl=TTL, rdata=soa_record))

        if not resolved:
            # Forward the query if no match is found
            print(f"Forwarding query for {qname}...")
            return forward_dns_query(data)

        print(f"Resolved query for {qname}:\n{reply}")
        return reply.pack()
    except Exception as e:
        print(f"Error processing DNS request: {e}")
        traceback.print_exc()
        return None


# ============================
# Request Handlers
# ============================
class BaseRequestHandler(socketserver.BaseRequestHandler):
    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        try:
            data = self.get_data()
            response = dns_response(data)
            if response:
                self.send_data(response)
            else:
                print("No response generated for the request.")
        except Exception:
            traceback.print_exc()


class TCPRequestHandler(BaseRequestHandler):
    def get_data(self):
        data = self.request.recv(8192).strip()
        size = struct.unpack('>H', data[:2])[0]
        return data[2:size + 2]

    def send_data(self, data):
        size = struct.pack('>H', len(data))
        self.request.sendall(size + data)


class UDPRequestHandler(BaseRequestHandler):
    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        self.request[1].sendto(data, self.client_address)


# ============================
# Main Function
# ============================
def main():
    parser = argparse.ArgumentParser(description='Python DNS Server')
    parser.add_argument('--port', default=5053, type=int, help='Port to listen on (default: 5053)')
    parser.add_argument('--tcp', action='store_true', help='Listen for TCP connections')
    parser.add_argument('--udp', action='store_true', help='Listen for UDP connections')

    args = parser.parse_args()
    if not (args.tcp or args.udp):
        parser.error("Please select at least one protocol: --tcp or --udp.")

    servers = []
    if args.udp:
        servers.append(socketserver.ThreadingUDPServer(('', args.port), UDPRequestHandler))
    if args.tcp:
        servers.append(socketserver.ThreadingTCPServer(('', args.port), TCPRequestHandler))

    for server in servers:
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        print(f"{server.RequestHandlerClass.__name__[:3]} server running on port {args.port} in thread: {thread.name}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        for server in servers:
            server.shutdown()


if __name__ == '__main__':
    main()
