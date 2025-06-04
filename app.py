import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')
API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/audit', methods=['POST'])
def audit():
    data = request.json
    url = data.get('url')
    description = data.get('description')

    if not API_KEY:
        return jsonify({'error': 'API key missing'}), 401

    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'mistralai/mistral-7b-instruct',
                'messages': [
                    {
                        'role': 'user',
                        'content': f"Perform a CRO audit for the following website: {url}\nDescription: {description}\nGive actionable feedback."
                    }
                ]
            }
        )

        response.raise_for_status()
        result = response.json()
        return jsonify({'result': result['choices'][0]['message']['content']})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"OpenRouter API error: {e.response.text if e.response else str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)