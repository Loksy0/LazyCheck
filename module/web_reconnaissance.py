import requests
from urllib.parse import urljoin
import platform
import sys
import msvcrt
import select

requests.packages.urllib3.disable_warnings()

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

def web_app_recon(domain, lvl):
    findings = {}

    try:
        r = requests.get(urljoin(domain, "robots.txt"), verify=False, timeout=5)
        if r.status_code == 200:
            findings["robots.txt"] = r.text.strip()
    except:
        pass

    try:
        r = requests.get(urljoin(domain, "sitemap.xml"), verify=False, timeout=5)
        if r.status_code == 200:
            findings["sitemap.xml"] = r.text.strip()
    except:
        pass

    wordlists = {
        1: "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-small-files.txt",
        2: "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-medium-files.txt",
        3: "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-large-files.txt"
    }

    common_paths = []
    try:
        wl_resp = requests.get(wordlists[lvl], timeout=10)
        wl_resp.raise_for_status()
        common_paths = wl_resp.text.splitlines()
    except Exception as e:
        findings["error"] = f"Failed to load wordlist: {e}"
        return findings

    found_paths = []
    for path in common_paths:
        if user_pressed_ctrl_d():
            log("User stopped further scanning (Ctrl+D).", 2)
            break
        try:
            url = urljoin(domain, path)
            r = requests.get(url, verify=False, timeout=5, allow_redirects=False)
            if r.status_code in (200, 301, 302, 403):
                found_paths.append({"url": url, "status": r.status_code})
        except:
            pass

    if found_paths:
        findings["interesting_paths"] = found_paths

    return findings
