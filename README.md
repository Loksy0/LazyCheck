# 💤 LazyCheck

LazyCheck is an automated reconnaissance tool that performs deep analysis of a target IP address. It gathers DNS, port, domain, subdomain, CMS, SSL, and leak-related data to help security researchers and analysts quickly understand the footprint of a remote host.

---

## 📦 What Does LazyCheck Collect?

LazyCheck performs multiple types of scans and collects:

- IP and DNS information via ViewDNS  
- Open ports and services  
- Hosted domains and online status  
- Subdomains (based on user input or automatic scan)  
- CMS and admin panel detection  
- SSL/TLS certificate details  
- Web application reconnaissance (robots.txt, sitemap.xml, interesting paths)  
- Public data breaches via Leak-Lookup  

All results are saved in a structured format inside the `results/<IP>` directory.

---

## 🧠 Scan Levels

You can choose the depth of analysis using the `lvl` argument:

| Level | Description                                      |
|-------|--------------------------------------------------|
| 1     | Fast scan — minimal data, quick execution        |
| 2     | Balanced — moderate depth and time               |
| 3     | Deep scan — full enumeration, may take hours     |

---

## 🛠️ Installation

```bash
git clone https://github.com/Loksy0/LazyCheck.git
cd LazyCheck
chmod +x install.sh
./install.sh
```

---

## 🚀 How It Works — Step by Step

1. **Run the tool**:  
   ```bash
   python start.py <IP_ADDRESS> <LEVEL>
   ```

2. **Load API keys**:  
   Reads `viewdns.info_api_key` and `leak-lookup.com_api_key` from `config.json`.

3. **IP & DNS Info**:  
   Uses ViewDNS to gather host data.

4. **Port Scan**:  
   Scans open ports and services.

5. **Domain Discovery**:  
   Extracts hosted domains and checks which are online.

6. **Subdomain Enumeration**:  
   Depending on user input and scan level, performs subdomain scans.

7. **CMS/Admin Detection**:  
   Identifies CMS types and admin panels.

8. **SSL Certificate Info**:  
   Collects certificate metadata.

9. **Web Reconnaissance**:  
   Fetches `robots.txt`, `sitemap.xml`, and scans for interesting paths.

10. **Leak Lookup**:  
    Checks for public breaches related to the domain.

11. **Save Results**:  
    All findings are saved in `results/<IP>` as `.txt` and `.json` files.

---

## 🔐 Privacy

LazyCheck performs all scans locally and only uses public APIs. No data is sent to third parties beyond the APIs you configure.

---

## 💸 Support

If you find LazyCheck useful, consider supporting me:

- LTC: `ltc1qcylc450gq9nr2gspn3x905kvj6jesmnm0fj8p6`  
- BTC: `bc1qp52tyf9hykehc4mjexj5ep36asjr0qskywzxtj`  
- ETH: `0x73100e9DcA1C591d07AaDE2B61F30c00Dd6da379`  

---

Thanks for using LazyCheck! 😴
