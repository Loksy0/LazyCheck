import requests
import json
import socket

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

DNS_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "CNAME", "SOA", "SRV", "CAA"]

def get_ip_info(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=66846719") 
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def reverse_dns(ip):
    ip_reversed = ".".join(reversed(ip.split("."))) + ".in-addr.arpa"
    url = f"https://dns.google/resolve?name={ip_reversed}&type=PTR"
    r = requests.get(url).json()
    if "Answer" in r:
        return r["Answer"][0]["data"].rstrip(".")
    return None

def get_dns_records(domain):
    results = {}
    for rtype in DNS_TYPES:
        url = f"https://dns.google/resolve?name={domain}&type={rtype}"
        r = requests.get(url).json()
        if "Answer" in r:
            results[rtype] = [ans["data"] for ans in r["Answer"]]
    return results

def reverse_ip_lookup(ip, api_key):
    if not api_key or api_key == "your_api_key_here" or api_key == "":
        log("API key is missing.", 3)
        return ["API key is missing."]
    
    url = f"https://api.viewdns.info/reverseip/?host={ip}&apikey={api_key}&output=json"
    try:
        r = requests.get(url).text
        if "error" not in r.lower():
            return r.strip().split("\n")
        return []
    except:
        return []

def full_ip_report(ip, api_key):
    report = {}
    
    report["ip_info"] = get_ip_info(ip)
    ptr = reverse_dns(ip)
    report["reverse_dns"] = ptr

    if ptr:
        report["dns_records"] = get_dns_records(ptr)
    else:
        report["dns_records"] = {}
    
    report["hosted_domains"] = reverse_ip_lookup(ip, api_key)
    
    return report

def ping(ip):
    time_out_s = 2
    online = False
    try:
        socket.setdefaulttimeout(time_out_s)
        host = socket.gethostbyaddr(ip)
        if host:
            online = True
    except Exception:
        online = False
    return online