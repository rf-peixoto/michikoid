#!/usr/bin/python
print("Loading Michikoid...")
# ---------------------------- #
#       __         _     __    #
#      / /_Michi  (_)___/ /    #
#     / //_/ __ \/ / __  /     #
#    / ,< / /_/ / / /_/ /      #
#   /_/|_|\____/_/\__,_/       #
#               Repeater       #
# ---------------------------- #
#         Version: 1.5         #
# ---------------------------- #
import os
import sys
import socket
import urllib.parse
from time import sleep
from datetime import datetime
import colorama
from colorama import Fore, Back
# ------------------------------------------------- #
# Initialize Colorama:
# ------------------------------------------------- #
colorama.init()

# ------------------------------------------------- #
# Menu
# ------------------------------------------------- #
banner = Fore.BLUE + """\n       __         _     __
      / /_{0}Michi{1}  (_)___/ /
     / //_/ __ \/ / __  /
    / ,< / /_/ / / /_/ /
   /_/|_|\____/_/\__,_/
              {0}Repeater\n""".format(Fore.CYAN, Fore.BLUE) + Fore.RESET

def print_menu(clear=True):
    if clear:
        os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    print(Fore.BLUE + "[+]" + Fore.RESET + " Welcome, " + Fore.CYAN + "{0}".format(os.getenv("USER")) + Fore.RESET + ". Choose mode:" )
    print(Fore.BLUE + " 1." + Fore.RESET + " Build Request")
    print(Fore.BLUE + " 2." + Fore.RESET + " Import From File")
    print(Fore.BLUE + " 3." + Fore.RESET + " Quit Michikoid")

# ------------------------------------------------- #
# Get Date
# ------------------------------------------------- #
def get_date():
    time = datetime.now()
    return "{0}{1}{2}_{3}{4}".format(time.month, time.day, time.year, time.hour    , time.minute)

# ------------------------------------------------- #
# Make Request
# ------------------------------------------------- #
def make_request(host, port, request):
    # Prepare for output:
    responses = []
    # Set number of requests:
    print(Fore.BLUE + "[+]" + Fore.RESET + " Set the total number of requests")
    print(" * 0: Send continuously.")
    print(" * 1: Default")
    ammount = input(Fore.BLUE + ">>> " + Fore.RESET)
    if ammount == "":
        ammount = 1
    else:
        ammount = int(ammount)
    # Set delay time:
    print(Fore.BLUE + "[+]" + Fore.RESET +  " Set delay in seconds.")
    print(" * 0.5: Default")
    delay = input(Fore.BLUE + ">>> " + Fore.RESET)
    if delay == "":
        delay = 0.5
    else:
        delay = float(delay)

    # Print Request:
    print(Fore.BLUE + "\n[+]" + Fore.RESET +  "Your Request:")
    print(Fore.CYAN + request + Fore.RESET)
    try:
        if ammount > 0:
            for i in range(ammount):
                print(" - Now on request number " + Fore.CYAN + "{0}".format(i + 1) + Fore.RESET + ".")
                # Prepare socket:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect:
                s.connect((host, port))
                # Send:
                s.send(request.encode())
                # Save each responde:
                responses.append("Response: {0}\n".format(i + 1) + s.recv(8192)    .decode())
                s.close()
                sleep(delay)
        elif ammount == 0:
            print(Fore.RED + "Sending requests continuously." + Fore.RESET)
            counter = 1
            while True:
                # Prepare socket:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect:
                s.connect((host, port))
                # Send:
                s.send(request.encode())
                # Save each response:
                responses.append("Response: {0}\n".format(counter) + s.recv(8192)    .decode())
                counter += 1
                s.close()
                sleep(delay)
        # Output:
        output = "{0}_{1}.txt".format(host, get_date())
        with open(output, "w") as fl:
            for i in responses:
                fl.write(i)
        # Clean pool:
        responses.clear()
        print(Fore.BLUE + "[+]" + Fore.RESET + " Result exported on " + Fore.CYAN +  "{0}".format(output) + Fore.RESET + ".")
    except Exception as error:
        print(Fore.WHITE + Back.RED)
        print(error)
        print(Fore.RESET + Back.RESET)
        sys.exit()

# ------------------------------------------------- #
# Build Request
# ------------------------------------------------- #
def build_request():
    # Get Method:
    method = input(Fore.RESET + "Request Method: " + Fore.CYAN).upper()
    if method == "":
        method = "GET"
    # Get and Clean Target URL:
    host = input(Fore.RESET + "Target URL: " + Fore.CYAN).lower()
    for noise in ["http://", "https://"]:
        if host.startswith(noise):
            host = host.replace(noise, "")
    # Get Port:
    port = input(Fore.RESET + "Target Port: " + Fore.CYAN)
    if port == "":
        port = 80
    else:
        port = int(port)
    # Get User Agent:
    user_agent = input(Fore.RESET + "User-Agent: " + Fore.CYAN)
    if user_agent == "":
        user_agent = "Michikoid-Repeater"
    # Get Referer link:
    referer = input(Fore.RESET + "Referer link: " + Fore.CYAN).lower()
    if referer == "":
        referer = "no-referer-when-downgrade"
    # Get Cookie(s):
    cookie = input(Fore.RESET + "Cookie(s): " + Fore.CYAN)
    # Get Payload:
    payload = urllib.parse.quote_plus(input(Fore.RESET + "Payload: " + Fore.CYAN))
    print(Fore.RESET)
    content_length = len(payload)
    # Prepare Request:
    request = "{0} / HTTP/1.1\r\n".format(method)
    request += "Host: {0}\r\n".format(host)
    request += "User-Agent: {0}\r\n".format(user_agent)
    request += "Accept: text/html, application/xhtml+xml, application/xml;q=0.9    ,*/*;q=0.8\r\n"
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
# Import From File
# ------------------------------------------------- #
def import_from_file():
    # Find and Load file:
    filename = input(Fore.RESET + "Filename: " + Fore.CYAN)
    try:
        with open(filename, "r") as fl:
            request = fl.read()
        # Show request:
        print("\n{0}\n".format(request))
    except Exception as error:
        print(Fore.WHITE + Back.RED)
        print(error)
        print(Fore.RESET + Back.RESET)
        sys.exit()
    # Get and Clean Target URL:
    host = input(Fore.RESET + "Target URL: " + Fore.CYAN).lower()
    for noise in ["http://", "https://"]:
        if host.startswith(noise):
            host = host.replace(noise, "")
    # Get Port:
    port = input(Fore.RESET + "Target Port: " + Fore.CYAN)
    if port == "":
        port = 80
    else:
        port = int(port)
    print(Fore.RESET)
    # Send to Function:
    make_request(host, port, request)

# ------------------------------------------------- #
# Starting Point
# ------------------------------------------------- #
print_menu()
while True:
    option = input(Fore.BLUE + ">>> " + Fore.RESET)
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
        print(Fore.RED + " Invalid option!" + Fore.RESET)
