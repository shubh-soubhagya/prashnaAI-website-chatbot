import os
import gradio as gr
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import groq

# Load API key from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = groq.Groq(api_key=groq_api_key) if groq_api_key else None

# Storage for extracted content
# CONTENT_FILE = os.path.join("content", "website_content.txt")
# os.makedirs("content", exist_ok=True)

CONTENT_FILE = r"content\website_content.txt"

def extract_content(url):
    """Extract content from a webpage and save it to a local file."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        text = '\n'.join(chunk for line in soup.get_text().splitlines() for chunk in line.strip().split("  ") if chunk)

        with open(CONTENT_FILE, "w", encoding="utf-8") as f:
            f.write(text)

        return f"✅ Content extracted successfully from {url}"
    except Exception as e:
        return f"❌ Error extracting content: {str(e)}"

def ask_groq(question):
    """Query Groq LLM with a question about the extracted website content."""
    if not client:
        return "❌ API key not configured. Set GROQ_API_KEY in the .env file."

    if not os.path.exists(CONTENT_FILE):
        return "❌ No content found. Please extract a website first."

    try:
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        prompt = f"""
        Based on the following website content:

        {content}

        Please answer the following question:
        {question}

        If the answer is not found, reply with: "I couldn't find information about that in the website content."
        """

        response = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on website content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error: {str(e)}"

def ask_and_update_chat(question, chat_history):
    """Handle chat with persistent history."""
    answer = ask_groq(question)
    chat_history.append((question, answer))
    return chat_history, ""

# Gradio UI
with gr.Blocks(title="Website QA Bot") as demo:
    gr.Markdown("# 🌍 Website Content Q&A (Groq-powered)")
    gr.Markdown(
        "**Introducing the Website URL Chatbot** – simply paste any website link, whether it’s a **blog**, **news article**, "
        "or **research page**, and perform real-time **Q&A**. It transforms any webpage into an **interactive experience**, "
        "helping you understand content **deeply and efficiently**. Ask as many questions as you like – it’s truly **helpful**."
    )


    url_input = gr.Textbox(label="Enter Website URL", placeholder="https://example.com")
    extract_status = gr.Textbox(label="Status", interactive=False)

    extract_btn = gr.Button("Extract Website Content")

    gr.Markdown("## Have an unlimited Chat with Webpage!")

    chatbot = gr.Chatbot(label="Website Chatbot")
    question_input = gr.Textbox(label="Your Question", placeholder="Ask a question about the content...")
    ask_btn = gr.Button("Ask")

    chat_state = gr.State([])

    extract_btn.click(fn=extract_content, inputs=url_input, outputs=extract_status)

    ask_btn.click(fn=ask_and_update_chat, inputs=[question_input, chat_state], outputs=[chatbot, question_input])
    ask_btn.click(fn=lambda history: history, inputs=[chatbot], outputs=[chat_state])  # Update state

demo.launch()