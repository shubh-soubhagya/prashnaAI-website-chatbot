import os
import groq
from dotenv import load_dotenv

# Set your Groq API key
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Dynamically get the correct file path
file_path = r"C:\Users\hp\Desktop\prashna\prashna\content\website_content.txt"
# file_path = r"C:\Users\hp\Desktop\prashna\prashna\scraped_pages\_.txt"

def load_text(file_path):
    """
    Reads the content text file and returns its content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: Content file not found."
    

# def ask_groq(question, client):
#     """
#     Asks a question based on the content of website_content.txt.
#     """
#     content_text = load_text(file_path)
    
#     if "Error" in content_text:
#         return content_text  # Return error if the file is missing
    
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are an AI chatbot trained on a website's content html architecture."
#                         "Answer questions accurately based on the content."
#                         "Just answer in words, don't give any instance of code,"
#                         "If the question is outside the content, answer within a related context."
#                     ),
#                 },
#                 {"role": "user", "content": f"Content: {content_text}\n\nQuestion: {question}"},
#             ],
#             model="llama3-70b-8192",
#             temperature=0.5,
#             max_tokens=1024,
#             top_p=1,
#             stop=None,
#         )
        
#         return chat_completion.choices[0].message.content
    
#     except Exception as e:
#         return f"Error: {str(e)}"
    


def ask_groq(question, client):
    """
    Asks a question based on the content of website_content.txt.
    """
    content_text = load_text(file_path)
    
    if "Error" in content_text:
        return content_text  # Return error if the file is missing
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI chatbot trained on a website's content."
                        "Answer questions accurately based on the content."
                        "If the question is outside the content, answer within a related context."
                    ),
                },
                {"role": "user", "content": f"Content: {content_text}\n\nQuestion: {question}"},
            ],
            model="llama3-70b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"

# def chatbot():
#     """
#     Runs the chatbot in a loop.
#     """
#     if not groq_api_key:
#         print("Error: Please set your Groq API key.")
#         return

#     client = groq.Groq(api_key=groq_api_key)

#     print("Welcome to the website chatbot! Type 'exit' to quit.")
    
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "exit":
#             print("Chatbot: Goodbye!")
#             break
        
#         response = ask_groq(user_input, client)
#         print(f"Chatbot: {response}")

# if __name__ == "__main__":
#     chatbot()
