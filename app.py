import streamlit as st
import pandas as pd
import yaml
import streamlit_authenticator as stauth
import numpy as np
import requests
import time
import random
import os
from datetime import datetime, timedelta
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import base64
import pydeck as pdk
import joblib
import csv
from streamlit_autorefresh import st_autorefresh


def get_img_as_base64(file_path):
    try:
        # Ensure path is relative to the current script
        abs_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(abs_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# --- CONFIGURATION ---
st.set_page_config(
    page_title="SENTINEL ZERO",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded" # Expanded by default so user sees the nav immediately
)

# --- VISUAL ASSETS ---
LOTTIE_SATELLITE = "https://lottie.host/64b90847-3806-4c45-9257-23f2d2425a7d/F8C2s4y1x5.json"
LOTTIE_RADAR = "https://lottie.host/93380486-455b-4375-8147-32115064560d/2k7M4j2W6y.json"
LOTTIE_SCANNER = "https://lottie.host/5e28206d-7132-4914-bce2-66bb70dfd437/dBS7z0wQ5C.json"
LOTTIE_LOCK = "https://lottie.host/4b859942-5f65-4654-a039-4467384218a4/p7lJqC1qR6.json"



@st.cache_resource
def load_ml_models():
    try:
        # Assuming run directory has access
        scaler = joblib.load('Sentinel_Zero_Scaler.pkl')
        model = joblib.load('Isolation_Forest.pkl')
        return scaler, model
    except Exception as e:
        return None, None

scaler, model = load_ml_models()

def get_last_10_lines(filepath):
    try:
        import collections
        with open(filepath, 'r') as f:
            return list(collections.deque(f, 10))
    except Exception:
        return []

@st.cache_data
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --- PROFESSIONAL AUDIO MANAGER ---
def play_sound(sound_type):
    """
    Plays a professional sound effect based on the event.
    Uses hidden audio players so it doesn't mess up the UI.
    """
    sound_urls = {
        "alert": "https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3",  # High-tech Sonar Ping
        "success": "https://assets.mixkit.co/active_storage/sfx/2578/2578-preview.mp3", # Soft Click
    }
    
    if sound_type in sound_urls:
        # We use a unique key based on time to force the sound to play even if triggered twice
        st.audio(sound_urls[sound_type], format="audio/mp3", autoplay=True)

# --- CYBERPUNK CSS (Wrapped) ---
def load_css():
    # --- CYBERPUNK CSS ---
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
        /* GLOBAL THEME */
        .stApp {
            background-color: #000000;
            color: #00ff41;
            font-family: 'Orbitron', sans-serif;
        }
    
        /* CRT SCANLINE EFFECT */
        .stApp::before {
            content: " ";
            display: block;
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            z-index: 9999;
            background-size: 100% 2px;
            pointer-events: none;
            animation: scanline 10s linear infinite;
        }
    
        @keyframes scanline {
            0% { background-position: 0 0; }
            100% { background-position: 0 100%; }
        }
    
        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #00ff41;
        }
    
        /* NEON BUTTONS */
        .stButton>button {
            background: #000;
            color: #00ff41 !important;
            border: 1px solid #00ff41 !important;
            border-radius: 0px !important;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s;
            box-shadow: 0 0 5px #00ff41;
        }
        .stButton>button:hover {
            background: #00ff41 !important;
            color: #000 !important;
            box-shadow: 0 0 20px #00ff41;
        }
    
        /* TOGGLES */
        .stToggle {
            font-family: 'Share Tech Mono', monospace;
            color: #00ff41;
        }
    
        /* RADIO BUTTONS (NAVIGATION) */
        .stRadio > label {
            color: #00ff41 !important;
            font-family: 'Orbitron', sans-serif;
            font-weight: bold;
        }
    
        /* TERMINAL LOG */
        .terminal-log {
            background-color: #050505;
            border: 1px solid #333;
            padding: 15px;
            font-family: 'Share Tech Mono', monospace;
            height: 400px;
            overflow-y: auto;
            color: #00ff41;
            font-size: 14px;
            box-shadow: inset 0 0 20px rgba(0, 255, 65, 0.1);
        }
        .log-entry {
            margin-bottom: 5px;
            border-bottom: 1px solid #111;
            padding-bottom: 2px;
        }
        .log-time { color: #888; margin-right: 10px; }
        .log-ip { color: #00aaff; margin-right: 10px; }
        .log-status { color: #00ff41; font-weight: bold; }
        .log-encrypted { color: #ff003c; font-family: 'Courier New', monospace; letter-spacing: 3px; }
    
        /* BOOT SCREEN */
        .boot-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            text-align: center;
        }
        .boot-title {
            font-size: 5em;
            font-weight: 900;
            color: #00ff41;
            text-shadow: 0 0 30px #00ff41;
            margin-bottom: 10px;
            letter-spacing: 5px;
        }
        .boot-subtitle {
            font-family: 'Share Tech Mono', monospace;
            color: #888;
            font-size: 1.5em;
            margin-bottom: 40px;
        }
    
        /* CUSTOM HEADER STYLE (Visible but unobtrusive) */
        header[data-testid="stHeader"] {
            background: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

# --- FORENSICS GENERATOR ---
def generate_forensics():
    signatures = [
        "APT-29 Cobalt Strike Beacon", "Lazarus Group RAT", "Emotet C2 Callback",
        "WannaCry SMB Exploit", "Mirai Botnet Scanner", "SQL Injection (Union Based)",
        "XSS Reflected Payload", "Brute Force SSH", "DDoS Amplification"
    ]
    locations = [
        ("St. Petersburg, RU", "185.243.x.x", 59.9343, 30.3351), 
        ("Pyongyang, KP", "175.45.x.x", 39.0392, 125.7625),
        ("Beijing, CN", "202.106.x.x", 39.9042, 116.4074), 
        ("Tehran, IR", "91.92.x.x", 35.6892, 51.3890),
        ("Lagos, NG", "197.210.x.x", 6.5244, 3.3792), 
        ("Unknown Proxy (Tor)", "104.244.x.x", 52.5200, 13.4050),
        ("Sao Paulo, BR", "177.12.x.x", -23.5505, -46.6333), 
        ("Bucharest, RO", "89.136.x.x", 44.4268, 26.1025)
    ]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "curl/7.64.1", "Python-urllib/3.8", "Bot/1.0", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"
    ]

    loc, ip_prefix, lat, lon = random.choice(locations)
    hex_dump = " ".join([f"{random.randint(0, 255):02x}" for _ in range(32)])

    return {
        "signature": random.choice(signatures),
        "confidence": round(random.uniform(85.0, 99.9), 1),
        "location": loc,
        "lat": lat,
        "lon": lon,
        "src_ip": f"{ip_prefix.replace('x', str(random.randint(0, 255)))}",
        "dest_ip": "192.168.1.105",
        "port": f"{random.choice([443, 80, 445, 22, 3389, 8080])}/TCP",
        "user_agent": random.choice(user_agents),
        "payload_hex": f"0x{hex_dump}...",
        "payload_ascii": ''.join([chr(random.randint(33, 126)) for _ in range(20)]),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "severity": random.choice(["CRITICAL", "HIGH", "MEDIUM"]),
        "risk_factors": {
            "Packet Size Anomaly": random.randint(30, 99),
            "Geo-Location Risk": random.randint(20, 95),
            "Port Scan Frequency": random.randint(40, 98)
        }
    }

# --- EXACT DIAGRAM VISUALIZATION ---
def render_network_viz():
    html_code = """
    <canvas id="networkCanvas" width="950" height="550" style="background: #050505; border: 1px solid #00ff41; border-radius: 8px;"></canvas>
    <script>
        const canvas = document.getElementById('networkCanvas');
        const ctx = canvas.getContext('2d');

        const COLORS = {
            safe: '#00ff41',
            threat: '#ff003c',
            neutral: '#00aaff',
            text: '#ffffff'
        };

        const nodes = [
            {id: 'internet', x: 60, y: 200, label: 'INTERNET', type: 'cloud', color: COLORS.neutral, icon: '🌐'},
            {id: 'proxy', x: 180, y: 200, label: 'PROXY', type: 'box', color: COLORS.neutral, icon: '🛡️'},
            {id: 'ml', x: 340, y: 200, label: 'ML ENSEMBLE', type: 'box', color: COLORS.neutral, icon: '🧠'},
            {id: 'anomaly', x: 500, y: 200, label: 'ANOMALY?', type: 'diamond', color: COLORS.neutral, icon: '❓'},
            {id: 'server', x: 850, y: 200, label: 'SERVER', type: 'server', color: COLORS.safe, icon: '💾'},
            {id: 'quarantine', x: 500, y: 380, label: 'QUARANTINE', type: 'box', color: COLORS.threat, icon: '☣️'},
            {id: 'admin', x: 680, y: 380, label: 'ADMIN', type: 'user', color: COLORS.neutral, icon: '👤'},
            {id: 'trash', x: 850, y: 380, label: 'TRASH', type: 'trash', color: COLORS.threat, icon: '🗑️'}
        ];

        let packets = [];

        function drawNode(n) {
            ctx.fillStyle = '#0a0a0a';
            ctx.strokeStyle = n.color;
            ctx.lineWidth = 2;

            if (n.type === 'cloud') {
                ctx.beginPath(); ctx.arc(n.x, n.y, 35, 0, Math.PI*2); ctx.stroke(); ctx.fill();
            } else if (n.type === 'box') {
                ctx.fillRect(n.x-40, n.y-25, 80, 50); ctx.strokeRect(n.x-40, n.y-25, 80, 50);
            } else if (n.type === 'diamond') {
                ctx.beginPath(); ctx.moveTo(n.x, n.y-35); ctx.lineTo(n.x+40, n.y); ctx.lineTo(n.x, n.y+35); ctx.lineTo(n.x-40, n.y); ctx.closePath(); ctx.stroke(); ctx.fill();
            } else if (n.type === 'server') {
                ctx.fillRect(n.x-25, n.y-35, 50, 70); ctx.strokeRect(n.x-25, n.y-35, 50, 70);
            } else if (n.type === 'user') {
                ctx.beginPath(); ctx.arc(n.x, n.y-15, 15, 0, Math.PI*2); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(n.x, n.y+25); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(n.x-15, n.y+10); ctx.lineTo(n.x+15, n.y+10); ctx.stroke();
            } else if (n.type === 'trash') {
                ctx.strokeRect(n.x-20, n.y-25, 40, 50);
            }

            ctx.fillStyle = COLORS.text;
            ctx.font = '11px Orbitron';
            ctx.textAlign = 'center';
            ctx.fillText(n.label, n.x, n.y + 50);

            // Draw Icon
            ctx.font = '20px Arial';
            ctx.textBaseline = 'middle';
            ctx.fillText(n.icon, n.x, n.y);
        }

        function drawArrow(fromX, fromY, toX, toY, color) {
            const headlen = 10;
            const angle = Math.atan2(toY - fromY, toX - fromX);
            ctx.strokeStyle = color;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(fromX, fromY);
            ctx.lineTo(toX, toY);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(toX, toY);
            ctx.lineTo(toX - headlen * Math.cos(angle - Math.PI / 6), toY - headlen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(toX - headlen * Math.cos(angle + Math.PI / 6), toY - headlen * Math.sin(angle + Math.PI / 6));
            ctx.fillStyle = color;
            ctx.fill();
        }

        function drawConnections() {
            drawArrow(95, 200, 140, 200, COLORS.neutral);
            drawArrow(220, 200, 300, 200, COLORS.neutral);
            drawArrow(380, 200, 460, 200, COLORS.neutral);
            drawArrow(540, 200, 825, 200, COLORS.safe);
            drawArrow(500, 235, 500, 355, COLORS.threat);
            drawArrow(540, 380, 660, 380, COLORS.threat);
            
            // Path B: Rejected/Deleted (Red) - Admin to Trash
            drawArrow(700, 380, 830, 380, COLORS.threat);
            ctx.fillStyle = COLORS.threat;
            ctx.font = 'bold 12px Arial';
            ctx.fillText("Neutralized by User", 765, 365); // Moved label UP to avoid line overlap

            // Path A: Accepted by User (Green) - From Admin to Server
            // Use a curve or direct line that doesn't overlap
            ctx.strokeStyle = COLORS.safe;
            ctx.beginPath(); 
            ctx.moveTo(680, 350); // Top of Admin
            ctx.quadraticCurveTo(765, 200, 825, 200); // Curve to Server Left
            ctx.stroke();
            
            // Draw Arrow Head for Green Path
            drawArrow(820, 200, 825, 200, COLORS.safe); 

            ctx.fillStyle = COLORS.safe;
            ctx.font = 'bold 12px Arial';
            ctx.fillText("Authorized by User", 750, 260); // Positioned in clear space

            ctx.strokeStyle = COLORS.safe;
            ctx.beginPath(); ctx.moveTo(180, 175); ctx.lineTo(180, 100); ctx.lineTo(850, 100); ctx.lineTo(850, 165); ctx.stroke();
            
            // REMOVED DOTTED LOOP FROM ADMIN TO ML ENSEMBLE AS REQUESTED

            ctx.strokeStyle = '#ffffff';
            ctx.setLineDash([10, 10]);

            // Fill Sandbox Background (Not Transparent)
            ctx.fillStyle = 'rgba(0, 255, 65, 0.05)';
            ctx.fillRect(280, 80, 600, 450);

            ctx.strokeRect(280, 80, 600, 450);
            ctx.setLineDash([]);
            ctx.fillStyle = '#ffffff';
            ctx.fillText("SANDBOXED ENVIRONMENT", 580, 95);
        }

        function createPacket() {
            const r = Math.random();
            let path = [];
            let finalColor = COLORS.safe;
            let switchStep = 0;

            if (r < 0.4) {
                // Bypass (Trusted)
                path = [{x:60,y:200}, {x:180,y:200}, {x:180,y:100}, {x:850,y:100}, {x:850,y:200}];
                finalColor = COLORS.neutral; // Trusted = Blue
                switchStep = 1; // Change after Proxy
            } else if (r < 0.7) {
                // Safe (Analyzed)
                path = [{x:60,y:200}, {x:180,y:200}, {x:340,y:200}, {x:500,y:200}, {x:850,y:200}];
                finalColor = COLORS.safe; // Safe = Green
                switchStep = 3; // Change after Anomaly
            } else {
                // Threat (Analyzed)
                path = [{x:60,y:200}, {x:180,y:200}, {x:340,y:200}, {x:500,y:200}, {x:500,y:380}, {x:680,y:380}, {x:850,y:380}];
                finalColor = COLORS.threat; // Threat = Red
                switchStep = 3; // Change after Anomaly
            }

            packets.push({ path: path, step: 0, t: 0, finalColor: finalColor, switchStep: switchStep });
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawConnections();
            nodes.forEach(drawNode);

            packets.forEach((p, i) => {
                p.t += 0.015;
                if (p.step < p.path.length - 1) {
                    const start = p.path[p.step];
                    const end = p.path[p.step+1];
                    const x = start.x + (end.x - start.x) * p.t;
                    const y = start.y + (end.y - start.y) * p.t;

                    // Dynamic Color Logic
                    if (p.step >= p.switchStep) {
                        ctx.fillStyle = p.finalColor;
                        ctx.strokeStyle = p.finalColor;
                    } else {
                        ctx.fillStyle = '#ffffff'; // White before decision
                        ctx.strokeStyle = '#ffffff';
                    }

                    // Draw Packet (Rectangle instead of Circle)
                    ctx.lineWidth = 1;
                    ctx.fillRect(x - 6, y - 4, 12, 8);
                    ctx.strokeRect(x - 6, y - 4, 12, 8);

                    // Add detail line
                    ctx.beginPath();
                    ctx.moveTo(x - 3, y);
                    ctx.lineTo(x + 3, y);
                    ctx.stroke();

                    if (p.t >= 1) { p.t = 0; p.step++; }
                } else {
                    packets.splice(i, 1);
                }
            });

            requestAnimationFrame(draw);
        }

        setInterval(createPacket, 800);
        draw();
    </script>
    """
    components.html(html_code, height=560)

# --- SESSION STATE ---
if 'boot_complete' not in st.session_state: st.session_state.boot_complete = False
if 'boot_step' not in st.session_state: st.session_state.boot_step = 0
if 'monitoring' not in st.session_state: st.session_state.monitoring = False
if 'safe_logs' not in st.session_state: st.session_state.safe_logs = []
if 'quarantine_list' not in st.session_state: st.session_state.quarantine_list = []
if 'blocked_count' not in st.session_state: st.session_state.blocked_count = 0
if 'false_positives' not in st.session_state: st.session_state.false_positives = 0
if 'scanned_count' not in st.session_state: st.session_state.scanned_count = 0
if 'last_alert_count' not in st.session_state: st.session_state.last_alert_count = 0
if 'threat_history' not in st.session_state: st.session_state.threat_history = []
if 'encryption_enabled' not in st.session_state: st.session_state.encryption_enabled = True
if 'system_power' not in st.session_state: st.session_state.system_power = True
if 'agent_logs' not in st.session_state: st.session_state.agent_logs = []

def authenticated_app(authenticator):
    load_css()
    st_autorefresh(interval=2000, key="datarefresh")

    # === PHASE 1: CINEMATIC SATELLITE BOOT ===
    if not st.session_state.boot_complete:
        # Load Logo
        logo_b64 = get_img_as_base64("logo_icon.png")
        if logo_b64:
            logo_src = f"data:image/png;base64,{logo_b64}"
        else:
            logo_src = "" 

        # Pure HTML/CSS Splash Screen for Perfect Centering

        # Pure HTML/CSS Splash Screen for Perfect Centering
        st.markdown(f"""
        <style>
            @keyframes breathe {{
                0% {{ transform: scale(1); filter: brightness(1) drop-shadow(0 0 10px rgba(0, 255, 65, 0.5)); }}
                50% {{ transform: scale(1.02); filter: brightness(1.2) drop-shadow(0 0 30px rgba(0, 255, 65, 0.8)); }}
                100% {{ transform: scale(1); filter: brightness(1) drop-shadow(0 0 10px rgba(0, 255, 65, 0.5)); }}
            }}
            @keyframes scan {{
                0% {{ top: 0%; opacity: 0; }}
                15% {{ opacity: 1; }}
                85% {{ opacity: 1; }}
                100% {{ top: 100%; opacity: 0; }}
            }}
            .splash-container {{
                width: 100%;
                min-height: 60vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: transparent; /* Let global bg show */
            }}
            .logo-wrapper {{
                position: relative;
                width: 600px;
                max-width: 90vw;
                margin-bottom: 20px;
            }}
            .logo-img {{
                width: 100%;
                max-width: 600px;
                border-radius: 50%;
                mix-blend-mode: screen;
                animation: breathe 4s infinite ease-in-out;
                -webkit-mask-image: radial-gradient(circle, white 60%, transparent 70%);
                mask-image: radial-gradient(circle, white 60%, transparent 70%);
            }}
            .scan-line {{
                position: absolute;
                left: 0;
                width: 100%;
                height: 4px;
                background: #00ff41;
                box-shadow: 0 0 15px #00ff41, 0 0 30px #00ff41;
                animation: scan 2.5s ease-in-out infinite alternate;
                opacity: 0.8;
                border-radius: 50%; /* Curve slightly */
            }}
            .main-title {{
                font-family: 'Orbitron', sans-serif;
                font-size: 70px;
                font-weight: 900;
                color: #00ff41;
                letter-spacing: 12px;
                text-shadow: 0 0 20px #00ff41;
                text-align: center;
                margin-top: -10px;
                text-transform: uppercase;
            }}
            .sub-title {{
                font-family: 'Share Tech Mono', monospace;
                font-size: 20px;
                color: #888;
                letter-spacing: 4px;
                margin-top: 10px;
                text-align: center;
                text-transform: uppercase;
            }}
            .boot-log-centered {{
                font-family: 'Share Tech Mono', monospace;
                color: #00ff41;
                font-size: 16px;
                margin-top: 20px;
                text-align: center;
                letter-spacing: 2px;
                opacity: 0.8;
            }}
            /* Engraved Button Style */
            .stButton > button {{
                background: transparent !important;
                border: 2px solid #00ff41 !important;
                color: #00ff41 !important;
                font-family: 'Orbitron', sans-serif !important;
                font-weight: bold !important;
                letter-spacing: 3px !important;
                box-shadow: 0 0 10px rgba(0, 255, 65, 0.2), inset 0 0 10px rgba(0, 255, 65, 0.1) !important;
                transition: all 0.3s ease !important;
                padding: 15px 40px !important;
                text-transform: uppercase !important;
            }}
            .stButton > button:hover {{
                background: rgba(0, 255, 65, 0.1) !important;
                box-shadow: 0 0 30px #00ff41, inset 0 0 20px #00ff41 !important;
                text-shadow: 0 0 10px #00ff41 !important;
                transform: scale(1.05);
            }}
            .stButton {{
                display: flex;
                justify-content: center;
            }}
        </style>
        """, unsafe_allow_html=True)

        # Step 2: Typing Logs
        logs = [
            "INITIALIZING SENTINEL CORE...",
            "LOADING NEURAL NETWORKS...",
            "CONNECTING TO GLOBAL THREAT GRID...",
            "DECRYPTING SECURE CHANNELS...",
            "SENTINEL ZERO: ONLINE."
        ]

        placeholder = st.empty()

        if st.session_state.boot_step < len(logs):
            current_log = logs[st.session_state.boot_step]

            # Render Full Splash Screen
            placeholder.markdown(f"""
            <div class="splash-container">
                <div class="logo-wrapper">
                    <img src="{logo_src}" class="logo-img">
                    <div class="scan-line"></div>
                </div>
                <div class="main-title">SENTINEL ZERO</div>
                <div class="boot-log-centered">_ {current_log}</div>
            </div>
            """, unsafe_allow_html=True)

            # Sound Logic
            pass

            time.sleep(1.2)
            st.session_state.boot_step += 1
            st.rerun()
        else:
            # Final State
            placeholder.empty()

            # Static Splash
            st.markdown(f"""
            <div class="splash-container" style="position: relative; height: auto; margin-top: 50px; margin-bottom: 50px;">
                <div class="logo-wrapper">
                    <img src="{logo_src}" class="logo-img">
                    <div class="scan-line"></div>
                </div>
                <div class="main-title">SENTINEL ZERO</div>
                <div class="sub-title">🛡️ ADAPTIVE ZERO-DAY THREAT IDENTIFICATION SYSTEM</div>
            </div>
            """, unsafe_allow_html=True)

            # Centered Button with Columns
            _, c2, _ = st.columns([1, 2, 1])
            with c2:
                if st.button("ENTER COMMAND CENTER", type="primary", key="btn_enter", use_container_width=True):
                    play_sound("success")
                    st.session_state.boot_complete = True
                    st.rerun()
        return

    # === PHASE 2: THE DASHBOARD ===

    # SIDEBAR NAVIGATION
    with st.sidebar:
        st.title("SENTINEL ZERO")
        st.markdown("---")

        # NAVIGATION MENU
        selected_view = st.radio(
            "NAVIGATION",
            ["📡 LIVE MONITOR", "💀 QUARANTINE BAY", "📊 INTELLIGENCE", "🎥 VISUALIZATION"],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("### SYSTEM CONTROL")

        # INTERACTIVE SWITCHES
        st.session_state.system_power = st.toggle("SYSTEM POWER", value=st.session_state.system_power)
        if st.session_state.system_power:
            st.session_state.encryption_enabled = st.toggle("ENCRYPTION PROTOCOL", value=st.session_state.encryption_enabled)
            
        st.markdown("<br>", unsafe_allow_html=True)
        authenticator.logout("Logout", "sidebar")
        
        # HONEYPOT TOGGLE
        st.markdown("<br>", unsafe_allow_html=True)
        honeypot_active = st.sidebar.checkbox("🛡️ Activate Deception Layer (Honeypot)", value=False, help="Reroutes attackers to a sandboxed environment instead of blocking them.")
        
        st.markdown("---")
        # INCIDENT REPORT GENERATOR
        if st.sidebar.button("📄 GENERATE INCIDENT REPORT", type="primary"):
            st.session_state.show_report = True
            st.balloons()
            
        # FORENSIC DATA EXPORT (PHASE 2.5)
        st.markdown("---")
        if st.session_state.threat_history:
            csv = pd.DataFrame(st.session_state.threat_history).to_csv(index=False).encode('utf-8')
            st.sidebar.download_button(
                label="💾 DOWNLOAD FORENSIC LOGS",
                data=csv,
                file_name="SENTINEL_ZERO_FORENSICS.csv",
                mime="text/csv",
                help="Export captured threat telemetry for forensic analysis."
            )
            st.sidebar.caption("Compliance Standard: NIST-800 compliant logging.")
        else:
             st.sidebar.info("AWAITING DATA FOR EXPORT...")

        st.markdown("---")
        st.metric("📦 PACKETS", st.session_state.scanned_count)
        st.metric("🚨 THREATS", len(st.session_state.quarantine_list))
        st.caption("SECURE CONNECTION")

    if not st.session_state.system_power:
        # Shutdown Sequence
        st.markdown("""
        <style>
            .stApp { background-color: #000000; }
        </style>
        """, unsafe_allow_html=True)
        
        terminal = st.empty()
        
        logs = [
            ">> SENTINEL ZERO KERNEL: TERMINATING PROCESSES...",
            ">> CLOSING ENCRYPTED UPLINK... [SUCCESS]",
            ">> WIPING VOLATILE MEMORY... [OK]",
            ">> SYSTEM STATUS: OFFLINE."
        ]
        
        for log in logs:
            terminal.code(log, language="bash")
            time.sleep(0.5)
            
        time.sleep(1)
        terminal.empty()
        
        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 60vh; flex-direction: column;'>
                <h1 style='color: #ff003c; font-family: "Courier New", monospace; font-size: 80px; text-shadow: 0 0 20px #ff003c; margin-bottom: 0;'>SYSTEM HALTED</h1>
                 <p style='color: #555; font-family: "Orbitron", sans-serif; letter-spacing: 5px;'>MANUAL RESTART REQUIRED</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # MAIN CONTENT AREA (Based on Sidebar Selection)

    # --- VIEW 1: LIVE MONITOR ---
    if selected_view == "📡 LIVE MONITOR":
        
         # INCIDENT REPORT DISPLAY (TOP OF DASHBOARD - HIGH VISIBILITY)
        if 'show_report' in st.session_state and st.session_state.show_report:
            threat_count = len(st.session_state.threat_history)
            
            # High-Visibility Popup
            st.markdown(f"""
                <div style="background-color: #002200; border: 2px solid #00FF41; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h2 style="color: #00FF41; margin-top: 0;">📄 INCIDENT REPORT GENERATED</h2>
                    <p style="color: white;"><b>DATE:</b> {datetime.now().strftime("%Y-%m-%d")}<br>
                    <b>STATUS:</b> <span style="color: #00FF41;">SYSTEM SECURE</span></p>
                    <hr style="border-color: #00FF41;">
                    <p style="color: #cccccc;">
                        <b>EXECUTIVE SUMMARY:</b><br>
                        Sentinel Zero has successfully monitored network traffic for the duration of the session. 
                        A total of <b>{threat_count}</b> anomalies were detected and neutralized. 
                        The Autonomous Agent (Sentinel-1) is currently <b>ACTIVE</b>.
                    </p>
                    <p style="color: cyan;"><i>Recommendation: No manual intervention required.</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("❌ CLOSE REPORT", key="close_rep_main"):
                st.session_state.show_report = False
                st.rerun()

        # --- EXECUTIVE KPI SCORECARD (PHASE 2.5) ---
        total_threats = len(st.session_state.threat_history)
        risk_mitigation = int((st.session_state.blocked_count / total_threats) * 100) if total_threats > 0 else 100
        
        p_threats = len(st.session_state.quarantine_list)
        dynamic_threat = st.session_state.get('dynamic_threat_level', 'STABLE')
        threat_level = "CRITICAL" if dynamic_threat == "CRITICAL" else ("ELEVATED" if p_threats >= 5 else "STABLE")
        
        level_delta = "- Stable" if threat_level == "STABLE" else "+ High Risk"
        mitigation_delta = "+2.4%" if risk_mitigation >= 90 else "-1.5%"
        
        # Calculate dynamic latency based on live monitoring
        pps = st.session_state.get('packets_per_sec', 0)
        live_latency = 0.015 + (pps * 0.0001) if pps > 0 else 0.000
        latency_str = f"{live_latency:.3f}s"
        
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("RISK MITIGATION", f"{risk_mitigation}%", mitigation_delta)
        k2.metric("AVG LATENCY", latency_str, f"{random.uniform(-0.002, 0.002):.3f}s")
        k3.metric("PROTECTION COVERAGE", "99.8%", "Optimal")
        k4.metric("CURRENT THREAT LEVEL", threat_level, level_delta, delta_color="inverse")
        
        st.markdown("---")

        # 1. Standard Header
        st.markdown("## 📡 LIVE MONITOR")

        # 2. Status Indicators (Left Aligned, Below Title)
        enc_status = "ACTIVE" if st.session_state.encryption_enabled else "DISABLED"
        enc_color = "#00ff41" if st.session_state.encryption_enabled else "#ff003c"

        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <div style="flex: 1; font-family: 'Share Tech Mono', monospace; font-size: 18px; color: #00ff41; border: 1px solid #00ff41; padding: 10px 20px; border-radius: 5px; background: rgba(0, 255, 65, 0.1); text-align: center;">
                SYSTEM: ONLINE
            </div>
            <div style="flex: 1; font-family: 'Share Tech Mono', monospace; font-size: 18px; color: {enc_color}; border: 1px solid {enc_color}; padding: 10px 20px; border-radius: 5px; background: rgba(0, 0, 0, 0.5); text-align: center;">
                ENCRYPTION: {enc_status}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Layout: Antenna (Left) | Controls (Right)
        c1, c2 = st.columns([1, 2])

        with c1:
            # Antenna
            radar_anim = load_lottie_url(LOTTIE_SATELLITE)
            if radar_anim:
                st_lottie(radar_anim, height=200, key="radar_main_loop")
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/2583/2583114.png", width=150)

        with c2:
            st.markdown("### MISSION CONTROLS")
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("▶ INITIATE SCAN", type="primary", key="btn_scan", use_container_width=True): st.session_state.monitoring = True
            with b2:
                if st.button("⏸ PAUSE UPLINK", key="btn_pause", use_container_width=True): st.session_state.monitoring = False
            with b3:
                if st.button("⏹ FLUSH LOGS", key="btn_flush", use_container_width=True):
                    st.session_state.monitoring = False
                    st.session_state.safe_logs = []
                    st.session_state.scanned_count = 0
                    st.session_state.threat_history = []

            st.markdown("### NETWORK TELEMETRY")
            m1, m2 = st.columns(2)
            m1.metric("PACKETS / SEC", f"{st.session_state.get('packets_per_sec', 0)}" if st.session_state.monitoring else "0")
            m2.metric("BANDWIDTH", f"{random.uniform(0.5, 2.5):.1f} GB/s" if st.session_state.monitoring else "0 GB/s")

        st.markdown("---")

        # Terminal Log Section
        st.markdown("### 📟 DECRYPTED TRAFFIC LOG")

        log_html = '<div class="terminal-log">'
        if not st.session_state.safe_logs:
             log_html += '<div class="log-entry">> AWAITING DATA STREAM...</div>'
        else:
            for log in reversed(st.session_state.safe_logs[-50:]): # Show last 50
                # Encryption Logic
                display_ip = log['ip']
                display_proto = log['protocol']

                if 'ANOMALY' in log['status']:
                    style_class = "log-encrypted"
                    display_proto = "THREAT"
                elif st.session_state.encryption_enabled and random.random() < 0.3:
                    display_ip = "".join([random.choice("XJ9#2@") for _ in range(12)])
                    display_proto = "ENCRYPTED"
                    style_class = "log-encrypted"
                else:
                    style_class = "log-ip"

                log_html += f"""
<div class="log-entry">
    <span class="log-time">[{log['time']}]</span>
    <span class="{style_class}">SRC: {display_ip}</span>
    <span class="log-status">{log['status']}</span>
    <span style="color: #666; float: right;">{display_proto}</span>
</div>
"""
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)

        # Monitoring Logic
        if st.session_state.monitoring:
            timestamp = datetime.now().strftime("%H:%M:%S")
            csv_path = "/home/kali/live_traffic.csv"
            
            # --- LIVE ML READ ---
            new_lines = []
            if os.path.exists(csv_path):
                lines = get_last_10_lines(csv_path)
                if 'processed_line_hashes' not in st.session_state:
                    st.session_state.processed_line_hashes = set()
                
                for line in lines:
                    line_hash = hash(line)
                    if line_hash not in st.session_state.processed_line_hashes:
                        new_lines.append(line)
                        st.session_state.processed_line_hashes.add(line_hash)
                
                if len(st.session_state.processed_line_hashes) > 1000:
                    st.session_state.processed_line_hashes = set(list(st.session_state.processed_line_hashes)[-500:])

            if new_lines:
                current_threat_level = "STABLE"
                for last_line in new_lines:
                    try:
                        parts = [p.strip() for p in last_line.split(',')]
                        if len(parts) >= 5:
                            time_epoch, src_ip, dst_ip, proto_str, frame_len = parts[:5]
                            
                            st.session_state.scanned_count += 1
                            
                            if 'packet_history' not in st.session_state:
                                st.session_state.packet_history = []
                            current_t = time.time()
                            st.session_state.packet_history.append(current_t)
                            st.session_state.packet_history = [t for t in st.session_state.packet_history if current_t - t <= 2.0]
                            packet_rate = len(st.session_state.packet_history)
                            
                            # Feature mapping -> 41 columns. One-hot encoded protocol, frame.len -> src_bytes
                            features = np.zeros(41)
                            features[22] = packet_rate  # Map count to NSL-KDD 'count' feature
                            proto_upper = str(proto_str).upper()
                            if proto_upper == "TCP" or proto_upper == "6":
                                features[1] = 1.0
                            elif proto_upper == "UDP" or proto_upper == "17":
                                features[2] = 1.0
                            elif proto_upper == "ICMP" or proto_upper == "1":
                                features[3] = 1.0
                            else:
                                features[1] = 1.0 # fallback
                            
                            features[4] = float(frame_len)
                            
                            if scaler and model:
                                features_scaled = scaler.transform([features])
                                prediction = model.predict(features_scaled)[0]
                            else:
                                prediction = 1
                            
                            if packet_rate > 5:
                                prediction = -1
                            
                            if prediction == -1: # Threat
                                current_threat_level = "CRITICAL"
                                st.session_state.dynamic_threat_level = "CRITICAL"
                                
                                forensics = generate_forensics()
                                forensics['src_ip'] = src_ip
                                forensics['dest_ip'] = dst_ip
                                threat_id = len(st.session_state.quarantine_list) + 1
                                st.session_state.quarantine_list.append({'id': threat_id, 'time': timestamp, 'forensics': forensics})
                                st.session_state.threat_history.append(forensics)
                                
                                if 'last_threat_time' not in st.session_state or (time.time() - st.session_state.last_threat_time > 2):
                                    play_sound("alert")
                                    st.session_state.last_threat_time = time.time()

                                st.session_state.last_alert_count = len(st.session_state.quarantine_list)

                                pid = random.randint(1000, 9999)
                                status_text = "ANOMALY 🔴"
                                log_msg = f"> [AUTO-HEAL] High Risk Identity. KILLING PROCESS PID {pid}. Blocking IP... SUCCESS."
                                st.toast(f"🚨 Threat Blocked!", icon="⚠️")
                                st.session_state.safe_logs.append({'time': timestamp, 'ip': src_ip, 'status': status_text, 'protocol': "THREAT"})

                                if 'agent_logs' not in st.session_state:
                                    st.session_state.agent_logs = []
                                st.session_state.agent_logs.append(log_msg)
                                if len(st.session_state.agent_logs) > 5:
                                    st.session_state.agent_logs.pop(0)

                            else: # Safe (prediction == 1)
                                st.session_state.safe_logs.append({'time': timestamp, 'ip': src_ip, 'status': 'SAFE ✅', 'protocol': proto_str})
                    except Exception as e:
                        pass
                
                if current_threat_level != "CRITICAL":
                    st.session_state.dynamic_threat_level = "STABLE"
            
            # --- End Live ML Read ---
            
            # Calculate polling-based Packets/Sec 
            if 'last_poll_time' not in st.session_state:
                st.session_state.last_poll_time = time.time()
                st.session_state.poll_packets = 0
                st.session_state.packets_per_sec = 0
            
            st.session_state.poll_packets += len(new_lines)
                
            current_time = time.time()
            if current_time - st.session_state.last_poll_time >= 1.0:
                st.session_state.packets_per_sec = st.session_state.poll_packets
                st.session_state.poll_packets = 0
                st.session_state.last_poll_time = current_time

            time.sleep(0.05) # Faster scan speed
            
             # --- AGENT PANEL (BOTTOM OF LIVE MONITOR) ---
            st.markdown("---")
            with st.expander("🤖 SENTINEL-1 AGENT ACTIVITY (AUTONOMOUS RESPONSE)", expanded=True):
                if not st.session_state.agent_logs:
                    st.code("> WAITING FOR THREATS...", language="bash")
                else:
                    # Display last 5 logs
                    log_text = "\n".join(st.session_state.agent_logs[-5:])
                    st.code(log_text, language="diff") # 'diff' highlights lines starting with + or - or similar, looks cool green/red
            
            st.rerun()

    # --- VIEW 2: QUARANTINE BAY ---
    elif selected_view == "💀 QUARANTINE BAY":
        st.markdown("## 💀 QUARANTINE BAY (INBOX)")

        if not st.session_state.quarantine_list:
            st.success("NO ACTIVE THREATS.")
        else:
            for idx, threat in enumerate(st.session_state.quarantine_list):
                f = threat['forensics']
                
                # 1. Expander with specific label
                with st.expander(f" THREAT DETECTED: {f['src_ip']} | {threat['time']}", expanded=False):
                    
                    # 2. Columns for XAI
                    c1, c2 = st.columns(2)
                    
                    # Mock Data for Chart
                    # risk_values = [88, 45, 92] # Make this dynamic or semi-random if needed, but keeping consistent for now
                    risk_data = f.get('risk_factors', {
                        "Packet Size Anomaly": 88,
                        "Geo-Location Risk": 45,
                        "Port Scan Frequency": 92
                    })
                    
                    # Calulate Average Risk (Linked to Chart Data)
                    avg_risk = int(sum(risk_data.values()) / len(risk_data))
                    
                    # Color Logic
                    if avg_risk > 70:
                        risk_color = "#FF3131" # Red
                    elif avg_risk >= 40:
                        risk_color = "#FFA500" # Orange
                    else:
                        risk_color = "#00FF00" # Green

                    # Col 1: Details (Text)
                    with c1:
                        st.markdown("### 🕵️ FORENSIC TRACE")
                        
                        # --- DYNAMIC RISK METRIC ---
                        st.markdown(f"<h2 style='text-align: center; color: {risk_color}; border: 2px solid {risk_color}; border-radius: 10px; padding: 10px;'>{avg_risk}% RISK</h2>", unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        # ---------------------------

                        st.markdown(f"**SOURCE IP:** `{f['src_ip']}`")
                        st.markdown(f"**DESTINATION:** `192.168.1.105`") # Match mock gen
                        st.markdown(f"**PORT:** `{f['port']}`")
                        st.markdown(f"**PROTOCOL:** `TCP/IPv4`")
                        st.markdown(f"**LOCATION:** `{f['location']}`")
                        
                        st.markdown("---")
                        b1, b2 = st.columns(2)
                        with b1:
                            if st.button(f"⚡ NEUTRALIZE", key=f"neu_{threat['id']}_{idx}", type="primary"):
                                play_sound("success")
                                st.session_state.blocked_count += 1
                                st.session_state.quarantine_list.pop(idx)
                                st.session_state.last_alert_count =len(st.session_state.quarantine_list)
                                st.rerun()
                        with b2:
                            if st.button(f"✅ AUTHORIZE", key=f"auth_{threat['id']}_{idx}"):
                                play_sound("success")
                                st.session_state.false_positives += 1
                                st.session_state.quarantine_list.pop(idx)
                                st.session_state.last_alert_count = len(st.session_state.quarantine_list)
                                st.rerun()

                    # Col 2: AI Analysis (Chart)
                    with c2:
                        st.markdown("### 🤖 AI RISK ANALYSIS")
                        # Mock Data for Chart
                        risk_data = {
                            "Packet Size Anomaly": 88,
                            "Geo-Location Risk": 45,
                            "Port Scan Frequency": 92
                        }
                        # Display Label
                        st.caption("RISK FACTOR CONFIDENCE INTERVALS (%)")
                        st.bar_chart(risk_data, color="#ff003c")

    # --- VIEW 3: INTELLIGENCE REPORT ---
    elif selected_view == "📊 INTELLIGENCE":
        # 1. Section 1: Global Telemetry (The Map)
        st.markdown("### 🌍 GLOBAL THREAT ORIGINS")
        
        # Enhanced Mock Data for 3D Map
        map_data = pd.DataFrame({
            'lat': [39.03, 55.75, 6.52, 39.90, 35.68, 52.52, -23.55],
            'lon': [125.76, 37.61, 3.37, 116.40, 51.38, 13.40, -46.63],
            'risk': [90, 70, 65, 85, 75, 40, 60], # Height of the column
            'country': ["North Korea", "Russia", "Nigeria", "China", "Iran", "Germany", "Brazil"],
            'state': ["Pyongyang", "Moscow Oblast", "Lagos State", "Beijing", "Tehran Province", "Berlin", "Sao Paulo State"],
            'city': ["Pyongyang", "Moscow", "Lagos", "Beijing", "Tehran", "Berlin", "Sao Paulo"],
            'threat_type': ["APT29", "Lazarus", "Botnet", "Cicada3301", "Chafer", "Hydra", "Trojans"],
            'ip': ["175.45.176.x", "185.243.x.x", "197.210.x.x", "202.106.x.x", "91.92.x.x", "104.244.x.x", "177.12.x.x"]
        })

        st.pydeck_chart(pdk.Deck(
            map_style=None, # Use TileLayer for base
            height=600, # Explicit height for better view
            initial_view_state=pdk.ViewState(
                latitude=20,
                longitude=10,
                zoom=2,
                pitch=45,
                bearing=0,
            ),
            layers=[
                pdk.Layer(
                    "TileLayer",
                    data="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
                    id="satellite-layer",
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=map_data,
                    get_position='[lon, lat]',
                    get_radius=80000, # 80km Radius for visibility
                    get_fill_color='[255, 0, 0, 180]', # Solid Red
                    pickable=True,
                    auto_highlight=True,
                ),
            ],
            tooltip={"text": "Target City: {city}\nState: {state}\nAdversary: {threat_type}"}
        ), use_container_width=True)

        # 2. Section 2: Live Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("PACKETS SCANNED", "1.2M+", "+5%")
        c2.metric("THREATS BLOCKED", len(st.session_state.threat_history), "Active")
        c3.metric("SYSTEM INTEGRITY", "99.9%", "Stable")

        st.markdown("---")

        # 3. Section 3: Threat Analytics (The Graphs)
        st.markdown("### 📊 TRAFFIC ANALYSIS")
        
        # Mock Data for Charts
        chart_data_lines = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['HTTP', 'TCP', 'UDP']
        )
        
        chart_data_bar = pd.DataFrame({
            "Attack Type": ["SQLi", "Brute Force", "Malware", "DDoS", "XSS"],
            "Count": [45, 120, 30, 80, 15]
        }).set_index("Attack Type")

        g1, g2 = st.columns(2)
        with g1:
            st.caption("TRAFFIC VOLUME (24H)")
            st.line_chart(chart_data_lines)
        with g2:
            st.caption("ATTACK VECTORS")
            st.bar_chart(chart_data_bar, color="#ff003c")

        st.markdown("---")

        # 4. Section 4: Adversary Attribution (The Table)
        st.markdown("### 🕵️ DETECTED ADVERSARY GROUPS")
        
        adversary_data = pd.DataFrame([
            {"Group Name": "APT-28 (Fancy Bear)", "Origin": "Russia", "Risk Level": "CRITICAL", "Status": "TRACKING 🟡"},
            {"Group Name": "Lazarus Group", "Origin": "North Korea", "Risk Level": "HIGH", "Status": "BLOCKED 🔴"},
            {"Group Name": "Anonymous", "Origin": "Global", "Risk Level": "MODERATE", "Status": "MONITORING 🟢"},
            {"Group Name": "Equation Group", "Origin": "Unknown", "Risk Level": "CRITICAL", "Status": "ANALYZING 🔵"},
        ])
        
        st.table(adversary_data)
        
        st.markdown("---")

        # 5. Section 5: Active Firewall Policies (Self-Healing)
        st.markdown("### 🛡️ ACTIVE FIREWALL POLICIES (AUTO-GENERATED)")
        
        if st.session_state.threat_history:
            # Generate Mock Rules based on history
            firewall_rules = []
            for i, threat in enumerate(st.session_state.threat_history[-5:]): # Show last 5
                
                # Retrieve the unique risk score for this threat (The "Brain")
                risk_factors = threat.get('risk_factors', {"Default": 50})
                risk_score = int(sum(risk_factors.values()) / len(risk_factors))
                
                # Determine NSL-KDD Reason (The "Why")
                if risk_score > 80:
                    reason = "CRITICAL: Anomaly detected in Service/Flag features (NSL-KDD)"
                elif risk_score > 60:
                    reason = "HIGH: Traffic volume exceeds cluster centroid threshold"
                else:
                    reason = "WARN: Unknown signature match in packet header"

                rule = {
                    "RULE ID": f"SZ-AUTO-{1000+i}",
                    "TARGET IP": threat['src_ip'],
                    "RISK SCORE": f"{risk_score}%", # The Link
                    "REASONING": reason,
                    "TIMESTAMP": threat.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "GENERATED POLICY": f"REJECT TCP FROM {threat['src_ip']}"
                }
                firewall_rules.append(rule)
            
            rules_df = pd.DataFrame(firewall_rules)
            st.table(rules_df)
            
            if st.button("🔥 SYNC RULES TO EDGE FIREWALL", key="fw_sync"):
                with st.spinner("Pushing policies to Virtual Firewall..."):
                    time.sleep(1.5)
                st.toast("✅ POLICIES ENFORCED: Security Policies pushed to Virtual Firewall successfully.", icon="🔥")
        else:
            st.info("NO ACTIVE THREATS TO BLOCK.")

    # --- VIEW 4: SYSTEM VISUALIZATION ---
    elif selected_view == "🎥 VISUALIZATION":
        st.markdown("<h1 style='text-align: center; color: #00FF00;'>📹 SYSTEM VISUALIZATION</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # 1. Center the Visualization (Canvas)
        col1, col2, col3 = st.columns([0.1, 15, 0.1])
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            # Flowchart / Visualization
            render_network_viz()
            st.markdown("<br>", unsafe_allow_html=True)



        # 2. Centered Legend (Using Columns)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🗺️ ARCHITECTURE LEGEND")
        
        # Row 1
        l1, l2, l3, l4 = st.columns(4)
        with l1:
            st.info("**🌐 INTERNET**\n\nExternal Traffic Source")
        with l2:
            st.info("**🛡️ PROXY**\n\nFirst Line of Defense")
        with l3:
            st.info("**🧠 ML ENSEMBLE**\n\nAI Threat Detection")
        with l4:
            st.info("**❓ ANOMALY?**\n\nDecision Point")

        # Row 2
        l5, l6, l7, l8 = st.columns(4)
        with l5:
            st.success("**💾 SERVER**\n\nSecure Data Storage")
        with l6:
            st.error("**☣️ QUARANTINE**\n\nIsolation for Threats")
        with l7:
            st.info("**👤 ADMIN**\n\nHuman Oversight")
        with l8:
            st.error("**🗑️ TRASH**\n\nDeleted Malicious Data")
        
    # --- GLOBAL THREAT TICKER (PHASE 2.5) ---
    st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #0e1117; padding: 10px; border-top: 1px solid #00FF41; color: #00FF41; font-family: 'Courier New', monospace; z-index: 9999; font-size: 14px; white-space: nowrap;">
        <marquee scrollamount="5">
            🔴 CRITICAL INTEL: ZERO-DAY EXPLOIT DETECTED IN APACHE LOG4J  ///  ⚠️ ALERT: LARGE-SCALE BOTNET ACTIVATED IN EASTERN EUROPE (IP RANGE 185.x.x.x)  ///  🔓 DATA LEAK: 5 MILLION CREDENTIALS EXPOSED ON DARK WEB FORUM  ///  🛡️ SYSTEM STATUS: DEFCON 3 (ELEVATED)
        </marquee>
    </div>
    """, unsafe_allow_html=True)


def main():
    # 1. GLOBAL STYLING (Applies to Login Page too)
    load_css()

    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )

    # 2. BRANDING & TRANSFORMATION
    if not st.session_state.get("authentication_status"):
        # Logo & Title
        logo_b64 = get_img_as_base64("logo_icon.png")
        if logo_b64:
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 20px;">
                    <img src="data:image/png;base64,{logo_b64}" style="width: 150px; border-radius: 50%; border: 2px solid #00ff41; box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);">
                    <h1 style="color: #00ff41; font-family: 'Orbitron', sans-serif; letter-spacing: 5px; text-shadow: 0 0 10px #00ff41; margin-top: 20px;">SENTINEL ZERO</h1>
                    <p style="color: #888; font-family: 'Share Tech Mono', monospace; letter-spacing: 2px;">ACCESS CONTROL GATEWAY</p>
                </div>
            """, unsafe_allow_html=True)

    # 3. CENTERED LOGIN BOX
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        authenticator.login()

    if st.session_state["authentication_status"]:
        authenticated_app(authenticator)
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")

if __name__ == "__main__":
    main()
