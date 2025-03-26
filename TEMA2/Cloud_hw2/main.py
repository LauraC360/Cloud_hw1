# from flask import Flask, render_template, jsonify, request
# from flask_cors import CORS
# import requests
# import os
# import logging
#
# from config import SERVICE1_URL, GOOGLE_BOOKS_API_KEY
#
# app = Flask(__name__)
# CORS(app)
#
# # Load configuration from config.py
# app.config.from_pyfile('config.py')
#
# SERVICE1_URL = app.config['SERVICE1_URL']
#
# # @app.route('/books', methods=['GET', 'POST'])
# # @app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
# # @app.route('/books/author/<author_name>', methods=['GET', 'DELETE'])
# # @app.route('/books/history/<int:book_id>', methods=['GET'])
# # def handle_books(book_id=None, author_name=None):
# #     try:
# #         if request.method == 'GET':
# #             if book_id:
# #                 response = requests.get(f'http://localhost:8000/books/{book_id}')
# #             elif author_name:
# #                 response = requests.get(f'http://localhost:8000/books/author/{author_name}')
# #             elif 'history' in request.path:
# #                 response = requests.get(f'http://localhost:8000/books/history/{book_id}')
# #             else:
# #                 response = requests.get('http://localhost:8000/books')
# #         elif request.method == 'POST':
# #             response = requests.post('http://localhost:8000/books', json=request.json)
# #         elif request.method == 'PUT':
# #             response = requests.put(f'http://localhost:8000/books/{book_id}', json=request.json)
# #         elif request.method == 'DELETE':
# #             if author_name:
# #                 response = requests.delete(f'http://localhost:8000/books/author/{author_name}')
# #             else:
# #                 response = requests.delete(f'http://localhost:8000/books/{book_id}')
# #         response.raise_for_status()
# #         return jsonify(response.json())
# #     except requests.exceptions.RequestException as e:
# #         return jsonify({'error': str(e)}), 500
#
# @app.route('/books', methods=['GET', 'POST'])
# def books():
#     try:
#         if request.method == 'GET':
#             response = requests.get(f'{SERVICE1_URL}/books')
#         else:  # POST
#             response = requests.post(f'{SERVICE1_URL}/books', json=request.json)
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500
#
# @app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
# def book_by_id(book_id):
#     try:
#         if request.method == 'GET':
#             response = requests.get(f'{SERVICE1_URL}/books/{book_id}')
#         elif request.method == 'PUT':
#             response = requests.put(f'{SERVICE1_URL}/books/{book_id}', json=request.json)
#         else:  # DELETE
#             response = requests.delete(f'{SERVICE1_URL}/books/{book_id}')
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500
#
# @app.route('/books/author/<author_name>', methods=['GET', 'DELETE'])
# def books_by_author(author_name):
#     try:
#         if request.method == 'GET':
#             response = requests.get(f'{SERVICE1_URL}/books/author/{author_name}')
#         else:  # DELETE
#             custom_header = request.headers.get('X-CUSTOM-HEADER')
#             if custom_header != app.config['AUTH_HEADER']:
#                 return jsonify({'error': 'Unauthorized'}), 401
#             response = requests.delete(f'{SERVICE1_URL}/books/author/{author_name}')
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500
#
# @app.route('/books/history/<int:book_id>', methods=['GET'])
# def book_history(book_id):
#     try:
#         response = requests.get(f'{SERVICE1_URL}/books/history/{book_id}')
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500
#
# @app.route('/books/batch', methods=['POST', 'PUT'])
# def batch_books():
#     try:
#         if request.method == 'POST':
#             response = requests.post(f'{SERVICE1_URL}/books/batch', json=request.json)
#         elif request.method == 'PUT':
#             response = requests.put(f'{SERVICE1_URL}/books/batch', json=request.json)
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500
#
# @app.route('/books/<int:book_id>/title', methods=['PATCH'])
# def update_book_title(book_id):
#     try:
#         response = requests.patch(f'{SERVICE1_URL}/books/{book_id}/title', json=request.json)
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500
#
# @app.route('/books/<int:book_id>/author', methods=['PATCH'])
# def update_book_author(book_id):
#     try:
#         response = requests.patch(f'{SERVICE1_URL}/books/{book_id}/author', json=request.json)
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500
#
# @app.route('/books/googlebooks')
# @app.route('/books/googlebooks', methods=['GET'])
# def google_books_search_volume():
#     # Get search query from request parameters
#     query = request.args.get('q')
#
#     # Define the API URL
#     base_url = "https://www.googleapis.com/books/v1/volumes"
#
#     # Define request parameters
#     params = {
#         'q': query,
#         'key': os.getenv('GOOGLE_BOOKS_API_KEY')
#     }
#
#     #print(f"Google Books API Key: {GOOGLE_BOOKS_API_KEY}")
#
#     try:
#         # Send request to Google Books API
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()  # Raises an error if the request fails
#
#         # Return JSON response
#         return jsonify(response.json())
#
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': f'Failed to fetch books from Google API: {str(e)}'}), 500
#
# @app.route('/books/googlebooks/<volume_id>', methods=['GET'])
# def google_books_volume(volume_id):
#     # Define the API URL
#     base_url = f"https://www.googleapis.com/books/v1/volumes/{volume_id}"
#
#     try:
#         # Send request to Google Books API
#         response = requests.get(base_url, params={'key': app.config['GOOGLE_BOOKS_API_KEY']})
#         response.raise_for_status()  # Raises an error if the request fails
#
#         # Return JSON response
#         return jsonify(response.json())
#
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': f'Failed to fetch book from Google API: {str(e)}'}), 500
#
# # @app.route('/books/googlebooks/mylibrary/bookshelves', methods=['GET'])
# # def google_books_mylibrary_bookshelves():
# #     # Define the API URL
# #     base_url = "https://www.googleapis.com/books/v1/mylibrary/bookshelves"
# #
# #     # Get the access token from the environment variable
# #     access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
# #
# #     # Define the headers for the request
# #     headers = {
# #         'Authorization': f'Bearer {access_token}'
# #     }
# #
# #     try:
# #         # Send request to Google Books API
# #         response = requests.get(base_url, headers=headers)
# #         response.raise_for_status()  # Raises an error if the request fails
# #
# #         # Return JSON response
# #         return jsonify(response.json())
# #
# #     except requests.exceptions.RequestException as e:
# #         return jsonify({'error': f'Failed to fetch bookshelves from Google API: {str(e)}'}), 500
# #     except ValueError as e:
# #         return jsonify({'error': str(e)}), 401
#
# @app.route('/books/googlebooks/mylibrary/bookshelves', methods=['GET'])
# def google_books_mylibrary_bookshelves():
#     base_url = "https://www.googleapis.com/books/v1/mylibrary/bookshelves"
#     access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
#
#     if not access_token:
#         logging.error("Access token is missing")
#         return jsonify({'error': 'Access token is missing'}), 401
#
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
#
#     try:
#         response = requests.get(base_url, headers=headers)
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Failed to fetch bookshelves from Google API: {str(e)}")
#         return jsonify({'error': f'Failed to fetch bookshelves from Google API: {str(e)}'}), 500
#
# @app.route('/books/googlebooks/mylibrary/bookshelves/<bookshelf_id>/addVolume', methods=['POST'])
# def google_books_add_volume(bookshelf_id):
#     # Get the volume ID from the request parameters
#     volume_id = request.args.get('volumeId')
#
#     # Define the API URL
#     base_url = f"https://www.googleapis.com/books/v1/mylibrary/bookshelves/{bookshelf_id}/addVolume"
#
#     # Get the access token from the environment variable
#     access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
#
#     print(f"Access Token: {access_token}")
#
#     # Define the headers for the request
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
#
#     # Define the parameters for the request
#     params = {
#         'volumeId': volume_id
#     }
#
#     try:
#         # Send request to Google Books API
#         response = requests.post(base_url, headers=headers, params=params)
#         response.raise_for_status()  # Raises an error if the request fails
#
#         # Return JSON response
#         return jsonify(response.json())
#
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': f'Failed to add volume to bookshelf: {str(e)}'}), 500
#
# @app.route('/books/googlebooks/mylibrary/bookshelves/<bookshelf_id>/removeVolume', methods=['POST'])
# def google_books_remove_volume(bookshelf_id):
#     # Get the volume ID from the request parameters
#     volume_id = request.args.get('volumeId')
#
#     # Define the API URL
#     base_url = f"https://www.googleapis.com/books/v1/mylibrary/bookshelves/{bookshelf_id}/removeVolume"
#
#     # Get the access token from the environment variable
#     access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
#
#     print(f"Access Token: {access_token}")
#
#     # Define the headers for the request
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
#
#     # Define the parameters for the request
#     params = {
#         'volumeId': volume_id
#     }
#
#     try:
#         # Send request to Google Books API
#         response = requests.post(base_url, headers=headers, params=params)
#         response.raise_for_status()  # Raises an error if the request fails
#
#         # Return JSON response
#         return jsonify(response.json())
#
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': f'Failed to remove volume from bookshelf: {str(e)}'}), 500
#
# @app.route('/books/googlebooks/mylibrary/bookshelves/<bookshelf_id>', methods=['GET'])
# def google_books_mylibrary_bookshelf(bookshelf_id):
#     # Define the API URL
#     base_url = f"https://www.googleapis.com/books/v1/mylibrary/bookshelves/{bookshelf_id}"
#
#     # Get the access token from the environment variable
#     access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
#
#     # Define the headers for the request
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
#
#     try:
#         # Send request to Google Books API
#         response = requests.get(base_url, headers=headers)
#         response.raise_for_status()  # Raises an error if the request fails
#
#         # Return JSON response
#         return jsonify(response.json())
#
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': f'Failed to fetch bookshelf from Google API: {str(e)}'}), 500
#
#
# # App route to fetch data from second web service (TMDB API)
# @app.route('/movies/search', methods=['GET'])
# def search_movies():
#     # Get the search query from request parameters
#     query = request.args.get('query')
#
#     # Define the API URL
#     base_url = "https://api.themoviedb.org/3/search/movie"
#
#     # Define request parameters
#     params = {
#         'query': query,
#         'api_key': app.config['TMDB_API_KEY']
#     }
#
#     try:
#         # Send request to TMDB API
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()  # Raises an error if the request fails
#
#         # Return JSON response
#         return jsonify(response.json())
#
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': f'Failed to search movies: {str(e)}'}), 500
#
#
# # Route to the frontend of the application
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import os
import logging

