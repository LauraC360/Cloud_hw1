import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Books from './Books';
import BookSearch from './BookSearch';
import MovieSearch from './MovieSearch';

const App = () => {
  return (
    <Router>
      <div>
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <Link className="navbar-brand" to="/">My Flask React App</Link>
          <div className="collapse navbar-collapse">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/books">My Books</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/books/search">Search Books</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/movies/search">Movies</Link>
              </li>
            </ul>
          </div>
        </nav>
        <div className="container">
          <Routes>
            <Route path="/books" element={<Books />} />
            <Route path="/books/search" element={<BookSearch />} />
            <Route path="/movies/search" element={<MovieSearch />} />
            <Route path="/" element={<h1>Welcome to My Books and Movies Finder App</h1>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;