#!/usr/bin/env python
"""
Keep-Alive Service for Render
Pings the app every 10 minutes to prevent cold start shutdown
"""

import requests
import time
import sys
from datetime import datetime
import os

# Get app URL from environment or use default
APP_URL = os.getenv('APP_URL', 'https://help-desk-tunisiar.onrender.com')
PING_INTERVAL = int(os.getenv('PING_INTERVAL', 600))  # 10 minutes default

def ping_app():
    """Send a ping request to the app"""
    try:
        response = requests.get(f"{APP_URL}/", timeout=10)
        status = "✓" if response.status_code < 400 else "✗"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {status} Ping {APP_URL}: {response.status_code}")
        return response.status_code < 400
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Ping failed: {str(e)}")
        return False

def main():
    print(f"🚀 Keep-Alive Service Started")
    print(f"   App URL: {APP_URL}")
    print(f"   Interval: {PING_INTERVAL}s ({PING_INTERVAL // 60} minutes)")
    print(f"   Starting pings...\n")
    
    attempt = 0
    while True:
        attempt += 1
        try:
            ping_app()
            time.sleep(PING_INTERVAL)
        except KeyboardInterrupt:
            print("\n\n🛑 Keep-Alive Service Stopped")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(60)  # Retry after 1 minute on error

if __name__ == '__main__':
    main()
