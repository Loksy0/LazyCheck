import requests

def leaks_check(domain, api_key):
    url = "https://leak-lookup.com/api/search"
    data = {
        "key": api_key,
        "type": "domain",
        "query": domain
    }
    try:
        resp = requests.post(url, data=data, timeout=10)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        return {"error": f"Request failed: {e}"}

    if result.get("error") == "true":
        return {"error": result.get("message", "Unknown error")}

    breaches = result.get("message", {})
    found = []
    for breach_name, details in breaches.items():
        found.append({
            "breach": breach_name,
            "details": details  
        })
    return found
