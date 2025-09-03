import groq
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, jsonify, send_file
import json
import requests
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Define the base directory as inside the Prashna folder
# This assumes the script is run from the Prashna folder
CONTENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content')

# Use proper path separators for files
HISTORY_FILE = os.path.join(CONTENT_DIR, 'history.json')
CONTENT_FILE = os.path.join(CONTENT_DIR, 'website_content.txt')

# Initialize Groq client if key is available
client = None
if groq_api_key:
    client = groq.Groq(api_key=groq_api_key)

# Store chat history
history = {}

def extract_content(url):
    """Extract content from a website URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Remove blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Save the extracted content to a file
        os.makedirs(CONTENT_DIR, exist_ok=True)
        with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
            f.write(text)
            
        return {"url": url, "content": text[:500] + "..."}  # Return truncated content
    except Exception as e:
        raise Exception(f"Failed to extract content: {str(e)}")

def ask_groq(question, content, client):
    """Ask a question based on the content"""
    if not client:
        return "API key not configured. Please set up your GROQ_API_KEY in the .env file."
    
    try:
        # Prepare context and question for the model
        prompt = f"""
        Based on the following website content:
        
        {content}
        
        Please answer the following question:
        {question}
        
        If the answer is not found in the content, please say "I couldn't find information about that in the website content.
        Dont answer in markdown format with special characters, answer in normal text.
        Dont ever give answer in points, always give answer in paragraph."

        """
        
        # Make API call to Groq
        response = client.chat.completions.create(
            model="gemma2-9b-it",  # You can change this to a model of your choice
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on website content. Dont ever give answer in points, always give answer in paragraph."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        # Extract content from the URL
        url_info = extract_content(url)
        
        # Initialize chat history for this URL
        if url not in history:
            history[url] = []
            
        return jsonify({"success": True, "message": "Content extracted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    url = data.get('url')
    
    if not question or not url:
        return jsonify({"error": "Question and URL are required"}), 400
    
    try:
        # Read content from file
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get response from Groq
        response = ask_groq(question, content, client)
        
        # Add to history
        if url not in history:
            history[url] = []
        
        history[url].append({"question": question, "answer": response})
        
        # Save history to JSON file
        os.makedirs(CONTENT_DIR, exist_ok=True)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f)
        
        return jsonify({"success": True, "answer": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history')
def get_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                return jsonify({"success": True, "history": history_data}), 200
        else:
            return jsonify({"success": True, "history": {}}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/content')
def get_content():
    try:
        if os.path.exists(CONTENT_FILE):
            with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({"success": True, "content": content}), 200
        else:
            return jsonify({"error": "Content file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download')
def download_content():
    try:
        if os.path.exists(CONTENT_FILE):
            return send_file(CONTENT_FILE, 
                             as_attachment=True, 
                             download_name='website_content.txt')
        else:
            return jsonify({"error": "Content file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure the content directory exists
    os.makedirs(CONTENT_DIR, exist_ok=True)
    
    # Create history.json if it doesn't exist
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
    
    app.run(debug=True)