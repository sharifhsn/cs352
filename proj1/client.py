import socket
if __name__ == "__main__":
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print(f"socket open error: {err}")
        exit()
    
    # define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on the local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # send data to the server
    with open("in-proj.txt", "r") as f:
        lines = f.read().split("\n")
    for line in lines:
        cs.send(line.encode())
    
    # close the client socket
    cs.close()
    exit()