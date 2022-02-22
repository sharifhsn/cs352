import socket
if __name__ == "__main__":
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f"socket open error: {err}")
        exit()
    
    port = 32702
    localhost_addr = socket.gethostbyname(socket.gethostname())

    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    with open("PROJ2-HNS.txt", "r") as f:
        hostnames = f.read().split()
    for hostname in hostnames:
        cs.send(hostname.encode())
        domain = cs.recv(4096)
        print(domain.decode("utf-8"))
    cs.close()
    exit()