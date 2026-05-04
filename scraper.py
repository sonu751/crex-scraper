from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    url = url.replace('crex.com', 'crex.live')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')
        
        if script_tag:
            data = json.loads(script_tag.string)
            return jsonify({"success": True, "data": data})
        else:
            return jsonify({"success": False, "error": "__NEXT_DATA__ not found. (Blocked)"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
