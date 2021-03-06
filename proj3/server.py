import socket
import signal
import sys
import random

def dict_creation(src, dict_sep, pair_sep):
    return dict([tuple(s.split(pair_sep)) for s in src.split(dict_sep)])

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print("Here is the " + tag)
    print("\"\"\"")
    print("Here is the " + value)
    print("\"\"\"")
    print()

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
# Read secret data of all the users

# login credentials are stored as a dictionary {username: password}
with open("passwords.txt", "r") as f:
    credentials = dict_creation(f.read().strip(), "\n", " ")

# secret data is stored as a dictionary {username: secret}
with open("secrets.txt", "r") as f:
    secrets = dict_creation(f.read().strip(), "\n", " ")

cookies = {}

### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024).decode("utf-8")

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)

    # TODO: Put your application logic here!
    # Parse headers and body and perform various actions
    fields = {} if body == '' else dict_creation(body, "&", "=")
    # print(headers.split("\r\n")[1].split(": "))
    headers_dict = dict_creation("\n".join(headers.split("\r\n")[1:]), "\n", ": ")
    print(headers_dict)
    # You need to set the variables:
    # (1) `html_content_to_send` => add the HTML content you'd
    # like to send to the client.
    # Right now, we just send the default login page.
    
    if "action" in fields.keys() and fields["action"] == "logout":
        print("logging out")
        # Case F. Logout
        html_content_to_send = logout_page
        headers_to_send = "Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n"
    elif "Cookie" in headers_dict.keys():
        print("cookie found")
        if headers_dict["Cookie"] in cookies.keys():
            print("cookie good")
            # Case C. Cookie validated
            html_content_to_send = success_page + cookies[headers_dict["Cookie"]]
        else:
            print("cookie bad")
            # Case D. Cookie invalid
            html_content_to_send = bad_creds_page
        headers_to_send = ""
    elif "username" in fields.keys() and "password" in fields.keys():
        print("username/password provided")
        # username and password were both sent as part of the headers
        if fields["username"] in credentials.keys() and credentials[fields["username"]] == fields["password"]:
            print("successful login!")
            # Case A. Username-password auth success
            html_content_to_send = success_page + secrets[fields["username"]]
            cookie = random.getrandbits(64)
            headers_to_send = "Set-Cookie: token=" + str(cookie) + "\r\n"
            if cookie not in cookies.keys():
                cookies.update({"token=" + str(cookie):secrets[fields["username"]]})
        else:
            print("username/password is bad")
            # Case B. Username-password auth failure
            html_content_to_send = bad_creds_page
            headers_to_send = ""
    elif ("username" in fields.keys()) != ("password" in fields.keys()):
        print("you included only one of username/password")
        # Case B. Either one of username/password fields missing
        html_content_to_send = bad_creds_page
        headers_to_send = ""
    else:
        # basic case
        print("just login normally")
        html_content_to_send = login_page
        headers_to_send = ""
    # But other possibilities exist, including
    # html_content_to_send = success_page + <secret>
    # html_content_to_send = bad_creds_page
    # html_content_to_send = logout_page
    
    # (2) `headers_to_send` => add any additional headers
    # you'd like to send the client?
    # Right now, we don't send any extra headers.

    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response.encode())
    client.close()
    
    print("Served one request/connection!\n")

# We will never actually get here.
# Close the listening socket
sock.close()
