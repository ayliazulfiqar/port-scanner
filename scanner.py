### Scanner Code

The scanner is implemented in `port-scanner/scanner.py`.

```python
import socket

host = "192.168.56.102"

print("Starting port scan...")
print("Target:", host)

for port in range(1, 1025):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((host, port))

        if result == 0:
            print("Port", port, "is open")

print("Scan complete!")
```
