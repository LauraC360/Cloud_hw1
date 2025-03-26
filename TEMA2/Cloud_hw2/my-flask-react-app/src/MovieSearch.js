import React, { useState } from 'react';

const MovieSearch = () => {
  const [query, setQuery] = useState('');
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState('');
  const [searchPerformed, setSearchPerformed] = useState(false);

  const handleSearchChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSearchClick = () => {
    setSearchPerformed(true);
    fetch(`/movies/search?query=${query}`)
      .then(response => response.json())
      .then(data => {
        if (data.results) {
          setMovies(data.results);
          setError('');
        } else {
          setMovies([]);
          setError('No results found.');
        }
      })
      .catch(error => {
        console.error('Error fetching movies:', error);
        setError('An error occurred while fetching movies.');
      });
  };

  return (
    <div className="container">
      <h1>Search Movies</h1>
      <div className="mb-4">
        <input
          type="text"
          className="form-control"
          placeholder="Search for a movie..."
          value={query}
          onChange={handleSearchChange}
        />
        <button className="btn btn-primary mt-2" onClick={handleSearchClick}>
          Search
        </button>
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="row">
        {movies.length > 0 ? (
          movies.map(movie => (
            <div className="col-md-4" key={movie.id}>
              <div className="card mb-4">
                <img
                  src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                  className="card-img-top"
                  alt={movie.title}
                />
                <div className="card-body">
                  <h5 className="card-title">{movie.title}</h5>
                  <p className="card-text">Release Date: {movie.release_date}</p>
                  <p className="card-text">Overview: {movie.overview}</p>
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

export default MovieSearch;