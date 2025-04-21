# MAAP Loader Service

MongoDB AI Applications Program (MAAP) Loader is a service that processes documents from files and web pages, generates embeddings using AWS Bedrock, and stores them in MongoDB Atlas Vector Search for AI-powered applications.

## Features

- Upload and process various document formats
- Load and process web pages
- Generate embeddings using AWS Bedrock
- Store documents and embeddings in MongoDB Atlas
- Clean, modular design with clear separation of concerns
- FastAPI-based REST API with automatic OpenAPI documentation

## Project Structure

```bash
├── main.py                  # FastAPI app initialization and API routes
├── config.py                # Configuration variables and constants
├── database/
│   ├── __init__.py
│   └── mongodb.py           # MongoDB connection and initialization
├── services/
│   ├── __init__.py
│   ├── bedrock_service.py   # AWS Bedrock integration
│   ├── document_service.py  # Document processing service
│   └── embedding_service.py # Embedding generation and vector operations
├── utils/
│   ├── __init__.py
│   ├── error_utils.py       # Error handling utilities
│   ├── file_utils.py        # File handling utilities
│   └── logger.py            # Logging utilities
└── models/
    ├── __init__.py
    └── pydantic_models.py   # Pydantic models for requests/responses
```

## Setup

### Prerequisites

- Python 3.10+
- MongoDB Atlas account with Vector Search enabled
- AWS account with access to Bedrock

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Application settings
DEBUG=true
SERVICE_HOST=0.0.0.0
SERVICE_PORT=8001
LOGGER_SERVICE_URL=http://0.0.0.0:8181

# AWS configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
EMBEDDING_MODEL_ID=amazon.titan-embed-text-v1

# Other settings (see .env file for full list)
```

### MongoDB Atlas Setup

1. Create a MongoDB Atlas cluster
2. Create a database and collection for your documents
3. Set up a Vector Search index on your collection
   - Index name should match the `index_name` parameter
   - Vector field should match the `embedding_field` parameter
   - Vector dimension should be 1536 (for Amazon Titan embeddings)

### Installation

#### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run with Docker directly
docker build -t maap-loader .
docker run -p 8001:8001 --env-file .env maap-loader
```

#### Local Development

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## API Usage

### Upload Endpoint

`POST /upload`

This endpoint accepts:
- Files via multipart form data
- JSON configuration parameters

Example request using curl:

```bash
curl -X POST "http://localhost:8001/upload" \
  -F "files=@document.pdf" \
  -F 'json_input_params={
    "user_id": "user123",
    "mongodb_config": {
      "uri": "mongodb+srv://username:password@cluster.mongodb.net/",
      "database": "documents_db",
      "collection": "embeddings",
      "index_name": "vector_index",
      "text_field": "text",
      "embedding_field": "embedding"
    },
    "web_pages": ["https://example.com"]
  }'
```

### API Documentation

FastAPI automatically generates interactive documentation:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## License

[MIT License](LICENSE)
```

## .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
venv/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Project specific
files/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# Logs
*.log
logs/
```

## API Test Guide

Create a file called `api_test.md` with the following content:

```markdown
# MAAP Loader API Testing Guide

This guide provides examples for testing the MAAP Loader API.

## Health Check

```bash
curl -X GET "http://localhost:8001/health"
```

## Upload Files with Web URLs

```bash
curl -X POST "http://localhost:8001/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@path/to/document.pdf" \
  -F 'json_input_params={
    "user_id": "testuser123",
    "mongodb_config": {
      "uri": "mongodb+srv://username:password@cluster.mongodb.net/",
      "database": "documents_db",
      "collection": "embeddings",
      "index_name": "vector_index",
      "text_field": "text",
      "embedding_field": "embedding"
    },
    "web_pages": ["https://www.mongodb.com/", "https://aws.amazon.com/bedrock/"]
  }'
```

## Upload Only Files

```bash
curl -X POST "http://localhost:8001/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@path/to/document1.pdf" \
  -F "files=@path/to/document2.docx" \
  -F 'json_input_params={
    "user_id": "testuser123",
    "mongodb_config": {
      "uri": "mongodb+srv://username:password@cluster.mongodb.net/",
      "database": "documents_db",
      "collection": "embeddings",
      "index_name": "vector_index"
    },
    "web_pages": []
  }'
```

## Upload Only Web Pages

```bash
curl -X POST "http://localhost:8001/upload" \
  -H "Content-Type: multipart/form-data" \
  -F 'json_input_params={
    "user_id": "testuser123",
    "mongodb_config": {
      "uri": "mongodb+srv://username:password@cluster.mongodb.net/",
      "database": "documents_db",
      "collection": "embeddings",
      "index_name": "vector_index"
    },
    "web_pages": [
      "https://www.mongodb.com/", 
      "https://aws.amazon.com/bedrock/"
    ]
  }'
```

## Testing with Python

```python
import requests
import json

url = "http://localhost:8001/upload"

# Prepare files
files = [
    ('files', ('document.pdf', open('path/to/document.pdf', 'rb'), 'application/pdf'))
]

# Prepare JSON parameters
params = {
    "user_id": "testuser123",
    "mongodb_config": {
        "uri": "mongodb+srv://username:password@cluster.mongodb.net/",
        "database": "documents_db",
        "collection": "embeddings",
        "index_name": "vector_index"
    },
    "web_pages": ["https://www.mongodb.com/"]
}

# Create form data
data = {
    'json_input_params': json.dumps(params)
}

# Send request
response = requests.post(url, files=files, data=data)

# Print response
print(response.status_code)
print(response.json())
```
```

These files provide a comprehensive setup for your MAAP Loader application, including Docker containerization, environment variables, documentation, and testing examples.