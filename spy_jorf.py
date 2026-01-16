import requests
from bs4 import BeautifulSoup
import datetime

# --- YOUR ENCRYPTED CREDENTIALS ---
TOKEN = "8096577927:AAFUk34msUbh2JwnyObKhyg2d4nxRmzsjns"
CHAT_ID = "1069789419"
# Jorf Lasfar Specific URL on VesselFinder
PORT_URL = "https://www.vesselfinder.com/ports/MAJFL001" 

def send_alert(message):
    """Sends the intelligence directly to your Telegram pocket."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": message, 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Connection Error: {e}")

def get_port_intelligence():
    """Scrapes live data to find the 'Ground Truth'."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(PORT_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # FINDING THE DATA:
        # We look for the table that lists vessels currently in the port.
        vessel_rows = soup.find_all('tr') 
        count = len(vessel_rows)
        
        # WHALE LOGIC: 
        # Usually, Jorf Lasfar has a baseline of activity. 
        # If the row count spikes, it means ships are stacking up.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if count > 45: # This is the "Congestion" threshold
            status = "🚨 *CRITICAL CONGESTION*"
            action = "⚠️ *ACTION:* High risk of demurrage fees for OCP shipments. Draft Whale Letter."
        elif count > 30:
            status = "🟡 *MODERATE DELAY*"
            action = "ℹ️ *MONITOR:* Traffic is increasing above seasonal norms."
        else:
            status = "✅ *OPERATIONAL NORMAL*"
            action = "Keep monitoring. No movement required."

        report = (
            f"{status}\n\n"
            f"📍 *Location:* Jorf Lasfar, Morocco\n"
            f"📅 *Time:* {timestamp}\n"
            f"🚢 *Activity Level:* {count} vessels tracked\n\n"
            f"{action}\n\n"
            f"🔗 [Live Intelligence]({PORT_URL})"
        )
        
        send_alert(report)

    except Exception as e:
        send_alert(f"❌ *SYSTEM ERROR:* Intelligence pipeline broken.\nError: `{str(e)}`")

if __name__ == "__main__":
    get_port_intelligence()