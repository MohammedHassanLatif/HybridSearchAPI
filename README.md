# Hybrid Search API

## Overview

The Hybrid Search API is designed to perform efficient searches across a dataset of 1 million magazine records. This API combines traditional keyword-based searches with vector-based searches to provide highly relevant results. The data model consists of two tables: one for the main magazine information and another for the magazine content.

## Features

- **Hybrid Search Endpoint**: A single API endpoint that combines keyword-based search with vector-based search.
- **Keyword Search**: Search by keywords in the title, author, and content of magazines.
- **Vector Search**: Search based on vector similarity in the `vector_representation` field.
- **Optimized for Performance**: Efficiently handles large datasets with appropriate indexing strategies and database optimizations.

## Data Model

### Table 1: Magazine Information

Stores the primary information about each magazine.

- `id`: Unique identifier for the magazine.
- `title`: Title of the magazine.
- `author`: Author of the magazine.
- `publication_date`: Date when the magazine was published.
- `category`: Category of the magazine (e.g., Science, Technology, Lifestyle).

### Table 2: Magazine Content

Stores the detailed content of each magazine, including vector representations for search.

- `id`: Unique identifier for the magazine content.
- `magazine_id`: Foreign key linking to the Magazine Information table.
- `content`: Full text content of the magazine.
- `vector_representation`: Array of numbers representing the vector embedding of the content.

## Technology Stack

- **Backend**: Node.js v18 or greater (using Express framework).
- **Database**: A suitable database such as PostgreSQL, Elasticsearch, or ChromaDB, supporting vector searches.

## Getting Started

### Prerequisites

- **Node.js**: Ensure you have Node.js v18 or greater installed on your machine.
- **Database**: Set up a suitable database (e.g., PostgreSQL, Elasticsearch, ChromaDB) that supports vector searches. Make sure the database server is running and accessible.

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/HybridSearchAPI.git
   cd HybridSearchAPI

2. **Install Dependencies**:
   ```bash
    npm install

3. **Configure Database**:

Edit the .env file to add your database connection details. Ensure the database schema is set up correctly using the provided SQL scripts or ORM models.

4. **Run the API**:
   ```bash
    npm start
   
The API will start on http://localhost:3000 (or the configured port).

### Example Search Queries
Keyword Search
curl -X GET "http://localhost:3000/search?query=technology"

Expected Result: Returns a list of magazines matching the keyword "technology" in the title, author, or content.

### Vector Search
curl -X POST "http://localhost:3000/search/vector" -H "Content-Type: application/json" -d '{"vector": [0.1, 0.2, ...]}'

Expected Result: Returns a list of magazines with content vectors similar to the provided vector.

### Hybrid Search
curl -X POST "http://localhost:3000/search/hybrid" -H "Content-Type: application/json" -d '{"query": "technology", "vector": [0.1, 0.2, ...]}'

Expected Result: Combines both keyword and vector searches to return the most relevant results.

### Performance Considerations
Indexing: Proper indexing on the title, author, and vector_representation fields to optimize search performance.
Database Optimizations: Utilize database-specific features like full-text search and vector indexes (if supported) for efficient querying.

### Deliverables
Source Code: Complete source code of the API.
Database Schema: SQL scripts or ORM models for creating the database tables.
Documentation: Detailed documentation on setting up and running the API, including usage examples.
Performance Report: A brief report on performance considerations and optimizations implemented.

### Evaluation Criteria
Functionality: API should meet all specified requirements.
Code Quality: Code should be clean, readable, and well-documented.
Performance: Efficient handling of large datasets is crucial.
Innovation: Creative solutions for hybrid search implementation are valued.
Documentation: Clear and comprehensive documentation is essential.

### Timeline
This task is to be completed within 7 days.
