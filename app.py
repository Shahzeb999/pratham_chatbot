from flask import Flask, request, jsonify, render_template, session
import logging
from ai.database_update import update_vector_database
from ai.rag_cot import process_query_with_chain_of_thought
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Global variable for the index
index = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update_embeddings', methods=['POST'])
def update_embeddings():
    global index
    try:
        data = request.json
        url = data['url']

        # Validate input
        if not url:
            raise ValueError("URL must be provided")

        index = update_vector_database(url)
        return jsonify({'status': 'success', 'message': 'Index updated successfully'}), 200
    except Exception as e:
        logging.error(f"Error updating embeddings: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/process_query', methods=['POST'])
def process_query():
    global index
    try:
        data = request.json
        user_query = data['query']

        # Validate input
        if not user_query:
            raise ValueError("User query must be provided")

        if index is None:
            raise ValueError("Index is not initialized. Update embeddings first.")

        # Retrieve the previous context from the session
        previous_context = session.get('conversation_context', '')

        # Process the query with chain of thought
        response = process_query_with_chain_of_thought(user_query, previous_context, index)

        # Update the session with the new context
        session['conversation_context'] = previous_context + f"\nUser: {user_query}\nBot: {response}\n"

        return jsonify({'response': response}), 200
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

