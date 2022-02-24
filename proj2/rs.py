import socket
import sys

if __name__ == "__main__":
    try:
        ts1s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f"socket open error: {err}\n")
        exit()
    port = int(sys.argv[3])
    rs_binding = (socket.gethostbyname(sys.argv[2]), port)
    ts1s.connect(rs_binding)
    ts1s.setblocking(False)
    ts1s.settimeout(5)

    try:
        ts2s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f"socket open error: {err}\n")
        exit()
    port = int(sys.argv[5])
    rs_binding = (socket.gethostbyname(sys.argv[4]), port)
    ts2s.connect(rs_binding)
    ts2s.setblocking(False)
    ts2s.settimeout(5)

    try:
        rss: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f"socket open error: {err}\n")
        exit()
    port = int(sys.argv[1])
    rs_binding = ("", port)
    rss.bind(rs_binding)
    rss.listen(5)
    csockid, addr = rss.accept()
    csockid.setblocking(False)
    csockid.settimeout(10)

    while True:
        try:
            host = csockid.recv(200).decode("utf-8")
        except socket.timeout:
            break

        try:
            ts1s.send(host.encode())
            domain = ts1s.recv(200).decode("utf-8")
        except socket.timeout:
            try:
                ts2s.send(host.encode())
                domain = ts2s.recv(200).decode("utf-8")
            except socket.timeout:
                csockid.send(f"{host} - TIMED OUT".encode())
                continue

        csockid.send(domain.encode("utf-8"))

    ts1s.close()
    ts2s.close()
    rss.close()
    exit()