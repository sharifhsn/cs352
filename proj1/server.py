import socket
if __name__ == "__main__":
    try:
        ss: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print(f"socket open error: {err}\n")
        exit()
    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host: str = socket.gethostname()
    print(f"[S]: Server host name is {host}")
    localhost_ip = (socket.gethostbyname(host))
    print(f"[S]: Server IP address is {localhost_ip}")
    csockid, addr = ss.accept()
    print(f"[S]: Got a connection request from a client at {addr}")

    with open("out-proj.txt", "a") as f:
        while data := csockid.recv(4096):
            f.write(f"{data.decode('utf-8')[::-1]}\n")
    
    # close the server socket
    ss.close()
    exit()