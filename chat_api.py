import os
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('COHERE_API_KEY')

# Initialize Cohere client
co = cohere.Client(api_key)

def generate_response():
    response = co.generate(
        model='command',
        prompt='tell me a joke about programming',
        max_tokens=50
    )
    return response.generations[0].text

if __name__ == "__main__":
    print(generate_response())

