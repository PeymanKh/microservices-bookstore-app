from flask import Flask, jsonify
from utils import get_mongo_client, initialize_bookstore_database
import os

app = Flask(__name__)

@app.route('/')
def initialize_database():
    """Endpoint to initialize the bookstore database."""
    client = get_mongo_client()
    json_file_path = os.path.join(os.path.dirname(__file__), 'bookstore.json')
    message = initialize_bookstore_database(client, json_file_path)
    return jsonify({"message": message})

@app.route('/books', methods=['GET'])
def get_books():
    """Endpoint to retrieve all books."""
    client = get_mongo_client()
    db = client.bookstore
    books = list(db.books.find({}, {'_id': 0}))  # Exclude the `_id` field
    return jsonify(books)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
