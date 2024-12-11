"""
Flask application for managing a bookstore.

This application provides RESTful endpoints for CRUD operations on a bookstore database.
The database is powered by MongoDB, and the application integrates with it using utility
functions for connection and initialization.

Endpoints:
- `/` [GET]: Initializes the bookstore database with data from a JSON file.
- `/books` [GET]: Retrieves all books in the database.
- `/books` [POST]: Adds a new book to the database.
- `/books/<isbn>` [PUT]: Updates an existing book's details by its ISBN.
- `/books/<isbn>` [DELETE]: Deletes a book by its ISBN.

Author: Peyman Kh
Date: 2024-12-11
"""


# Import libraries
from flask import Flask, jsonify, request
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

@app.route('/books', methods=['POST'])
def create_book():
    """Endpoint to create a new book."""
    client = get_mongo_client()
    db = client.bookstore
    book_data = request.json

    if not book_data or 'isbn' not in book_data:
        return jsonify({"error": "Invalid data or missing 'isbn'"}), 400

    # Insert the book into the collection
    db.books.insert_one(book_data)
    return jsonify({"message": "Book added successfully!"}), 201

@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    """Endpoint to update a book by its ISBN."""
    client = get_mongo_client()
    db = client.bookstore
    updated_data = request.json

    if not updated_data:
        return jsonify({"error": "No data provided for update"}), 400

    # Update the book with the given ISBN
    result = db.books.update_one({"isbn": isbn}, {"$set": updated_data})

    if result.matched_count == 0:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book updated successfully!"})

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """Endpoint to delete a book by its ISBN."""
    client = get_mongo_client()
    db = client.bookstore

    # Delete the book with the given ISBN
    result = db.books.delete_one({"isbn": isbn})

    if result.deleted_count == 0:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book deleted successfully!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
