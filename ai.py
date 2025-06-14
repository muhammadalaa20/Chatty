import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Only load .env if running locally (i.e., __name__ == '__main__')
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

# Configure Gemini with the API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Start chat session globally
chat = genai.GenerativeModel("gemini-2.0-flash").start_chat()

@app.route('/chat', methods=['POST'])
def chat_api():
    user_message = request.json.get("message")
    try:
        response = chat.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run locally only (on your machine)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
