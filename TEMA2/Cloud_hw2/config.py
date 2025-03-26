from dotenv import load_dotenv
import os

load_dotenv()

SERVICE1_URL = os.getenv('SERVICE1_URL')
AUTH_HEADER = os.getenv('AUTH_HEADER')

GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
GOOGLE_BOOKS_API_URL = os.getenv('GOOGLE_BOOKS_API_URL')
GOOGLE_BOOKS_USER_ID = os.getenv('GOOGLE_BOOKS_USER_ID')
GOOGLE_BOOKS_ACCESS_TOKEN = os.getenv('GOOGLE_BOOKS_ACCESS_TOKEN')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# Print the loaded environment variables for debugging
# print(f"GOOGLE_BOOKS_API_KEY: {GOOGLE_BOOKS_API_KEY}")

# SERVICE2_URL = os.getenv('SERVICE2_URL')
# SERVICE2_API_KEY = os.getenv('SERVICE2_API_KEY')
# SERVICE3_URL = os.getenv('SERVICE3_URL')
# SERVICE3_API_KEY = os.getenv('SERVICE3_API_KEY')