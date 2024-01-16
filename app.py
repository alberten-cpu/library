from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Create a Flask application
app = Flask(__name__)

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

# Configure Flask app with a secret key for JWT
app.config['SECRET_KEY'] = 'albert'

# Initialize JWTManager with the Flask app
jwt = JWTManager(app)

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)


# Define a Book model for the database
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    cover_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Boolean, default=True)


# Function for validating ISBN
def validate_isbn(isbn):
    return len(isbn) == 13 and isbn.isdigit()


# Function for fetching book details from the database
def fetch_book_details(isbn):
    book = Book.query.filter_by(isbn=isbn).first()

    if book:
        book_list = [
            {
                'id': book.id,
                'isbn': book.isbn,
                'author': book.author,
                'title': book.title,
                'summary': book.summary,
                'cover_url': book.cover_url,
                'status': book.status
            }
        ]
        return book_list
    else:
        return {'error': 'Book not found'}


# Route for generating a JWT token
@app.route('/generate_token', methods=['POST'])
def generate_token():
    provided_secret_key = request.json.get('secret_key', None)

    # Fetching configured secret key
    env_secret_key = app.config.get('SECRET_KEY')

    # Check if the provided key matches the environment key
    if provided_secret_key != env_secret_key:
        return jsonify({'error': 'Invalid secret key'}), 401

    # If the keys match, proceed to generate the token
    token_input = {'project': 'library'}
    access_token = create_access_token(identity=token_input)
    return jsonify(access_token=access_token)


# Route for fetching book details by ISBN
@app.route('/isbn/<isbn>', methods=['GET'])
def fetch_book_by_isbn(isbn):
    # Validating ISBN format
    if not validate_isbn(isbn):
        return {'error': 'Invalid ISBN format'}, 400

    # Fetching book details from the database
    book_details = fetch_book_details(isbn)

    if book_details:
        return {'book_details': book_details}
    else:
        return {'error': 'Book details not found'}, 404


# Route for handling books with JWT token required
@app.route('/books', methods=['GET', 'POST'])
@jwt_required()
def handle_books():
    if request.method == 'GET':
        # Fetching all books from the database
        books = Book.query.all()

        # Creating a list of book details for the response
        book_list = [
            {
                'id': book.id,
                'isbn': book.isbn,
                'author': book.author,
                'title': book.title,
                'summary': book.summary,
                'cover_url': book.cover_url,
                'status': book.status
            }
            for book in books
        ]

        return jsonify({'books': book_list})
    elif request.method == 'POST':
        data = request.json
        isbn = data.get('isbn')

        # Validating ISBN format
        if not isbn or not validate_isbn(isbn):
            return {'error': 'Invalid ISBN format'}, 400

        # Checking if a book with the same ISBN already exists
        existing_book = Book.query.filter_by(isbn=isbn).first()

        if existing_book:
            return {'message': 'Book with the same ISBN already exists'}
        else:
            # Creating a new book and saving it to the database
            new_book = Book(
                isbn=isbn,
                author=data.get('author'),
                title=data.get('title'),
                summary=data.get('summary'),
                cover_url=data.get('cover_url')
            )
            db.session.add(new_book)
            db.session.commit()
            return {'message': 'Book details saved successfully'}


# Entry point of the application
if __name__ == '__main__':
    # Creating the database tables if they don't exist
    with app.app_context():
        db.create_all()
    # Running the Flask application in debug mode
    app.run(debug=True)
