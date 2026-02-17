import requests
import re
import json

def get_google_images(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    params = {
        "q": query,
        "tbm": "isch",
        "hl": "en",
        "gl": "us",
        "ijn": "0"
    }
    
    html = requests.get("https://www.google.com/search", params=params, headers=headers).text
    
    # Extract image URLs using regex (looking for http/https in likely image containers)
    # This is a bit of a heuristic since Google obfuscates classes
    matches = re.findall(r'\"(https?://[^\"]+?\.jpg|png|jpeg)\"', html)
    
    # Filter for high-res looking ones (not thumbnails)
    images = [url for url in matches if 'gstatic' not in url and 'google' not in url][:3]
    
    if not images:
        # Fallback to any images if strict filtering fails
        images = [url for url in matches if 'http' in url][:3]
        
    return images

if __name__ == "__main__":
    try:
        urls = get_google_images("high quality papaya fruit")
        print(json.dumps(urls))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
