import socket
if __name__ == "__main__":
    try:
        ss: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f"socket open error: {err}\n")
        exit()
    client_binding = ('', 32702)
    ss.bind(client_binding)
    ss.listen(1)
    csockid, addr = ss.accept()

    ts1_binding = ('', 32703)
    ss.bind(ts1_binding)
    ss.listen(1)
    ts1sockid, addr = ss.accept()

    # ts2_binding = ('', 32704)
    # ss.bind(ts2_binding)
    # ss.listen(1)
    # ts2sockid, addr = ss.accept()

    while data := csockid.recv(4096):
        csockid.send("random domain".encode())
    
    ss.close()
    exit()