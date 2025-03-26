import React, { useEffect, useState } from 'react';

const Books = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetch('/books')
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          setBooks(data);
        } else {
          console.error('Unexpected response format:', data);
        }
      })
      .catch(error => console.error('Error fetching books:', error));
  }, []);

  const handleRemoveBook = (bookId) => {
    removeBookFromLocalLibrary(bookId);
  };

  const removeBookFromLocalLibrary = (bookId) => {
    fetch(`/books/${bookId}`, {
      method: 'DELETE'
    })
    .then(() => {
      setBooks(books.filter(book => book.id !== bookId));
    })
    .catch(error => console.error('Error removing book from local library:', error));
  };

  return (
    <div className="container">
      <h1>Books</h1>
      <div className="row">
        {books.map(book => (
          <div className="col-md-4" key={book.id}>
            <div className="card mb-4">
              <div className="card-body">
                <h5 className="card-title">{book.title}</h5>
                <p className="card-text">Author: {book.author}</p>
                <p className="card-text">Year: {book.year}</p>
                <button className="btn btn-danger mt-2" onClick={() => handleRemoveBook(book.id)}>
                  Remove from Library
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Books;