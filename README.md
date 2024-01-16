# Library

This is a simple library management system implemented using Flask, SQLAlchemy, and JWT for authentication.

## Getting Started

### Prerequisites

Make sure you have [Python](https://www.python.org/) installed on your machine.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/library.git
    ```

2. Navigate to the project directory:

    ```bash
    cd library
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

- Configure the database URI and JWT secret key in the `app.config` of `app.py`:

    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    ```

## Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Use the provided endpoints:

    - To generate a JWT token:

        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"secret_key": "your_secret_key"}' http://localhost:5000/generate_token
        ```

    - To fetch book details by ISBN:

        ```bash
        curl http://localhost:5000/isbn/9780132350884
        ```

    - To get a list of books (requires JWT token):

        ```bash
        curl -H "Authorization: Bearer your_access_token" http://localhost:5000/books
        ```

    - To add a new book (requires JWT token):

        ```bash
        curl -X POST -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{"isbn": "9780132350884", "author": "Author Name", "title": "Book Title", "summary": "Book Summary", "cover_url": "http://example.com/cover.jpg"}' http://localhost:5000/books
        ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
