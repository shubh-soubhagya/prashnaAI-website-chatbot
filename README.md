# YouTube Transcript ChatBot

**PrashnaAI Website Chatbot** is an intelligent tool that lets users input any website URL and instantly chat with its content. It supports real-time Q&A, content summarization, and downloading in .txt format. Ideal for students, researchers, analysts, and professionals needing fast insights from blogs, articles, documentation, or knowledge bases.

---

## 🚀 Features

- **AI-Powered Question Answering**: Get precise answers based on YouTube video transcripts.
- **Interactive Web-Based Interface**: Easy-to-use UI for seamless interactions.
- **Chat History Navigation**: Browse previous queries for improved research efficiency.
- **Transcript Download**: Extract and save video transcripts for offline reference.
- **Ideal for Researchers & Professionals**: Quickly analyze lectures, tutorials, and discussions.

## 🖥️ Usage

1. Enter the YouTube video URL.
2. Ask a specific question related to the video content.
3. Get AI-driven responses based on the transcript.
4. Download the transcript for further analysis if needed

---

## Website Demo

![Website UI](assets/demo.png)


## 📦 Custom Packages
- **`transcript_extractor`**: Extracts and preprocesses YouTube video transcripts efficiently.
- **`transcriptQA`**: Enables AI-driven question-answering functionality using the `llama3-70b-8192` model via the Groq inference API.

## 🛠 Installation & Setup

Follow these steps to set up and run the YouTube Support ChatBot on your local machine:

#### 1️⃣ Install Dependencies
Run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

#### 2️⃣ Configure the `.env` File
Create a `.env` file inside the project directory (`YouTube-support-chatbot/.env`) and add your Groq API key:
```ini
GROQ_API_KEY=<your-api-key>
```

#### 3️⃣ Generate API Key
Obtain your Groq API key by visiting [Groq Console](https://console.groq.com/keys) and copying your key.

#### 4️⃣ Run the Application
Start the chatbot by executing the following command:
```bash
python app.py
```
Then, open your browser and navigate to `http://127.0.0.1:5000` to interact with the chatbot.

---

## 💡 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## 📩 Contact
For any queries, reach out via [soubhagyasrivastava240@gmail.com](mailto:soubhagyasrivastava240@gmail.com).

---
*Developed with ❤️ for seamless YouTube content analysis.*
