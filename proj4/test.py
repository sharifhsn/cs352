from subprocess import Popen, DEVNULL
from time import time
from filecmp import cmp

def check(pkt, ack, infile):
    print(f"checking options {pkt} {ack} {infile}")
    p = Popen(["python3", "receiver.py", "--pktloss"] + pkt + ["--ackloss"] + ack, stdout=DEVNULL)
    q = Popen(["python3", "sender.py", "--infile"] + infile, stdout=DEVNULL)
    while p.poll() == None or q.poll == None:
        pass
    assert(cmp(infile[0], "test-output.txt"))

# 1. no packet loss, no ACK loss
check(["noloss"], ["noloss"], ["test-input.txt"])

# 2. packet loss everyn with N = 3, no ACK loss
check(["everyn", "--pktlossN", "3"], ["noloss"], ["test-input.txt"])

# 3. packet loss everyn with N = 10, no ACK loss
check(["everyn", "--pktlossN", "10"], ["noloss"], ["test-input.txt"])

# 4. no packet loss, ACK loss everyn with N = 3
check(["noloss"], ["everyn", "--acklossN", "3"], ["test-input.txt"])

# 5. no packet loss, ACK loss everyn with N = 10
check(["noloss"], ["everyn", "--acklossN", "10"], ["test-input.txt"])

# 6. packet loss alteveryn with N = 8, no ACK loss
check(["alteveryn", "--pktlossN", "8"], ["noloss"], ["test-input.txt"])

# 7. no packet loss, ACK loss alteveryn with N = 8
check(["noloss"], ["alteveryn", "--acklossN", "8"], ["test-input.txt"])

# 8. packet loss iid with N = 5, no ACK loss
check(["iid", "--pktlossN", "5"], ["noloss"], ["test-input.txt"])

# 9. no packet loss, ACK loss iid with N = 5
check(["noloss"], ["iid", "--acklossN", "5"], ["test-input.txt"])

# 10. packet loss everyn with N = 3, ACK loss alteveryn with N = 4
check(["everyn", "--pktlossN", "3"], ["alteveryn", "--acklossN", "4"], ["test-input.txt"])

# 11. start the sender first, give a few seconds, then start the receiver
print("checking sender before receiver")
Popen(["python3", "sender.py", "--infile", "test-input.txt"], stdout=DEVNULL)
t = time()
while time() - t < 5:
    pass
Popen(["python3", "receiver.py", "--pktloss", "noloss", "--ackloss", "noloss"], stdout=DEVNULL)
assert(cmp("test-input.txt", "test-output.txt"))

# with medium-input.txt
# uncomment this section to test medium-input.txt (will take a while)

check(["noloss"], ["noloss"], ["medium-input.txt"])
check(["everyn", "--pktlossN", "3"], ["noloss"], ["medium-input.txt"])
check(["everyn", "--pktlossN", "10"], ["noloss"], ["medium-input.txt"])
check(["noloss"], ["everyn", "--acklossN", "3"], ["medium-input.txt"])
check(["noloss"], ["everyn", "--acklossN", "10"], ["medium-input.txt"])
check(["alteveryn", "--pktlossN", "8"], ["noloss"], ["medium-input.txt"])
check(["noloss"], ["alteveryn", "--acklossN", "8"], ["medium-input.txt"])
check(["iid", "--pktlossN", "5"], ["noloss"], ["medium-input.txt"])
check(["noloss"], ["iid", "--acklossN", "5"], ["medium-input.txt"])
check(["everyn", "--pktlossN", "3"], ["alteveryn", "--acklossN", "4"], ["medium-input.txt"])
print("checking sender before receiver")
Popen(["python3", "sender.py", "--infile", "medium-input.txt"], stdout=DEVNULL)
t = time()
while time() - t < 5:
    pass
Popen(["python3", "receiver.py", "--pktloss", "noloss", "--ackloss", "noloss"], stdout=DEVNULL)
assert(cmp("medium-input.txt", "test-output.txt"))

# with long-input.txt
# uncomment this section to test long-input.txt (will take a LONG while)

check(["noloss"], ["noloss"], ["long-input.txt"])
check(["everyn", "--pktlossN", "3"], ["noloss"], ["long-input.txt"])
check(["everyn", "--pktlossN", "10"], ["noloss"], ["long-input.txt"])
check(["noloss"], ["everyn", "--acklossN", "3"], ["long-input.txt"])
check(["noloss"], ["everyn", "--acklossN", "10"], ["long-input.txt"])
check(["alteveryn", "--pktlossN", "8"], ["noloss"], ["long-input.txt"])
check(["noloss"], ["alteveryn", "--acklossN", "8"], ["long-input.txt"])
check(["iid", "--pktlossN", "5"], ["noloss"], ["long-input.txt"])
check(["noloss"], ["iid", "--acklossN", "5"], ["long-input.txt"])
check(["everyn", "--pktlossN", "3"], ["alteveryn", "--acklossN", "4"], ["long-input.txt"])
print("checking sender before receiver")
Popen(["python3", "sender.py", "--infile", "long-input.txt"], stdout=DEVNULL)
t = time()
while time() - t < 5:
    pass
Popen(["python3", "receiver.py", "--pktloss", "noloss", "--ackloss", "noloss"], stdout=DEVNULL)
assert(cmp("long-input.txt", "test-output.txt"))
