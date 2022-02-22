import socket

if __name__ == "__main__":
    try:
        t1s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f"socket open error: {err}")
        exit()
    
    port = 32703
    localhost_addr = socket.gethostbyname(socket.gethostname())

    server_binding = (localhost_addr, port)
    t1s.connect(server_binding)

    with open("PROJ2-DNSTS1", "r") as f:
        lines = f.readlines()
        print(lines)