from config import SERVICE1_URL, GOOGLE_BOOKS_API_KEY

app = Flask(__name__)
CORS(app)

# Load configuration from config.py
app.config.from_pyfile('config.py')

SERVICE1_URL = app.config['SERVICE1_URL']

# Configure logging
logging.basicConfig(level=logging.ERROR)

@app.route('/books', methods=['GET', 'POST'])
def books():
    try:
        if request.method == 'GET':
            response = requests.get(f'{SERVICE1_URL}/books')
        else:  # POST
            response = requests.post(f'{SERVICE1_URL}/books', json=request.json)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_by_id(book_id):
    try:
        if request.method == 'GET':
            response = requests.get(f'{SERVICE1_URL}/books/{book_id}')
        elif request.method == 'PUT':
            response = requests.put(f'{SERVICE1_URL}/books/{book_id}', json=request.json)
        else:  # DELETE
            response = requests.delete(f'{SERVICE1_URL}/books/{book_id}')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/{book_id}: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/books/author/<author_name>', methods=['GET', 'DELETE'])
def books_by_author(author_name):
    try:
        if request.method == 'GET':
            response = requests.get(f'{SERVICE1_URL}/books/author/{author_name}')
        else:  # DELETE
            custom_header = request.headers.get('X-CUSTOM-HEADER')
            if custom_header != app.config['AUTH_HEADER']:
                return jsonify({'error': 'Unauthorized'}), 401
            response = requests.delete(f'{SERVICE1_URL}/books/author/{author_name}')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/author/{author_name}: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/books/history/<int:book_id>', methods=['GET'])
