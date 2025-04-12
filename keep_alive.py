#!/usr/bin/env python
"""
Keep Alive Script for Render Free Tier

This script pings your website periodically to prevent it from going inactive.
You can run this script on any machine that has Python installed and internet access.

Usage:
    python keep_alive.py

Requirements:
    - Python 3.6+
    - requests library (pip install requests)
"""

import requests
import time
import datetime
import sys

# Configuration
WEBSITE_URL = "https://gla-event-feedback.onrender.com/health/"  # Update with your website URL
PING_INTERVAL = 14 * 60  # 14 minutes in seconds (Render free tier suspends after 15 minutes of inactivity)
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def ping_website():
    """Send a request to the website and return the response."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Pinging {WEBSITE_URL}...", end="", flush=True)
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(WEBSITE_URL, timeout=30)
            if response.status_code == 200:
                print(f" Success! Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"Response: {data.get('message', 'No message')}")
                except:
                    print(f"Response: {response.text[:100]}...")
                return True
            else:
                print(f" Failed! Status: {response.status_code}")
                if attempt < MAX_RETRIES - 1:
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
        except requests.RequestException as e:
            print(f" Error: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
    
    print("All retry attempts failed.")
    return False

def main():
    """Main function to periodically ping the website."""
    print(f"Keep Alive Script for {WEBSITE_URL}")
    print(f"Pinging every {PING_INTERVAL // 60} minutes")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        while True:
            ping_website()
            print(f"Sleeping for {PING_INTERVAL // 60} minutes...")
            print("-" * 50)
            time.sleep(PING_INTERVAL)
    except KeyboardInterrupt:
        print("\nScript stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
