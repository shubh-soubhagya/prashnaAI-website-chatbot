import groq
from dotenv import load_dotenv
from zero_shot import ask_groq
from scrap_content import extract_content
import os

# Set your Groq API key
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')


# url = "https://indianexpress.com/article/technology/artificial-intelligence/7-free-ghibli-style-ai-image-editors-you-can-use-online-right-now-9917247/"  # Replace with your target website
url = input()

url_info= extract_content(url)


# Dynamically get the correct file path
# file_path = r"\content\website_content.txt"

def chatbot():
    """
    Runs the chatbot in a loop.
    """
    if not groq_api_key:
        print("Error: Please set your Groq API key.")
        return

    client = groq.Groq(api_key=groq_api_key)

    print("Welcome to the website chatbot! Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        
        response = ask_groq(user_input, client)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot()