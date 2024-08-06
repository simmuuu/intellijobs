from query import search_jobs
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/')
def home():
    return 'Home route'

@app.route('/job-search', methods=['POST'])
def llm_response():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'Invalid input, missing query'}), 400

    response = search_jobs(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)