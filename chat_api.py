import os
import cohere

# Set the API key as an environment variable
os.environ['COHERE_API_KEY'] = 'API_KEY'  # Replace with your actual API key

# Initialize Cohere client
co = cohere.Client(os.getenv('COHERE_API_KEY'))

# Test with a simple prompt
response = co.generate(
    model='command',
    prompt='tell me a joke about programming',
    max_tokens=50
)
print(response.generations[0].text)
