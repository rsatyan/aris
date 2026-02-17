import json
import time
import requests
import websocket

# Connect to Chrome
try:
    resp = requests.get("http://127.0.0.1:9222/json")
    tabs = resp.json()
    # Find a page target
    ws_url = None
    for tab in tabs:
        if tab.get("type") == "page":
            ws_url = tab.get("webSocketDebuggerUrl")
            break
    if not ws_url:
        # Fallback
        ws_url = tabs[0].get("webSocketDebuggerUrl")
    
    if not ws_url:
        print(json.dumps({"error": "No WebSocket URL found"}))
        exit(1)
except Exception as e:
    print(json.dumps({"error": f"Failed to connect to Chrome: {str(e)}"}))
    exit(1)

print("Connecting to Chrome...", flush=True)
ws = websocket.create_connection(ws_url)
ws.settimeout(2)
print("Connected.", flush=True)

def send_command(method, params={}):
    cmd_obj = {"id": int(time.time()*1000), "method": method, "params": params}
    ws.send(json.dumps(cmd_obj))
    start = time.time()
    while time.time() - start < 10:
        try:
            msg = ws.recv()
            res = json.loads(msg)
            # print(f"Received: {res}", flush=True) # Debug
            if res.get("id") == cmd_obj["id"]:
                return res
        except Exception as e:
            print(f"Error receiving: {e}", flush=True)
            break
    return {}

# Navigate via JS
print("Navigating via JS...", flush=True)
send_command("Runtime.evaluate", {"expression": "window.location.href='https://www.google.com/search?q=high+quality+papaya+photos&tbm=isch'"})
time.sleep(5) # Wait for load

# Evaluate JS to extract images
print("Extracting images...", flush=True)
js_code = """
(function() {
    const images = Array.from(document.querySelectorAll('img')).filter(img => img.src.startsWith('http') && img.width > 100);
    return images.slice(0, 5).map(img => img.src);
})()
"""

res = send_command("Runtime.evaluate", {"expression": js_code, "returnByValue": True})
print(json.dumps(res.get("result", {}).get("value", [])))
js_code = """
(function() {
    const images = Array.from(document.querySelectorAll('img')).filter(img => img.src.startsWith('http') && img.width > 100);
    return images.slice(0, 5).map(img => img.src);
})()
"""

res = send_command("Runtime.evaluate", {"expression": js_code, "returnByValue": True})
print(json.dumps(res.get("result", {}).get("value", [])))

ws.close()
