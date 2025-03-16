import React, { useState } from 'react';
import './App.css';

function App() {
  // State to store user input and response from API
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  // Function to call the API
  const getResponse = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),  // Send the query entered by the user
      });
      const data = await res.json();  // Parse the JSON response
      setResponse(data.response);  // Set the response from the backend
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Query</h1>

        <input
          type="text"
          placeholder="Enter your query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}  // Update query state
        />

        <button onClick={getResponse}>Get Response</button>

        <div>
          <h2>Response from Backend:</h2>
          <p>{response}</p>
        </div>
      </header>
    </div>
  );
}

export default App;
