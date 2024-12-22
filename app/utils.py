"""
Module for managing MongoDB connections and initializing the bookstore database.

This module provides functionality to connect to a MongoDB instance using
environment variables and to initialize a bookstore database with data
from a JSON file.

Author: Peyman Kh
Date: 2024-12-11
"""


# Import libraries
import os
import json
from pymongo import MongoClient


def get_mongo_client():
    """Establish a connection to the MongoDB instance."""
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_port = os.getenv("MONGO_PORT", "27017")
    mongo_user = os.getenv("MONGO_USER", "admin")
    mongo_password = os.getenv("MONGO_PASSWORD", "admin")
    connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
    return MongoClient(connection_string)

def initialize_bookstore_database(client, json_file_path):
    """Drop the bookstore database and reinitialize it with data from the JSON file."""
    db = client.bookstore
    db.books.drop()  # Drop the existing books collection
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        db.books.insert_many(data)  # Insert data into the books collection
    return "Database initialized successfully"
