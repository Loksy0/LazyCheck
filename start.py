import module
import json
import argparse
import os
import requests
import platform
from datetime import datetime

__version__ = "1.0 Release"
__date__ = "12.08.2025"
__author__ = "Loksy0"

def log(message, type):
    prefixes = {1: "[+]", 2: "[-]", 3: "[!]"}
    print(f"{prefixes.get(type, '[?]')} {message}")

with open("config.json", "r") as f:
    config = json.load(f)
viewdns_api_key = config.get("viewdns.info_api_key")
leaks_api_key = config.get("leak-lookup.com_api_key")

parser = argparse.ArgumentParser(description="Lazy Check")
parser.add_argument("ip", help="IP address to scan")
parser.add_argument("lvl", choices=["1", "2", "3"], help="Lvl 1 > Less time, less specific.\nLvl 2 > Balanced.\nLvl 3 > Very detailed, may take hours.")
args = parser.parse_args()

ip = args.ip
lvl = int(args.lvl)

results_dir = os.path.join("results", ip)
os.makedirs(results_dir, exist_ok=True)

log("Starting getting IP and DNS info..", 1)
ip_results = module.full_ip_report(ip, viewdns_api_key)
with open(os.path.join(results_dir, "ip.txt"), "w", encoding="utf-8") as f:
    f.write(json.dumps(ip_results, indent=2))

log("Scanning ports..", 1)
port_results = module.scan_target(ip)
with open(os.path.join(results_dir, "port.txt"), "w", encoding="utf-8") as f:
    f.write(json.dumps(port_results, indent=2))

log("Getting domains..", 1)
hosted_domains_str = ip_results["hosted_domains"][0]
hosted_domains_json = json.loads(hosted_domains_str)
domains_list = hosted_domains_json["response"]["domains"]
all_domains = [d["name"] for d in domains_list]

log("Searching for online domains..", 1)
online_domains = []
for domain in all_domains:
    try:
        if module.ping(domain):
            online_domains.append(domain)
    except Exception as e:
        log(f"Error while checking {domain}: {e}", 3)

with open(os.path.join(results_dir, "domains.txt"), "w", encoding="utf-8") as f:
    f.write("-=-=-=-=-=-=-=-=-= All found domains: =-=-=-=-=-=-=-=-=-\n" + "\n".join(all_domains) + "\n\n")
    f.write("-=-=-=-=-=-=-=-=-= Online domains: =-=-=-=-=-=-=-=-=-\n" + "\n".join(online_domains) + "\n")
log("Checking web server..", 1)
port_443 = next((p for p in port_results["ports"] if p["port"] == 443), None)
port_80 = next((p for p in port_results["ports"] if p["port"] == 80), None)

is_https_open = (port_443 and port_443.get("status") == "open")
is_http_open = (port_80 and port_80.get("status") == "open")
web_server = is_https_open or is_http_open

http_prefix = ""
if web_server:
    log("Web server detected!", 1)
    http_prefix = "https://" if is_https_open else "http://"
else:
    log("Web server is not detected.. skipping subdomain search..", 2)

log(f"We find: {len(online_domains)} online domain(s)..", 1)
for o in online_domains:
    log(f"Domain: {o if o.startswith(('http://', 'https://')) else http_prefix + o}", 1)

sub_domains = []
if web_server:
    if len(online_domains) == 1:
        domain = online_domains[0]
        if not domain.startswith(("http://", "https://")):
            domain = http_prefix + domain
        log(f"Only one domain found: {domain} — scanning subdomains automatically..", 1)
        sub_domains = module.check_subdomains(domain, lvl)
    elif len(online_domains) >= 2:
        log("There is more than 2 domains..", 1)
        choice = input("[!] Do you know target domain? (y/n) > ").lower().strip()
        if choice == "y":
            domain = input("[!] Enter target domain > ").strip()
            if not domain.startswith(("http://", "https://")):
                domain = http_prefix + domain
            sub_domains = module.check_subdomains(domain, lvl)
        elif choice == "n":
            w = input("[!] Do you want to scan all domains from list? (y/n) > ").lower().strip()
            if w == "y":
                for domain in online_domains:
                    if not domain.startswith(("http://", "https://")):
                        domain = http_prefix + domain
                    sub_domains.extend(module.check_subdomains(domain, lvl))
            else:
                log("Skipping..", 2)
        else:
            log("Invalid choice — skipping search for subdomains..", 2)

if sub_domains:
    with open(os.path.join(results_dir, "sub.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sub_domains))

if web_server:
    results = module.cms_admin_check(domain)
    cms_file = os.path.join(results_dir, "cms.txt")

    if results:
        with open(cms_file, "w", encoding="utf-8") as f:
            for item in results:
                line = f"{item['type']} version {item['version'] or 'unknown'}"
                log(f"Detected: {line}", 1)
                f.write(line + "\n")
    else:
        log("No CMS/Admin panel detected.", 2)
        with open(cms_file, "w", encoding="utf-8") as f:
            f.write("No CMS/Admin panel detected.\n")

if web_server:
    log("Collecting SSL/TLS certificate info..", 1)
    cert_info = module.ssl_info(ip)
    with open(os.path.join(results_dir, "ssl.txt"), "w", encoding="utf-8") as f:
        f.write(json.dumps(cert_info, indent=2))

if web_server:
    log("Starting web reconnaissance..", 1)
    web_enum = module.web_app_recon(domain, lvl)

    with open(os.path.join(results_dir, "web_enum.txt"), "w", encoding="utf-8") as f:
        if "robots.txt" in web_enum:
            f.write("[robots.txt]\n" + web_enum["robots.txt"] + "\n\n")
        if "sitemap.xml" in web_enum:
            f.write("[sitemap.xml]\n" + web_enum["sitemap.xml"] + "\n\n")
        if "interesting_paths" in web_enum:
            f.write("[Interesting Paths]\n")
            for p in web_enum["interesting_paths"]:
                log(f"Found: {p['url']} (status {p['status']})", 1)
                f.write(f"{p['url']} (status {p['status']})\n")
        if "error" in web_enum:
            log(web_enum["error"], 3)

log("Checking public leaks via Leak-Lookup..", 1)
leaks = module.leaks_check(domain.replace("https://", "").replace("http://", ""), leaks_api_key)

leaks_file = os.path.join(results_dir, "leaks.txt")
with open(leaks_file, "w", encoding="utf-8") as f:
    if isinstance(leaks, dict) and leaks.get("error"):
        log(f"Error: {leaks['error']}", 3)
        f.write(f"Error: {leaks['error']}\n")
    elif leaks:
        for item in leaks:
            line = f"Breach: {item['breach']}"
            if item["details"]:
                line += f" – details: {item['details']}"
            log(line, 1)
            f.write(line + "\n")
    else:
        log("No breaches found.", 2)
        f.write("No breaches found.\n")
        
log("All data saved in structured format.", 1)