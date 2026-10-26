# port-scanner
A TCP port scanner built from scratch in Python to understand how tools like Nmap work; tested only against my own isolated lab.

This project is a port scanner written in Python using the socket module. I'm building it in three stages: a basic TCP connect scan, then a faster version with threading and banner grabbing, then a command-line tool with saved output and a safety check that refuses non-private IP addresses. The goal is to understand how a connect scan relates to the TCP handshake, and to compare my results against Nmap. All testing is done only on machines I own, inside an isolated lab.
## Goal
Build a simple scanner from scratch using Python's `socket` module, then improve it in stages. I want to understand how a connect scan relates to the TCP handshake, not just run a tool.

## Planned versions
| Version | Features | Status |
|---|---|---|
| v1 | Basic TCP connect scan over a port range, printing open ports | Planned |
| v2 | Threading for speed, plus banner grabbing | Planned |
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

## Progress log
- [Oct 27th'26]: Project planned. v1 starts next session.

Part of my [Cybersecurity Journal](../README.md).
