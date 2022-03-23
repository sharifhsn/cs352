from asyncio import subprocess
import sys
from subprocess import run, Popen, DEVNULL
import signal
from time import sleep

port = "8080"
if len(sys.argv) > 1:
    port = sys.argv[1]

addr = f"http://localhost:{port}"

cookie_file = "cookies.txt"

user_good = "bezos"
pass_good = "amazon"
user_bad = "some"
pass_bad = "none"

# run server.py
server = Popen(["python", "server.py", port], stdout=DEVNULL)

# curl commands

# basic: no username or password posted, no cookies (login)
run(["curl", addr])

# correct username and password posted, no cookies (success)
run(["curl", "-d", f"username={user_good}&password={pass_good}", "-c", "cookies.txt", "-b", "cookies.txt", addr])

# non-existent username posted with password, no cookies (bad credentials)
run(["curl", "-d", f"username={user_bad}&password={pass_bad}", addr])

# existing username posted with bad password, no cookies (bad credentials)
run(["curl", "-d", f"username={user_good}&password={pass_bad}", addr])

# exactly one of username or password posted, other field missing, no cookies (bad credentials)
run(["curl", "-d", f"username={user_good}", addr])

# no username or password posted, valid cookie (success)
run(["curl", "-c", cookie_file, "-b", cookie_file, addr])

# non-existent username or bad password for existing username, valid cookie (success)
run(["curl", "-d", f"username={user_bad}&password={pass_bad}", "-c", cookie_file, "-b", cookie_file, addr])

# correct username and password, valid cookie (success)
run(["curl", "-d", f"username={user_good}&password={pass_good}", "-c", cookie_file, "-b", cookie_file, addr])

# correct username and password, invalid cookie (bad credentials)
server.send_signal(signal.SIGINT)
sleep(5)
server = Popen(["python", "server.py", port], stdout=DEVNULL)
run(["curl", "-d", f"username{user_good}&password={pass_good}", "-c", cookie_file, "-b", cookie_file, addr])

# logout posted, valid cookie (logout)
run(["curl", "-d", f"username={user_good}&password={pass_good}", "-c", cookie_file, "-b", cookie_file, addr], stdout=DEVNULL) # regenerate cookie
run(["curl", "-d", "action=logout", "-c", cookie_file, "-b", cookie_file, addr])

# logout posted, invalid cookie (logout)
run(["curl", "-d", f"username={user_good}&password={pass_good}", "-c", cookie_file, "-b", cookie_file, addr], stdout=DEVNULL) # regenerate cookie
server.send_signal(signal.SIGINT)
sleep(5)
server = Popen(["python", "server.py", port], stdout=DEVNULL)
run(["curl", "-d", "action=logout", "-c", cookie_file, "-b", cookie_file, addr])
