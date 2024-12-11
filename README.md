# Microservices Bookstore Application

This project is a microservices-based bookstore application. The application consists of a Flask-based REST API that interacts with a MongoDB database. The MongoDB database is deployed as a StatefulSet on Kubernetes, and the Flask app is a Docker container running within the same Kubernetes cluster.

# Features
* Perform CRUD operations on books via REST API endpoints.
* MongoDB for persistent data storage.
* Dockerized environment for seamless deployment.
* Kubernetes manifests for cloud-native deployment.

# Technologies Used
* Flask: For building the REST API.
* MongoDB: As the database backend.
* Docker: For containerization of the application.
* Kubernetes: For orchestration and deployment.

# Setup Instructions
Ensure the following tools are installed on your system:
* [Python 3.x](https://www.python.org/downloads/)
* [Docker](https://www.docker.com/get-started/)
* [Kubernetes (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Minikube](https://minikube.sigs.k8s.io/docs/start/)
* [MongoDB Shell](https://www.mongodb.com/try/download/shell)

# Project Structure
This section outlines the folder and file organization of the microservices-based bookstore application. The structure includes:
```bash
microservices-bookstore-app/
├── app/
│   ├── __init__.py          # Initialize Flask app
│   ├── app.py               # Flask app with CRUD routes
│   ├── utils.py             # MongoDB connection and helper functions
│   ├── bookstore.json       # Initial data for the database
│   ├── Dockerfile           # Dockerfile for the Flask app
│   └── requirements.txt     # Python dependencies
├── k8s/
│   ├── mongodb-statefulset.yaml          # StatefulSet for MongoDB
│   ├── flask-deployment.yaml             # Deployment for Flask app
│   ├── flask-service.yaml                # Service for Flask app
│   └── mongodb-service.yaml              # Service for MongoDB
├── README.md           # Documentation
└── .gitignore          # Ignore unnecessary files
```

# Application Workflow
### A. Initializing the Database
- MongoDB is deployed as a StatefulSet in the Kubernetes cluster, with a dedicated service for connectivity.
- Authentication is enabled, using credentials (`admin:admin`) for secure access.
- The database is populated with initial data from the `bookstore.json` file during setup.

### B. API Operations
- The Flask application acts as the gateway for managing the bookstore's data, providing endpoints for CRUD operations.  
- Each endpoint is designed to handle a specific operation, such as retrieving, adding, updating, or deleting books in the database.

### C. Deployment and Access
- The Flask app is containerized using Docker and deployed on Kubernetes.
- The application is exposed via NodePort for external access.

### D. Integration
- The Flask app interacts with MongoDB using the credentials and connection string configured via environment variables.

# Steps to Run the Application
### 1. Clone the Repository
Start by cloning the project repository from GitHub:
```bash
git clone https://github.com/PeymanKh/microservices-bookstore-app.git
cd microservices-bookstore-app
```

### 2. Set Up MongoDB
a. Deploy MongoDB on Kubernetes:
```bash
kubectl apply -f k8s/mongodb-statefulset.yaml
kubectl apply -f k8s/mongodb-service.yaml
```

b. Access the MongoDB pod:
```bash
kubectl exec -it mongodb-0 -- mongosh
```

c. Switch to the `admin` database:
```bash
use admin
```

d. Create an admin user:
```bash
db.createUser({
    user: "admin",
    pwd: "admin",
    roles: [{ role: "root", db: "admin" }]
})
```

e. Exit the shell:
```bash
exit
```

### 3. Run the Flask Application
a. Build the Docker image:
```bash
cd app
docker build -t flask-app .
```

b. Run the containerized Flask application:
```bash
docker run --rm -p 5002:5000 -e MONGO_HOST=host.docker.internal -e MONGO_USER=admin -e MONGO_PASSWORD=admin flask-app
```
Explanation of the Command:
* `docker run`: Executes a new Docker container.
* `--rm`: Automatically removes the container when it stops to avoid clutter.
* `-p 5002:5000`: Maps port `5000` inside the container to port `5002` on the host machine, allowing access to the application via `http://localhost:5002`.
* `-e MONGO_HOST=host.docker.internal`: Sets the `MONGO_HOST` environment variable inside the container to `host.docker.internal`. This ensures the Flask app can locate the MongoDB host when MongoDB is running on the host machine.
* `-e MONGO_USER=admin`: Sets the `MONGO_USE`R environment variable to `admin`, used for authenticating with MongoDB.
* `-e MONGO_PASSWORD=admin`: Sets the `MONGO_PASSWORD` environment variable to `admin`, used for authenticating with MongoDB.
* `flask-app`: Specifies the name of the Docker image to run.

c. Open your browser and access the application:
```bash
http://localhost:5002/
```

You also have the option to deploy the application on Kubernetes for a scalable and containerized environment.

# API Endpoints
**URL**: `/`

**Description**: Initializes the bookstore database with the contents of `bookstore.json`.

**CRUD Operation**: Creates the database and its initial collections if they don’t exist.

---

**URL**: `/books`

**Method**: `GET`

**Description**: Retrieves all books in the database.

**CRUD Operation**: Reads data from the `books` collection in MongoDB.

---

**URL**: `/books`

**Method**: `POST`

**Request Body**: 
```bash
{
  "isbn": "1234567890",
  "title": "New Book",
  "author": "Author Name",
  "year": 2024,
  ...
}
```

**Description**: Adds a new book to the database.

**CRUD Operation**: Inserts a new document into the `books` collection.

---

**URL**: `/books/<isbn>`

**Method**: `PUT`

**Request Body**: 
```bash
{
  "title": "Updated Title",
  ...
}
```

**Description**: Updates an existing book identified by its ISBN.

**CRUD Operation**: Modifies an existing document in the `books` collection.

---

**URL**: `/books/<isbn>`

**Method**: `DELETE`

**Description**: Deletes a book identified by its ISBN.

**CRUD Operation**: Removes a document from the `books` collection.

# Testing the application 
### Using Browser:
* Visit `http://localhost:5002/` to initialize the database.

* Visit `http://localhost:5002/books` to retrieve all books.

### Using `curl`
* Add a book:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"isbn": "1234567890", "title": "Book Title", "author": "Author Name", "year": 2024}' \
http://127.0.0.1:5002/books
```

* Update a book:
```bash
curl -X PUT -H "Content-Type: application/json" \
-d '{"title": "Updated Title"}' \
http://127.0.0.1:5002/books/1234567890
```

* Delete a book
```bash
curl -X DELETE http://127.0.0.1:5002/books/1234567890
```

# Author
**Peyman Kh**

*Email*: [Peymankhodabandehlouei@gmail.com](mailto:Peymankhodabandehlouei@gmail.com)


