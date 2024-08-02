
import os
from flask import Flask, request, jsonify
from ai.scraper import PrathamScraper, create_knowledge_base
from ai.rag_cot import process_query_with_chain_of_thought

app = Flask(__name__)

# Initialize the scraper and knowledge base
scraper = PrathamScraper('https://www.pratham.org/')
knowledge_base = create_knowledge_base(scraper)

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query', '')
    if not user_query:
        return jsonify({'error': 'Query is required'}), 400

    # Use the knowledge base to answer the query
    previous_context = ' '.join(knowledge_base.values())
    response = process_query_with_chain_of_thought(user_query, previous_context, None)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