def book_history(book_id):
    try:
        response = requests.get(f'{SERVICE1_URL}/books/history/{book_id}')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/history/{book_id}: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/books/batch', methods=['POST', 'PUT'])
def batch_books():
    try:
        if request.method == 'POST':
            response = requests.post(f'{SERVICE1_URL}/books/batch', json=request.json)
        elif request.method == 'PUT':
            response = requests.put(f'{SERVICE1_URL}/books/batch', json=request.json)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/batch: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/books/<int:book_id>/title', methods=['PATCH'])
def update_book_title(book_id):
    try:
        response = requests.patch(f'{SERVICE1_URL}/books/{book_id}/title', json=request.json)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/{book_id}/title: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/books/<int:book_id>/author', methods=['PATCH'])
def update_book_author(book_id):
    try:
        response = requests.patch(f'{SERVICE1_URL}/books/{book_id}/author', json=request.json)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/{book_id}/author: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/books/googlebooks', methods=['GET'])
def google_books_search_volume():
    query = request.args.get('q')
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {'q': query, 'key': os.getenv('GOOGLE_BOOKS_API_KEY')}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/googlebooks: {str(e)}')
        return jsonify({'error': f'Failed to fetch books from Google API: {str(e)}'}), 500

@app.route('/books/googlebooks/<volume_id>', methods=['GET'])
def google_books_volume(volume_id):
    base_url = f"https://www.googleapis.com/books/v1/volumes/{volume_id}"

    try:
        response = requests.get(base_url, params={'key': app.config['GOOGLE_BOOKS_API_KEY']})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/googlebooks/{volume_id}: {str(e)}')
        return jsonify({'error': f'Failed to fetch book from Google API: {str(e)}'}), 500

