from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)
CORS(app)

# 👇 यहाँ अपनी कॉपी की हुई ScraperAPI Key डालें
API_KEY = "60e35009fe4336cf1150539dd61ccfc3"

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    url = url.replace('crex.com', 'crex.live')
    
    # ScraperAPI Cloudflare Bypass Magic ✨
    scraper_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={url}"
    
    try:
        # ScraperAPI को डेटा लाने में 10-15 सेकंड लग सकते हैं
        response = requests.get(scraper_url, timeout=45)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')
        
        if script_tag:
            data = json.loads(script_tag.string)
            return jsonify({"success": True, "data": data})
        else:
            return jsonify({"success": False, "error": "__NEXT_DATA__ not found. (Still Blocked or Invalid URL)"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
