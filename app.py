from flask import Flask, request, jsonify, render_template
import cohere
import os
import json
from dotenv import load_dotenv
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Cohere client
co = cohere.Client(os.getenv('COHERE_API_KEY'))

# Load applications data
def load_applications_data() -> Dict:
    try:
        with open('data/applications_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default data if file doesn't exist
        return {
            "Cramer": ["Chandan", "Piyush", "Surabhi", "Abdul", "Kajal", "Rohit", "Nikhil"],
            "Geo": ["Abdul", "Rohit", "Surabhi"],
            "Pods": ["Veena", "Minal", "Alina"],
            "Pplus/Mypplus": ["Sandeep", "Rucha"],
            "Com5": ["Sandeep", "Unnati", "Rucha"]
        }

# Save applications data
def save_applications_data(data: Dict):
    os.makedirs('data', exist_ok=True)
    with open('data/applications_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Initialize applications data
applications_data = load_applications_data()

def process_application_query(query: str) -> Optional[str]:
    """Process application-specific queries"""
    query = query.lower()
    
    # Query for members of a specific application
    if "who are the members of" in query or "who is in" in query:
        for app in applications_data.keys():
            if app.lower() in query.lower():
                return f"Members of {app}: {', '.join(applications_data[app])}"
    
    # Query for applications a person is part of
    elif "which applications" in query or "what applications" in query:
        for member in set(sum(applications_data.values(), [])):  # Get unique members
            if member.lower() in query.lower():
                apps = [app for app, members in applications_data.items() if member in members]
                return f"{member} is a member of: {', '.join(apps)}"
    
    # Query for listing all applications
    elif "list all applications" in query:
        return f"Available applications: {', '.join(applications_data.keys())}"
    
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # First try to handle application-specific queries
        app_response = process_application_query(user_message)
        if app_response:
            return jsonify({'response': app_response})
        
        # If not an application query, use Cohere
        response = co.chat(
            message=user_message,
            model='command',
            temperature=0.7,
            max_tokens=300,
            context="You are a helpful assistant that knows about various applications and their team members."
        )
        
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_data', methods=['POST'])
def update_data():
    try:
        new_data = request.json
        save_applications_data(new_data)
        global applications_data
        applications_data = new_data
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Save initial data
    save_applications_data(applications_data)
    app.run(debug=True)
