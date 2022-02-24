import socket
import sys

if __name__ == "__main__":
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f"socket open error: {err}")
        exit()
    
    port = int(sys.argv[2])
    localhost_addr = socket.gethostbyname(socket.gethostname())

    rs_binding = (socket.gethostbyname(sys.argv[1]), port)
    cs.connect(rs_binding)

    with open("PROJ2-HNS.txt", "r") as f:
        hostnames = f.read().strip().split("\n")
    with open("RESOLVED.txt", "w") as f:
        for hostname in hostnames:
            cs.send(hostname.encode())
            domain = cs.recv(200).decode("utf-8")
            f.write(domain)
            f.write("\n")

    cs.close()
    exit()