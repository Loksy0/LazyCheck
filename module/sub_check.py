import json
import requests
import platform
import sys
import msvcrt 
import select 

word_list_url_big = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/big.txt"
word_list_url_common = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/common.txt"

mega_pack = ["https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/big.txt", 
             "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/Proxy-Auto-Configuration-Files.txt", 
             "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/default-web-root-directory-linux.txt", 
             "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/URLs/urls-joomla-3.0.3.txt", 
             "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/URLs/urls-Drupal-7.20.txt",
             "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/api/api-endpoints.txt"]
small_pack = [
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/big.txt",   
    "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/default-web-root-directory-linux.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/URLs/urls-joomla-3.0.3.txt"]

def log(message, type):
    n = int(type)
    s = None
    if n == 1:
        s = "[+] "
    elif n == 2:
        s = "[-] "
    elif n == 3:
        s = "[!] "
    print(f"{s}{message}")

def user_pressed_ctrl_d():
    system_name = platform.system()

    if system_name == "Windows":
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x04':
                return True
    else:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            key = sys.stdin.read(1)
            if key == '\x04':
                return True
    return False

def check_subdomains(domain, l):
    log(f"Testing: {domain}", 1)
    lvl = int(l)

    def fetch_wordlist(urls):
        combined = []
        for url in urls:
            try:
                r = requests.get(url)
                r.raise_for_status()
                lines = r.text.splitlines()
                combined.extend(lines)
                log(f"Load {len(lines)} from {url}", 1)
            except requests.RequestException as e:
                log(f"Download error > {url}: {e}", 2)
        return list(dict.fromkeys(combined))

    if lvl == 1:
        word_list = fetch_wordlist([
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt",
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/big.txt"
        ])
    elif lvl == 2:
        word_list = fetch_wordlist(small_pack)
    elif lvl == 3:
        word_list = fetch_wordlist(mega_pack)

    valid_subdomains = []
    for word in word_list:
        if user_pressed_ctrl_d():
            log("User stopped further scanning (Ctrl+D).", 3)
            break
        subdomain = f"{domain}/{word}"
        try:
            response = requests.get(subdomain, timeout=3)
            if response.status_code == 200:
                log(f"[200] {subdomain}", 1)
                valid_subdomains.append(subdomain)
        except requests.RequestException:
            pass  

    return valid_subdomains
