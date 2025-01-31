# Library Management API

## Introduction
This Library Management API is a RESTful API for managing a library's book collection. It allows users to add, update, delete, and retrieve books.

## Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/F0laf0lu/library-api
    cd library-api
    ```

2. Install dependencies:
    ```bash
    pip install requirements.txt
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory and add the following variables:
    ```env
    SECRET_KEY=your_secret_key
    ```
    
## Running the Application
To start the application, run:
```bash
python manage.py runserver
```
The server will start on the port 8000.

## API Endpoints

### Add a Book
- **URL:** `/api/v1/books/`
- **Method:** `POST`
- **Body:**
    ```json
    {
        "title": "Book Title",
        "author": "Author Name",
        "genre": "Genre",
        "publication_date": "YYYY-MM-DD",
        "edition": "Edition",
        "summary": "Book Summary"
    }
    ```
- **Response:**
    ```json
    {
        "status": "success",
        "code": 201,
        "message": "Book added successfully",
        "data": {
            "id": "BOOK-id",
            "title": "Book Title",
            "author": "Author Name",
            "genre": "Genre",
            "publication_date": "YYYY-MM-DD",
            "edition": "Edition",
            "summary": "Book Summary",
        }
    }
    ```

### Get a Book by ID
- **URL:** `/api/v1/books/:bookId/`
- **Method:** `GET`
- **Response:**
    ```json
    {
        "status": "success",
        "code": 200,
        "message": "Book details retrieved successfully.",
        "data": {
            "id": "BOOK-id",
            "title": "Book Title",
            "author": "Author Name",
            "genre": "Genre",
            "publication_date": "YYYY-MM-DD",
            "edition": "Edition",
            "summary": "Book Summary",
            "available": "available",
        }
    }
    ```

### Get All Books
- **URL:** `/api/v1/books/`
- **Method:** `GET`
- **Response:**
    ```json
    {
        "status": "success",
        "code": 200,
        "message": "Books retrieved successfully.",
        "count": 4,
        "data": [
            {
                "id": "BOOK-uuid1",
                "title": "Book Title 1",
                "author": "Author Name 1",
                "genre": "Genre 1",
                "publication_date": "YYYY-MM-DD",
                "edition": "Edition 1",
                "summary": "Book Summary 1",
                "available": "available",
            },
            {
                "id": "BOOK-id",
                "title": "Book Title 2",
                "author": "Author Name 2",
                "genre": "Genre 2",
                "publication_date": "YYYY-MM-DD",
                "edition": "Edition 2",
                "summary": "Book Summary 2",
                "available": "not available",
            }
        ],
        "pagination": {
            "current_Page": 2,
            "per_page": 10,
        }
    }
    ```

### Update a Book
- **URL:** `/api/v1/books/:bookId/`
- **Method:** `PUT`
- **Body:**
    ```json
    {
        "title": "Updated Book Title",
        "author": "Updated Author Name",
        "genre": "Updated Genre",
        "publication_date": "YYYY-MM-DD",
        "edition": "Updated Edition",
        "summary": "Updated Book Summary",
        "available": "available",

    }
    ```
- **Response:**
    ```json
    {
        "status": "success",
        "code": 200,
        "message": "Book updated successfully",
        "data": {
            "id": "BOOK-id",
            "title": "Updated Book Title",
            "author": "Updated Author Name",
            "genre": "Updated Genre",
            "publication_date": "YYYY-MM-DD",
            "edition": "Updated Edition",
            "summary": "Updated Book Summary",
            "available": "available"
        }
    }
    ```

### Delete a Book
- **URL:** `/api/v1/books/:bookId`
- **Method:** `DELETE`
- **Response:**
    ```json
    {
        "status": "success",
        "code": 200,
        "message": "Book deleted successfully"
    }
    ```

## Rate Limiting
The API has rate limiting enabled user django throttling to prevent abuse. The rate limiter is configured to allow a certain number of requests per minute. If the limit is exceeded, the API will respond with a `429 Too Many Requests` status. Current rate is set to 10requests per second for anon users


## Pagination
The API supports pagination for endpoints that return multiple items. This helps to manage large sets of data by dividing them into pages.

### Pagination Parameters
- **page:** The page number to retrieve (default is 1).
- **page_size:** The number of items per page (default is 10).

### Example Request
To retrieve the second page with 5 items per page:
```http
GET /api/v1/books?page=2&page_size=10
```

### Example Response
```json
{
    "status": "success",
    "code": 200,
    "message": "Books retrieved successfully.",
    "data": [
        {
            "id": 1,
            "title": "Book Title 6",
            "author": "Author Name 6",
            "genre": "Genre 6",
            "publicationDate": "YYYY-MM-DD",
            "edition": "Edition 6",
            "summary": "Book Summary 6",
            "available": "available",
        },
        {
            "id": 2,
            "title": "Book Title 7",
            "author": "Author Name 7",
            "genre": "Genre 7",
            "publicationDate": "YYYY-MM-DD",
            "edition": "Edition 7",
            "summary": "Book Summary 7",
            "available": "not available",
        }
    ],
    "pagination": {
        "current_Page": 2,
        "per_page": 10,
    },
}
```
