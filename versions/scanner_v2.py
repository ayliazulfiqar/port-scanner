
import socket
import time
from concurrent.futures import ThreadPoolExecutor

host = "192.168.56.102"
ports = range(1, 1025)


def grab_banner(host, port):
    """Try to read a banner from an open TCP service."""
    try:
        with socket.create_connection((host, port), timeout=1) as s:
            s.settimeout(1)

            # Web servers may need a request before replying.
            if port in (80, 8080):
                request = (
                    f"HEAD / HTTP/1.0\r\n"
                    f"Host: {host}\r\n\r\n"
                )
                s.sendall(request.encode())

            data = s.recv(512)
            return data.decode(errors="ignore").strip()

    except (OSError, socket.timeout):
        return ""


def scan_port(port):
    """Check one port and return its result if open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))

        if result == 0:
            banner = grab_banner(host, port)
            return (port, banner)

    except OSError:
        pass

    return None


print("Starting threaded port scan...")
print("Target:", host)

start_time = time.perf_counter()
results = []

with ThreadPoolExecutor(max_workers=100) as pool:
    for result in pool.map(scan_port, ports):
        if result is not None:
            results.append(result)

# Sort the open ports so output is tidy.
results.sort(key=lambda item: item[0])

for port, banner in results:
    if banner:
        print(f"Port {port} open: {banner!r}")
    else:
        print(f"Port {port} open: No banner received")

elapsed = time.perf_counter() - start_time

print("Open ports found:", len(results))
print(f"Scan complete in {elapsed:.2f} seconds")

