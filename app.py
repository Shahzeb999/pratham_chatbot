import logging
from flask import Flask, request, jsonify, render_template
import openai
from scraper.scrape import scrape_pratham
import os
from dotenv import load_dotenv


# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY')

# Scrape the website when the server starts
try:
    logging.debug("Starting to scrape Pratham website...")
    knowledge_base = scrape_pratham()
    logging.debug(f"Scraped knowledge base: {knowledge_base}")
except Exception as e:
    logging.error(f"Error during scraping: {e}")
    knowledge_base = {}

def generate_response(question):
    try:
        logging.debug(f"Received question: {question}")

        # Format the knowledge base content for the prompt
        knowledge_base_content = " ".join(
            f"{key}: {content}" for key, content in knowledge_base.items()
        )
        
        if not knowledge_base_content:
            raise ValueError("Knowledge base content is empty.")

        # Use the latest OpenAI API method to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{knowledge_base_content}\n\nQuestion: {question}"},
            ]
        )
        answer = response['choices'][0]['message']['content'].strip()
        logging.debug(f"Generated response: {answer}")
        return answer
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "I'm sorry, I couldn't process your request."

@app.route('/')
def home():
    logging.debug("Rendering home page")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        question = data.get('question', '')
        logging.debug(f"Question from user: {question}")

        # Generate a response from the knowledge base or AI model
        response_text = generate_response(question)

        return jsonify({'answer': response_text})
    except Exception as e:
        logging.error(f"Error in ask route: {e}")
        return jsonify({'answer': "Sorry, something went wrong."})

if __name__ == '__main__':
    app.run(debug=True)
