# 42Amman AI Chatbot 

This project is an AI-powered chatbot developed during the **42Amman AI Hackathon**. It answers questions about **42Amman** and **Jordan** using **DistilGPT-2** for natural language processing, with a **Flask**-based backend.

##Features

- Provides quick, accurate responses to questions related to **42Amman** and **Jordan**.
- Powered by **DistilGPT-2**, a smaller, faster version of GPT-2.
- Flask-based backend to serve the AI model and handle user interactions.
- Modern, responsive **Frontend** built with **Vanilla JavaScript** for a clean, interactive user experience.

## Getting Started

### Prerequisites

Make sure you have the following installed:
- Python 3.8+
- Flask
- `transformers` library for loading the DistilGPT-2 model
- CSS vanilla (for frontend styling)
- Basic understanding of **Vanilla JavaScript** for frontend functionality

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:MossaJehad/chatbot42Hackthon.git
   ```

2. Navigate into the project directory:
   ```bash
   cd chatbot
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Open your browser and visit `http://localhost:5000` to start chatting with the bot.

## Team

This chatbot was developed by the following team members during the **42Amman AI Hackathon**:

- **Mousa**: Backend development 
- **Omar**: Frontend development
- **Rama**: Research on **DistilGPT-2** and documentation 


## About DistilGPT-2

**DistilGPT-2** is a distilled version of OpenAI's GPT-2 model. It offers a faster, more efficient alternative to the original GPT-2 while still providing impressive language generation capabilities, making it ideal for lightweight AI applications like chatbots.
