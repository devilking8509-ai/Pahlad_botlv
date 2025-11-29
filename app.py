import os
import threading
import asyncio
import sys
import time
from flask import Flask, jsonify

# --- IMPORTING BOT ---
# Yahan hum try-except laga rahe hain taki agar main.py mein error ho to pata chale
try:
    from main import StarTinG 
except ImportError as e:
    print(f"CRITICAL ERROR: main.py ya modules missing hain! Error: {e}")
    StarTinG = None

# --- FLASK SETUP ---
app = Flask(__name__)
PORT = int(os.environ.get('PORT', 5000))

# --- LOG FLUSHING (ZARURI HAI) ---
# Ye line ensure karegi ki logs turant dikhein
sys.stdout.reconfigure(line_buffering=True)

bot_status = "Not Started"

def start_bot_core():
    global bot_status
    print("--- BOT THREAD STARTED ---", flush=True)
    
    if StarTinG is None:
        bot_status = "Failed to Import main.py"
        print("Error: main.py import nahi hua. Files check karein.", flush=True)
        return

    try:
        while True:
            print(">>> Launching Bot (StarTinG)...", flush=True)
            bot_status = "Running"
            try:
                # Bot ko run karna
                asyncio.run(StarTinG())
            except Exception as inner_e:
                print(f"Bot function crashed: {inner_e}", flush=True)
            
            print("Bot stopped/crashed! Restarting in 10s...", flush=True)
            bot_status = "Crashed/Restarting"
            time.sleep(10)
    except Exception as e:
        print(f"THREAD CRITICAL ERROR: {e}", flush=True)
        bot_status = f"Error: {str(e)}"
        sys.stdout.flush()

# --- THREAD START LOGIC ---
try:
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        bot_thread = threading.Thread(target=start_bot_core, daemon=True)
        bot_thread.start()
        print("Bot thread command sent...", flush=True)
except Exception as e:
    print(f"Thread Error: {e}", flush=True)

@app.route('/')
def health_check():
    return jsonify({
        "status": "Online", 
        "bot_status": bot_status,
        "logs": "Check Render Logs tab for details"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
