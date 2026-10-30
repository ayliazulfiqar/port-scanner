# Python Port Scanner

A lightweight, multithreaded Python TCP port scanner built to identify open ports, grab service banners, and compare scanning performance in an authorized lab environment.

## 1. Features

The project was developed in three versions, with each version introducing new functionality.

### Version 1 – Basic Port Scanner
- Scans a specified range of TCP ports.
- Uses Python's `socket` library to test port connectivity.
- Identifies open ports.
- Provides basic scan results.

### Version 2 – Multithreading
- Introduced multithreading to improve scanning speed.
- Scans multiple ports concurrently.
- Reduced scanning time compared with Version 1.
- Improved efficiency when scanning larger port ranges.

### Version 3 – Advanced Features
- Added command-line arguments using `argparse`.
- Added support for custom port ranges.
- Added banner grabbing to collect service information.
- Added a private IPv4 address validation check.
- Added optional output-file support.
- Improved scan summaries and error handling.

## 2. Usage

### Requirements

- Python 3
- Kali Linux or another Linux environment
- No external Python packages required.

### Clone the repository

```bash
git clone https://github.com/ayliazulfiqar/port-scanner.git
cd port-scanner
```

### Display help

```bash
python3 scanner.py --help
```

Example output:

```text
usage: scanner.py [-h] [-p PORTS] [-t THREADS] [--timeout TIMEOUT]
                  [-o OUTPUT] target

Python TCP Port Scanner

positional arguments:
  target                Private IPv4 address to scan

options:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Port range to scan
  -t THREADS, --threads THREADS
                        Number of worker threads
  --timeout TIMEOUT     Connection timeout in seconds
  -o OUTPUT, --output OUTPUT
                        Save results to a file
```

### Scan a port range

```bash
python3 scanner.py 192.168.56.102 -p 1-100
```

### Scan with custom thread count

```bash
python3 scanner.py 192.168.56.102 -p 1-1000 -t 100
```

### Save results to a file

```bash
python3 scanner.py 192.168.56.102 -p 1-100 -o results.txt
```

### Example scan output

```text
Starting scan on 192.168.56.102
Scanning ports 1-100...

Port 22 open: 'SSH-2.0-OpenSSH'
Port 80 open: 'HTTP/1.1 200 OK'

--- Scan Summary ---
Ports scanned: 100
Open ports found: 2
Time taken: [YOUR ACTUAL TIME] seconds
Results saved to: results.txt
```

## 3. How It Works

The scanner uses Python's built-in `socket` library to establish TCP connections with a target's ports.

### connect_ex()

The `connect_ex()` method attempts to establish a connection to a specified IP address and port. It returns `0` when the connection succeeds, which indicates that the port is open. A non-zero result indicates that the connection failed.

### Threading

Instead of checking every port one at a time, the scanner uses multiple threads to check several ports concurrently. This reduces the time required to scan a range of ports.

### Banner Grabbing

When an open port is discovered, the scanner attempts to receive information from the service running on that port. This information is called a banner and can sometimes reveal the service name or version.

Banner grabbing is optional in practice because not every service sends information automatically.

## 4. Safety

This project includes a private IPv4 address validation check to restrict scanning to private network addresses.

The scanner accepts addresses within these private IPv4 ranges:

- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

This restriction helps prevent accidental scanning of public IP addresses.

**Important:** This tool is intended only for my own lab environment and systems I am explicitly authorized to test. Never scan networks or devices without permission.

## 5. Results

### Comparison with Nmap

The custom Python scanner was tested against Nmap in the same lab environment.

| Comparison | Python Port Scanner | Nmap |
|---|---|---|
| Language | Python | C/C++ and other languages |
| TCP connect scanning | Yes | Yes |
| Multithreading | Yes | Advanced parallel scanning |
| Banner grabbing | Basic | More advanced service detection |
| UDP scanning | No | Yes |
| SYN scanning | No | Yes |
| Service detection | Basic banner grabbing | Advanced service detection |

Nmap is a mature and feature-rich network scanning tool. This project is not intended to replace Nmap. Its purpose is to demonstrate how port scanning works and how Python can be used to build a basic scanner.

### Version 1 vs Version 2 Performance

Version 1 scanned ports sequentially, while Version 2 introduced multithreading to scan multiple ports concurrently.

| Version | Scanning method | Scan time |
|---|---|---|
| V1 | Sequential | 0.74 seconds |
| V2 | Multithreaded | 1.29 seconds |

**Speed improvement:**

```text
Speed-up = V1 scan time / V2 scan time
```

For example, if V1 takes 20 seconds and V2 takes 5 seconds, V2 is 4 times faster.

Actual performance depends on network conditions, timeout settings, thread count, and target availability.

## 6. What I Learned

While building this project, I learned:

- How TCP connections work.
- How open ports can be identified using Python sockets.
- How `connect_ex()` can be used for connection testing.
- How multithreading improves scanning performance.
- How banner grabbing can reveal basic service information.
- How to use `argparse` to create command-line tools.
- How to validate private IPv4 addresses.
- How to handle errors and connection timeouts.
- How to use Git and GitHub to manage and publish a project.
- How to compare a custom security tool with an established tool like Nmap.

## 7. Limitations and Next Improvements

Although the scanner covers basic TCP port scanning, it has some limitations.

### Current limitations

- Supports TCP scanning only; no UDP scanning.
- Does not perform SYN scanning.
- Service detection is limited to basic banner grabbing.
- Some services do not return banners.
- Scan performance depends on network conditions and timeout settings.
- It does not provide the advanced detection capabilities of Nmap.

### Future improvements

- Add UDP port scanning.
- Add more advanced service detection.
- Add optional SYN scanning in an authorized lab.
- Improve banner grabbing and service identification.
- Add scan progress indicators.
- Improve result formatting and reporting.
- Add automated tests.

## 8. Link Back to My Journal

For the complete learning journey, development notes, troubleshooting, and project progress, visit my cybersecurity journal:

**([Cybersecurity Journal](../README.md))**

---

**Author:** Aylia Zulfiqar  
**Project:** Python Port Scanner 
**Repository:** https://github.com/ayliazulfiqar/port-scanner
