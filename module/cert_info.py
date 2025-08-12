import ssl
import socket
from datetime import datetime

def ssl_info(domain):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                protocol = ssock.version()  

        info = {
            "protocol": protocol,
            "subject": dict(x[0] for x in cert.get("subject", [])),
            "issuer": dict(x[0] for x in cert.get("issuer", [])),
            "serialNumber": cert.get("serialNumber"),
            "version": cert.get("version"),
            "notBefore": cert.get("notBefore"),
            "notAfter": cert.get("notAfter"),
        }

        try:
            info["notBefore"] = datetime.strptime(info["notBefore"], "%b %d %H:%M:%S %Y %Z").isoformat()
            info["notAfter"] = datetime.strptime(info["notAfter"], "%b %d %H:%M:%S %Y %Z").isoformat()
        except:
            pass

        return info
    except Exception as e:
        return {"error": str(e)}
