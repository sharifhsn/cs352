import socket
import sys

if __name__ == "__main__":
    try:
        ts1s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f"socket open error: {err}")
        exit()
    
    port = int(sys.argv[1])
    rs_binding = ('', port)
    ts1s.bind(rs_binding)
    ts1s.listen(1)
    csockid, addr = ts1s.accept()

    with open("PROJ2-DNSTS1.txt", "r") as f:
        lines = f.read().strip().split("\n")
        maps = [line.split(" ") for line in lines]
    
    while True:
        data = csockid.recv(200).decode("utf-8")
        for m in maps:
            if m[0].casefold() == data.casefold():
                msg = " ".join(m) + " IN"
                csockid.send(msg.encode("utf-8"))