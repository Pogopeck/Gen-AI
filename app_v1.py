from flask import Flask, request, jsonify, render_template
import cohere
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Cohere client
co = cohere.Client(os.getenv('COHERE_API_KEY'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Generate response using Cohere
        response = co.chat(
            message=user_message,
            model='command',  # You can also use 'command-light' for faster responses
            temperature=0.7,
            max_tokens=300
        )
        
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
