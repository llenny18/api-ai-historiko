from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from tavily import TavilyClient
from googletrans import Translator

app = Flask(__name__)

# Enable CORS for all domains or a specific domain
CORS(app, origins="http://localhost:5173/Chat")  # This allows your React app to access the Flask API

# Step 1: Instantiate TavilyClient with your API key
tavily_client = TavilyClient(api_key="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")

@app.route('/api/search', methods=['GET'])
def search_query():
    # Step 2: Get query from URL parameter
    query = request.args.get('query', '')
    if not query:
        return jsonify({"status": "error", "message": "Query is required."})
    
    # Step 3: Execute search query with Tavily API
    response = tavily_client.search(query)

    # Step 4: Initialize Google Translator
    translator = Translator()

    if response['results']:
        result = response['results'][0]  # Get the first result
        # Translate title and content to Tagalog
        title_tagalog = translator.translate(result['title'], src='en', dest='tl').text
        content_tagalog = translator.translate(result['content'], src='en', dest='tl').text
        
        # Step 5: Return the result as a JSON response
        return jsonify({
            "title": title_tagalog,
            "url": result['url'],
            "content": content_tagalog[:150],  # Limiting snippet length
            "score": result['score']
        })
    else:
        return jsonify({"status": "error", "message": "No results found."})

if __name__ == '__main__':
    app.run(debug=True)
