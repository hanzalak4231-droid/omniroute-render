import os
import subprocess
import sys
import shutil
import time
import requests
from threading import Thread


print("=== Starting OmniRoute on Render ===")


# 1. Download & use Node 22.22.2+ (LTS patched)
node_version = "22.22.2"
node_dir = f"/tmp/node-v{node_version}-linux-x64"
if not os.path.exists(os.path.join(node_dir, "bin", "node")):
    print(f"Downloading Node.js v{node_version}...")
    os.system(f"curl -fsSL https://nodejs.org/dist/v{node_version}/node-v{node_version}-linux-x64.tar.xz | tar -xJ -C /tmp")

os.environ["PATH"] = f"{node_dir}/bin:{os.environ.get('PATH', '')}"

print(f"Active Node: {shutil.which('node')}")
print(f"Active NPM: {shutil.which('npm')}")


# 2. Install OmniRoute
print("Installing omniroute@3.8.50...")
subprocess.run(["npm", "install", "omniroute@3.8.50"], check=False)
os.environ["PATH"] = f"./node_modules/.bin:{os.environ.get('PATH', '')}"


# 3. Restore database from backup
print("Restoring database from backup...")
home_dir = os.path.expanduser("~")
omniroute_dir = os.path.join(home_dir, ".omniroute")
os.makedirs(omniroute_dir, exist_ok=True)

# Check if storage.sqlite.gz exists in current directory
backup_file = "storage.sqlite.gz"
target_db = os.path.join(omniroute_dir, "storage.sqlite")

if os.path.exists(backup_file):
    print(f"Found backup file: {backup_file}")
    subprocess.run(["gunzip", "-c", backup_file], stdout=open(target_db, 'wb'), check=False)
    print(f"Database restored! Size: {os.path.getsize(target_db)} bytes")
else:
    print("No backup found, starting with fresh database")


# 4. Self-ping to prevent inactivity (Render free tier sleeps after 15 min)
def keep_alive():
    """Ping self every 10 minutes to stay awake"""
    time.sleep(120)  # Wait for server to start
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "")

    if render_url:
        while True:
            try:
                print(f"[Keep-Alive] Pinging {render_url}/health")
                requests.get(f"{render_url}/health", timeout=5)
            except Exception as e:
                print(f"[Keep-Alive] Ping failed: {e}")
            time.sleep(600)  # Ping every 10 minutes

# Start keep-alive in background
Thread(target=keep_alive, daemon=True).start()


# 5. Start OmniRoute server
port = os.environ.get("PORT", "10000")
print(f"Starting OmniRoute server on port {port}...")

cmd = [f"{node_dir}/bin/npx", "omniroute", "serve", "--port", str(port), "--no-open", "--log"]
print(f"Running command: {' '.join(cmd)}")
sys.stdout.flush()

process = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
process.wait()
