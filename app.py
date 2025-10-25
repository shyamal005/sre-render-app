import os
import sys
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    """Main home page."""
    return f"Hello! I am a reliable app deployed on Render, running on PID: {os.getpid()}"

@app.route('/health')
def health_check():
    """Health check endpoint for Render."""
    return "OK", 200

@app.route('/fail')
def fail():
    """This endpoint simulates a hard crash."""
    print("CRASH: Received /fail request. Simulating a hard 'taskkill' crash...")
    try:
        
        current_pid = os.getpid()

                subprocess.call(['taskkill', '/F', '/PID', str(current_pid)])

    except Exception:
        
        os.kill(current_pid, signal.SIGKILL)

    return "Crashing...", 500

