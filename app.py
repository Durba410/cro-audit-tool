from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-3.5-turbo"

@app.route('/')
def serve_html():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/audit', methods=['POST'])
def generate_audit():
    data = request.json
    url = data.get('url', '')
    description = data.get('description', '')

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    prompt = f"""
You are a CRO (Conversion Rate Optimization) expert.
Provide a CRO Audit report for this landing page: {url}
Page Description: {description}

Include:
- Hero section analysis
- CTA effectiveness
- Copy tone
- Trust signals
- Visual hierarchy
- Suggestions
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        result = response.json()

        if 'choices' in result and result['choices']:
            return jsonify({"audit": result['choices'][0]['message']['content']})
        else:
            return jsonify({"error": "No valid response"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)