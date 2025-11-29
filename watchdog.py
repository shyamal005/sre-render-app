import subprocess
import requests
import time
import sys
import datetime
import os 


APP_COMMAND = [sys.executable, "app.py"]
HEALTH_CHECK_URL = "http://127.0.0.1:5000/health"
CHECK_INTERVAL_SECONDS = 5
PID_FILE = "app.pid" 


app_process = None 

def log(message):
    """Simple logger with timestamps."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [WATCHDOG] {message}")

def get_app_pid_from_file():
    """Reads the true app PID from the pid file."""
    try:
    
        time.sleep(1) 
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
            log(f"Got true app PID {pid} from file.")
            return pid
    except Exception as e:
        log(f"Warning: Could not read PID file: {e}")
        return None

def start_app():
    """Starts the web application as a subprocess."""
    log("Attempting to start application...")
    try:
       
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
            
        process = subprocess.Popen(APP_COMMAND)
        log(f"Launcher process started (PID: {process.pid}). Waiting for true PID...")
        
       
        true_pid = get_app_pid_from_file()
        if not true_pid:
            log("CRITICAL: App started but failed to write PID file.")
            
        return proces
    
    except Exception as e:
        log(f"CRITICAL: Failed to start application: {e}")
        return None

def kill_app():
    """Forcefully kills the app using the PID from the file."""
    log("Attempting to kill app process...")
    try:
        if os.path.exists(PID_FILE):
            with open(PID_FILE, 'r') as f:
                pid_to_kill = f.read().strip()
            log(f"Killing process {pid_to_kill} using taskkill...")
            subprocess.call(['taskkill', '/F', '/PID', pid_to_kill])
            os.remove(PID_FILE) 
        else:
            log("No PID file found to kill.")
            
       
        if app_process:
            app_process.terminate()
            
    except Exception as e:
        log(f"Error during kill process: {e}")

def check_app_health():
    """Checks the application's /health endpoint."""
    try:
        response = requests.get(HEALTH_CHECK_URL, timeout=3)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        log("ANOMALY: Health check failed (ConnectionError). App is down.")
        return False
    except Exception as e:
        log(f"ANOMALY: Health check failed with error: {e}")
        return False

def run_watchdog():
    """Main watchdog loop."""
    global app_process
    app_process = start_app()

    while True:
        if not check_app_health():
            
            log("REMEDIATING: App is unhealthy or down. Restarting...")
            kill_app() 
            time.sleep(1) 
            app_process = start_app() 
        else:
            log("Health check OK.")
            
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    log("SRE Watchdog is starting...")
    run_watchdog()

