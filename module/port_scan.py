import subprocess
import json

def log(message, type):
    n = int(type)
    s = None
    if n == 1:
        s = "[+] "
    elif n == 2:
        s = "[-] "
    elif n == 3:
        s = "[!] "

    log(f"{s}{message}", 3)

def scan_target(target):
    args = ['nmap', '-p-', '-sS', '-sV', '-O', '-T4', target]

    result = {
        "target": target,
        "ports": [],
        "system": None
    }

    try:
        proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.stdout.decode('utf-8', errors='ignore')
        err = proc.stderr.decode('utf-8', errors='ignore')

        if err:
            print(f"nmap stderr:\n{err}")

        lines = out.splitlines()

        for line in lines:
            if 'OS details:' in line:
                os_name = line.split('OS details:')[1].strip()
                result["system"] = os_name
                break

        port_section = False
        for line in lines:
            line = line.strip()
            if line.startswith('PORT'):
                port_section = True
                continue
            if port_section:
                if line == '' or line.startswith('Nmap done:'):
                    break
                if line.startswith('|'):
                    continue

                parts = line.split()
                if len(parts) >= 3:
                    port_proto = parts[0]
                    status = parts[1].lower()  
                    service = parts[2]
                    version = " ".join(parts[3:]) if len(parts) > 3 else ""

                    if status == 'closed':
                        continue

                    try:
                        port_num = int(port_proto.split('/')[0])
                    except ValueError:
                        continue

                    result["ports"].append({
                        "port": port_num,
                        "status": status,
                        "service": service,
                        "version": version
                    })

        return result

    except FileNotFoundError:
        log("Error: nmap is not installed or not found in PATH.", 3)
        return None