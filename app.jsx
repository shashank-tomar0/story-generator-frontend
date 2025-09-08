import { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [genre, setGenre] = useState('fantasy');
  const [story, setStory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!prompt) {
      setError('Please enter a story idea!');
      return;
    }

    setIsLoading(true);
    setError('');
    setStory([]);

    try {
      const response = await fetch('http://127.0.0.1:5001/generate-story', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt, genre }),
      });

      if (!response.ok) {
        throw new Error('Something went wrong on the server.');
      }

      const data = await response.json();
      setStory(data.story);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>AI Story Weaver 📖✨</h1>
        <p>Turn your ideas into illustrated stories!</p>
      </header>

      <div className="input-form">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g., A lonely robot finds a flower in a post-apocalyptic city."
        />
        <div className="options">
          <select value={genre} onChange={(e) => setGenre(e.target.value)}>
            <option value="fantasy">Fantasy</option>
            <option value="sci-fi">Sci-Fi</option>
            <option value="mystery">Mystery</option>
            <option value="comedy">Comedy</option>
          </select>
          <button onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? 'Weaving your tale...' : 'Generate Story'}
          </button>
        </div>
      </div>
      
      {error && <p className="error">{error}</p>}

      <div className="story-container">
        {isLoading && <div className="loader"></div>}
        
        {story.map((part, index) => (
          <div key={index} className="story-part">
            <img src={part.image_url} alt={`Scene ${index + 1}`} />
            <p>{part.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;