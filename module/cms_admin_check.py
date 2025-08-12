import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def cms_admin_check(domain):
    cms_signatures = {
        "WordPress": {
            "patterns": [r"wp-content", r"wp-includes", r"WordPress"],
            "version": r"WordPress\s+([0-9.]+)"
        },
        "Drupal": {
            "patterns": [r"Drupal", r"/sites/default", r"/misc/drupal.js"],
            "version": r"Drupal\s+([0-9.]+)"
        },
        "Joomla": {
            "patterns": [r"Joomla", r"/media/system/js/core.js"],
            "version": r"Joomla!\s+([0-9.]+)"
        },
        "OctoberCMS": {
            "patterns": [r"OctoberCMS", r"/modules/system/"],
            "version": r"OctoberCMS\s+([0-9.]+)"
        }
    }

    admin_panels = {
        "AdminLTE": {"patterns": [r"AdminLTE"]},
        "CoreUI": {"patterns": [r"coreui\.css", r"coreui\.js"]},
        "Tabler": {"patterns": [r"tabler\.css", r"tabler\.js"]},
        "Adminer": {"patterns": [r"Adminer"]},
        "webmin": {"patterns": [r"Webmin"]},
        "Vuexy / Material Dashboard": {"patterns": [r"Vuexy", r"Material Dashboard"]},
    }

    found_items = []

    try:
        r = requests.get(domain, timeout=5, verify=False)
        html = r.text

        for cms, sig in cms_signatures.items():
            if any(re.search(p, html, re.I) for p in sig["patterns"]):
                version_match = re.search(sig["version"], html, re.I) if "version" in sig else None
                version = version_match.group(1) if version_match else None
                found_items.append({"type": cms, "version": version})

        admin_paths = [
            "admin", "administrator", "adminer",
            "admin/login", "wp-admin", "user/login"
        ]
        for path in admin_paths:
            try:
                url = f"{domain.rstrip('/')}/{path}"
                resp = requests.get(url, timeout=4, verify=False)
                content = resp.text
                for panel, sig in admin_panels.items():
                    if any(re.search(p, content, re.I) for p in sig["patterns"]):
                        found_items.append({"type": panel, "version": None})
            except requests.RequestException:
                pass

    except requests.RequestException:
        return []

    return found_items
