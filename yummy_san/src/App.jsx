import { useState } from 'react';
import './App.css';

function App() {
  const [url, setURL] = useState('');
  const [question, setQuestion] = useState('');
  const [urlSubmitted, setURLSubmitted] = useState(false);

  const handleURLSubmit = (e) => {
    e.preventDefault(); // Prevent form from refreshing the page
    if (url.trim()) {
      setURLSubmitted(true); // Hide URL box and show Question box
    } else {
      alert('Please enter a valid URL.');
    }
  };

  const handleQuestionSubmit = (e) => {
    e.preventDefault(); // Prevent form from refreshing the page
    if (question.trim()) {
      alert(`Your question: "${question}" has been submitted!`);
      setQuestion('');
    } else {
      alert('Please enter a question.');
    }
  };

  const handleNewChat = () => {
    setURL(''); // Reset URL
    setQuestion(''); // Reset Question
    setURLSubmitted(false); // Show URL input again
  };

  return (
    <>
      <header className='main-heading'>
        <img src="../img/logo_processed.jpeg" className="logo" alt="Logo" />
        <h1>Yummy San</h1>
      </header>

      {!urlSubmitted && (
        <form className='text-box' onSubmit={handleURLSubmit}>
          <div className="input-group">
          <input
            className='text-input'
            type='text'
            value={url}
            onChange={(e) => setURL(e.target.value)}
            placeholder='Enter URL'
          />
          <button className='submit-arrow-button' type='submit'>
            <span className='submit-arrow-icon'>&#10140;</span>
          </button>
          </div>
        </form>
      )}

      {urlSubmitted && (
        <form className='text-box' onSubmit={handleQuestionSubmit}>
          <div className="input-group">
          <input
            className='text-input'
            type='text'
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder='Question'
          />
          <button className='submit-arrow-button' type='submit'>
            <span className='submit-arrow-icon'>&#10140;</span>
          </button>
          </div>
        </form>
      )}

      <button className='new-chat-button' onClick={handleNewChat}>
        New Chat
      </button>
    </>
  );
}

export default App;
