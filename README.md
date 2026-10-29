# port-scanner
A TCP port scanner built from scratch in Python to understand how tools like Nmap work; tested only against my own isolated lab.

This project is a port scanner written in Python using the socket module. I'm building it in three stages: a basic TCP connect scan, then a faster version with threading and banner grabbing, then a command-line tool with saved output and a safety check that refuses non-private IP addresses. The goal is to understand how a connect scan relates to the TCP handshake, and to compare my results against Nmap. All testing is done only on machines I own, inside an isolated lab.
## Goal
Build a simple scanner from scratch using Python's `socket` module, then improve it in stages. I want to understand how a connect scan relates to the TCP handshake, not just run a tool.

## Planned versions
| Version | Features | Status |
|---|---|---|
| v1 | Basic TCP connect scan over a port range, printing open ports | Done |
| v2 | Threading for speed, plus banner grabbing | Done |
| v3 | Command-line options (`argparse`), saved output, and a safety check | Planned |

## Rules
- **I only scan machines I own, inside my isolated lab** (Metasploitable on the host-only network).
- In v3, the scanner will refuse targets outside private IP ranges.
- I compare my results with `nmap -sT` to check they match.

## Python refresher
- `socket` module: creating a TCP socket
- `connect_ex()`: returns 0 when a port is open
- Timeouts with `settimeout()`
- Loops and `range()` for port ranges
- `try` / `except` for error handling
- `threading` or `concurrent.futures` (v2)
- `argparse` for command-line options (v3)
- `ipaddress` module for the safety check (v3)

## v1 Results

**What it does:** Scans TCP ports 1–1024 on my Metasploitable lab target using Python's `socket` module and `connect_ex()`. It prints the ports where TCP connections succeed.

**How it works:** The script loops through each port, attempts a TCP connection, and checks the result. A return value of `0` means the TCP connection succeeded. The script uses a one-second timeout for each attempt.

**Test environment:** Kali Linux and Metasploitable in my lab.

**Test results:**

| Test | Result |
|---|---|
| Individual test of port 80 | `0` — connection succeeded |
| Individual test of port 9999 | `111` — connection refused |
| Full scan of ports 1–1024 | Completed and displayed open ports |

**Nmap comparison:** I compared my scanner with `nmap -sT -p 1-1024 <target-ip>`.

| Tool | Open ports found |
|---|---|
| My Python scanner | 21, 22, 23, 25, 53, 80, 111, 139, 445, 512, 513, 514 |
| Nmap | 21, 22, 23, 25, 53, 80, 111, 139, 445, 512, 513, 514] |

**Result:** The Python scanner and Nmap results matched. Both tools identified the same 12 open TCP ports: 21, 22, 23, 25, 53, 80, 111, 139, 445, 512, 513, and 514. No differences were observed in this scan.

**Problems I hit:**
- Learning how to create and use TCP sockets in Python.
- Understanding the return value of `connect_ex()`.
- Building a loop to test multiple ports automatically.

**What I learned:**

I learned how to create TCP sockets, test connections with `connect_ex()`, and use a `for` loop to scan multiple ports. I also learned that a successful connection returns `0`, while a failed connection does not necessarily prove that a port is closed.

**Status:** v1 implemented and tested in my lab.

## v2 Results

- **Target:** `192.168.56.102`
- **Port range:** TCP 1–1024

| Measurement | v1 | v2 |
|---|---|---|
| Scan time | 0.74 seconds	 | 1.29 seconds |

**Banner examples:**
- **Port 21 (FTP):** `220 (vsFTPd 2.3.4)`
- **Port 22 (SSH):** `SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1`

### What I Learned

- Multithreading makes port scanning faster by checking multiple ports concurrently.
- Banner grabbing helps identify services running on open ports.
- Sorting results makes scan output easier to read.
- Comparing results with Nmap helps validate accuracy.

## Progress log
- [Oct 26th'26]: Project planned. v1 starts next session.
- [Oct 27th'26]: v1 Done. v2 starts next session.
- [Oct 28th'26]: v2 Done. v3 starts next session.
   
Part of my [Cybersecurity Journal](../README.md).
