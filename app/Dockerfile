# Dockerfile
# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Set environment variables for MongoDB connection
ENV MONGO_HOST=mongodb
ENV MONGO_PORT=27017
ENV MONGO_USER=admin
ENV MONGO_PASSWORD=admin

# Expose the port for Flask
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
