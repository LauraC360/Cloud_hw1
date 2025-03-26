import React, { useState } from 'react';

const BookSearch = () => {
  const [query, setQuery] = useState('');
  const [books, setBooks] = useState([]);
  const [error, setError] = useState('');
  const [searchPerformed, setSearchPerformed] = useState(false);

  const handleSearchChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSearchClick = async () => {
    setSearchPerformed(true);
    await fetch(`/books/googlebooks?q=intitle:${query}`)
      .then(response => response.json())
      .then(data => {
        if (data.items) {
          setBooks(data.items);
          setError('');
        } else {
          setBooks([]);
          setError('No results found.');
        }
      })
      .catch(error => {
        console.error('Error fetching books:', error);
        setError('An error occurred while fetching books.');
      });
  };

  const handleAddBook = (book) => {
    const bookData = {
      title: book.volumeInfo.title,
      author: book.volumeInfo.authors?.join(', '),
      year: book.volumeInfo.publishedDate?.substring(0, 4)
    };

    fetch('/books', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(bookData)
    })
    .then(response => response.json())
    .then(() => {
      fetch(`/books/googlebooks/mylibrary/bookshelves/2/addVolume?volumeId=${book.id}`, {
        method: 'POST'
      })
      .then(response => response.json())
      .catch(error => console.error('Error adding book to Google Books library:', error));
    })
    .catch(error => console.error('Error adding book to local library:', error));
  };

  return (
    <div className="container">
      <h1>Search Books</h1>
      <div className="mb-4">
        <input
          type="text"
          className="form-control"
          placeholder="Search for a book by title..."
          value={query}
          onChange={handleSearchChange}
        />
        <button className="btn btn-primary mt-2" onClick={handleSearchClick}>
          Search
        </button>
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="row">
        {books.length > 0 ? (
          books.map(book => (
            <div className="col-md-4" key={book.id}>
              <div className="card mb-4">
                <img
                  src={book.volumeInfo.imageLinks?.thumbnail}
                  className="card-img-top"
                  alt={book.volumeInfo.title}
                  style={{ width: '150px', height: '225px' }}
                />
                <div className="card-body">
                  <h5 className="card-title">{book.volumeInfo.title}</h5>
                  <p className="card-text">Author: {book.volumeInfo.authors?.join(', ')}</p>
                  <p className="card-text">Published Date: {book.volumeInfo.publishedDate}</p>
                  <button className="btn btn-success mt-2" onClick={() => handleAddBook(book)}>
                    Add to Library
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          searchPerformed && <div className="col-12"></div>
        )}
      </div>
    </div>
  );
};

export default BookSearch;