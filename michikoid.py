#!/usr/bin/python
# ------------------------------------------------- #
# Version 1.0.0
# ------------------------------------------------- #
# Import libraries:
import os
import sys
import socket
import urllib.parse
from time import sleep
# ------------------------------------------------- #
#  Banner                                           #
# ------------------------------------------------- #
banner = """\n       __         _     __
      / /_Michi  (_)___/ /
     / //_/ __ \/ / __  /
    / ,< / /_/ / / /_/ /
   /_/|_|\____/_/\__,_/
              Repeater\n"""

def print_menu(clear=True):
    if clear:
        os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    print("[*] Welcome, {0}. Choose mode:".format(os.getenv("USER")))
    print(" 1. Build Request")
    print(" 2. Import From File")
    print(" 3. Quit Michikoid")

# ------------------------------------------------- #
#  Make Request                                     #
# ------------------------------------------------- #
def make_request(host, port, request):
    # Set number of requests:
    print("\n")
    print("[+] Set the total number of requests")
    print(" * 0: Send continuously.")
    print(" * 1: Default")
    ammount = input(">>> ")
    if ammount == "":
        ammount = 1
    else:
        ammount = int(ammount)
    # Set delay time:
    print("[+] Set delay in seconds.")
    print(" * 0.5: Default")
    delay = input(">>> ")
    if delay == "":
        delay = 0.5
    else:
        delay = float(delay)

    # Print Request:
    print("\n")
    print("[+] Your Request:")
    print(request)
    print("\n")
    try:
        if ammount > 0:
            for i in range(ammount):
                # Prepare socket:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect:
                s.connect((host, port))
                # Send:
                s.send(request.encode())
                # Print each responde:
                print("Response: {0}".format(i + 1))
                print(s.recv(8192).decode())
                s.close()
                sleep(delay)
        elif ammount == 0:
            print("\nSending requests continuously.")
            counter = 1
            while True:
                # Prepare socket:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect:
                s.connect((host, port))
                # Send:
                s.send(request.encode())
                # Print each responde:
                print("Response: {0}".format(counter))
                print(s.recv(8192).decode())
                counter += 1
                s.close()
                sleep(delay)
        print("\n[+] Done!")
    except Exception as error:
        print(error)
        sys.exit()

# ------------------------------------------------- #
#  Build Request                                    #
# ------------------------------------------------- #
def build_request():
    # Get Method:
    method = input("Request Method: ").upper()
    if method == "":
        method = "GET"
    # Get and Clean Target URL:
    host = input("Target URL: ").lower()
    for noise in ["http://", "https://"]:
        if host.startswith(noise):
            host = host.replace(noise, "")
    # Get Port:
    port = int(input("Target Port: "))
    # Get User Agent:
    user_agent = input("User-Agent: ")
    if user_agent == "":
        user_agent = "Michikoid-Repeater"
    # Get Referer link:
    referer = input("Referer link: ").lower()
    if referer == "":
        referer = "no-referer-when-downgrade"
    # Get Cookie(s):
    cookie = input("Cookie(s): ")
    # Get Payload:
    payload = urllib.parse.quote_plus(input("Payload: "))
    content_length = len(payload)
    # Prepare Request:
    request = "{0} / HTTP/1.0\r\n".format(method)
    request += "Host: {0}\r\n".format(host)
    request += "User-Agent: {0}\r\n".format(user_agent)
    request += "Accept: text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8\r\n"
    request += "Accept-Encoding: gzip, deflate\r\n"
    request += "Cache-Control: no-cache\r\n"
    request += "Pragma: no-cache\r\n"
    request += "Referer: {0}\r\n".format(referer)
    request += "Content-Length: {0}\r\n".format(content_length)
    request += "DNT: 1\r\n"
    request += "Connection: close\r\n"
    request += "Cookie: {0}\r\n".format(cookie)
    request += "\r\n{0}".format(payload)
    # Send to Function:
    make_request(host, port, request)

# ------------------------------------------------- #
#  Import From File                                 #
# ------------------------------------------------- #
def import_from_file():
    # Find and Load file:
    filename = input("Filename: ")
    try:
        with open(filename, "r") as fl:
            request = fl.read()
        # Show request:
        print("\n{0}\n".format(request))
    except Exception as error:
        print(error)
        sys.exit()
    # Get and Clean Target URL:
    host = input("Target URL: ").lower()
    for noise in ["http://", "https://"]:
        if host.startswith(noise):
            host = host.replace(noise, "")
    # Get Port:
    port = int(input("Target Port: "))
    # Send to Function:
    make_request(host, port, request)

# ------------------------------------------------- #
#  Start                                            #
# ------------------------------------------------- #
print_menu()
while True:
    option = input(">>> ")
    if option == "1":
        build_request()
        print_menu(clear=False)
    elif option == "2":
        import_from_file()
        print_menu(clear=False)
    elif option == "3":
        print(" Thank you and goodbye.")
        sys.exit()
    else:
        print_menu()
        print(" Invalid option!")
