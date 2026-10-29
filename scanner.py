
"""
Port Scanner v3
A command-line TCP port scanner for authorized private lab targets.
"""

import argparse
import ipaddress
import socket
import time
from concurrent.futures import ThreadPoolExecutor


def parse_ports(value):
    """Validate a port range such as 1-1024."""
    try:
        parts = value.split("-")
        if len(parts) != 2:
            raise ValueError

        start, end = map(int, parts)

        if not (1 <= start <= end <= 65535):
            raise ValueError

        return start, end
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Use a valid port range such as 1-1024."
        )


def validate_target(value):
    """Allow RFC1918 private IPs, excluding loopback."""
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Enter a valid IPv4 or IPv6 address."
        )

    # This scanner uses IPv4 TCP sockets.
    if ip.version != 4:
        raise argparse.ArgumentTypeError(
            "This scanner currently supports IPv4 only."
        )

    private_networks = [
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
    ]

    if ip.is_loopback or not any(
        ip in network for network in private_networks
    ):
        raise argparse.ArgumentTypeError(
            "Refusing target: use an authorized private lab IP."
        )

    return str(ip)


def parse_arguments():
    """Read and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Scan TCP ports on an authorized private lab target."
    )

    parser.add_argument(
        "target",
        type=validate_target,
        help="IPv4 address of your private lab target",
    )
    parser.add_argument(
        "-p", "--ports",
        type=parse_ports,
        default=(1, 1024),
        metavar="START-END",
        help="Port range (default: 1-1024)",
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=1.0,
        help="Connection timeout in seconds (default: 1.0)",
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=100,
        help="Worker thread count (default: 100)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional file for saving scan results",
    )

    args = parser.parse_args()

    if not 0 < args.timeout <= 30:
        parser.error("--timeout must be greater than 0 and at most 30")

    if not 1 <= args.workers <= 200:
        parser.error("--workers must be between 1 and 200")

    return args


def grab_banner(host, port, timeout):
    """Try to read a banner from an open TCP service."""
    try:
        with socket.create_connection(
            (host, port), timeout=timeout
        ) as sock:
            sock.settimeout(timeout)

            if port in (80, 8080):
                request = (
                    f"HEAD / HTTP/1.0\r\n"
                    f"Host: {host}\r\n\r\n"
                )
                sock.sendall(request.encode())

            data = sock.recv(512)
            return data.decode(errors="ignore").strip()

    except OSError:
        return ""


def scan_port(host, port, timeout):
    """Check one TCP port and return its banner if open."""
    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))

        if result == 0:
            banner = grab_banner(host, port, timeout)
            return port, banner

    except OSError:
        pass

    return None


def save_results(filename, host, results, scanned, elapsed):
    """Save open ports and scan summary to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Target: {host}\n")
        file.write("Open ports:\n")

        for port, banner in results:
            description = banner or "No banner received"
            file.write(f"Port {port} open: {description}\n")

        file.write(f"\nPorts scanned: {scanned}\n")
        file.write(f"Open ports found: {len(results)}\n")
        file.write(f"Time taken: {elapsed:.2f} seconds\n")


def main():
    """Validate options, run the scan, and report results."""
    args = parse_arguments()
    host = args.target
    start_port, end_port = args.ports
    ports = range(start_port, end_port + 1)

    print("Starting threaded port scan...")
    print("Target:", host)
    print(f"Port range: {start_port}-{end_port}")

    start_time = time.perf_counter()
    results = []

    with ThreadPoolExecutor(
        max_workers=args.workers
    ) as pool:
        tasks = (
            pool.submit(scan_port, host, port, args.timeout)
            for port in ports
        )

        for task in tasks:
            result = task.result()
            if result is not None:
                results.append(result)

    results.sort(key=lambda item: item[0])
    elapsed = time.perf_counter() - start_time

    for port, banner in results:
        if banner:
            print(f"Port {port} open: {banner!r}")
        else:
            print(f"Port {port} open: No banner received")

    scanned = end_port - start_port + 1

    print("\n--- Scan Summary ---")
    print("Ports scanned:", scanned)
    print("Open ports found:", len(results))
    print(f"Time taken: {elapsed:.2f} seconds")

    if args.output:
        try:
            save_results(
                args.output, host, results, scanned, elapsed
            )
            print("Results saved to:", args.output)
        except OSError as error:
            print(f"Error saving results: {error}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