@app.route('/books/googlebooks/mylibrary/bookshelves', methods=['GET'])
def google_books_mylibrary_bookshelves():
    base_url = "https://www.googleapis.com/books/v1/mylibrary/bookshelves"
    access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')

    if not access_token:
        logging.error("Access token is missing")
        return jsonify({'error': 'Access token is missing'}), 401

    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/googlebooks/mylibrary/bookshelves: {str(e)}')
        return jsonify({'error': f'Failed to fetch bookshelves from Google API: {str(e)}'}), 500

@app.route('/books/googlebooks/mylibrary/bookshelves/<bookshelf_id>/addVolume', methods=['POST'])
def google_books_add_volume(bookshelf_id):
    volume_id = request.args.get('volumeId')
    base_url = f"https://www.googleapis.com/books/v1/mylibrary/bookshelves/{bookshelf_id}/addVolume"
    access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'volumeId': volume_id}

    try:
        response = requests.post(base_url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/googlebooks/mylibrary/bookshelves/{bookshelf_id}/addVolume: {str(e)}')
        return jsonify({'error': f'Failed to add volume to bookshelf: {str(e)}'}), 500

@app.route('/books/googlebooks/mylibrary/bookshelves/<bookshelf_id>/removeVolume', methods=['POST'])
def google_books_remove_volume(bookshelf_id):
    volume_id = request.args.get('volumeId')
    base_url = f"https://www.googleapis.com/books/v1/mylibrary/bookshelves/{bookshelf_id}/removeVolume"
    access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'volumeId': volume_id}

    try:
        response = requests.post(base_url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/googlebooks/mylibrary/bookshelves/{bookshelf_id}/removeVolume: {str(e)}')
        return jsonify({'error': f'Failed to remove volume from bookshelf: {str(e)}'}), 500

@app.route('/books/googlebooks/mylibrary/bookshelves/<bookshelf_id>', methods=['GET'])
def google_books_mylibrary_bookshelf(bookshelf_id):
    base_url = f"https://www.googleapis.com/books/v1/mylibrary/bookshelves/{bookshelf_id}"
    access_token = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /books/googlebooks/mylibrary/bookshelves/{bookshelf_id}: {str(e)}')
        return jsonify({'error': f'Failed to fetch bookshelf from Google API: {str(e)}'}), 500

@app.route('/movies/search', methods=['GET'])
def search_movies():
    query = request.args.get('query')
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {'query': query, 'api_key': app.config['TMDB_API_KEY']}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in /movies/search: {str(e)}')
        return jsonify({'error': f'Failed to search movies: {str(e)}'}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)