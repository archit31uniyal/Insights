import { useState } from 'react';
import './App.css';
import axios from 'axios';
import config from "./config";

function App() {
  const [url, setURL] = useState('');
  const [question, setQuestion] = useState('');
  const [urlSubmitted, setURLSubmitted] = useState(false);
  const [reviews, setReviews] = useState({})
  const [answer, setAnswer] = useState()

  const handleURLSubmit = (e) => {
    e.preventDefault(); // Prevent form from refreshing the page
    
    if (url.trim()) {
      setURLSubmitted(true); // Hide URL box and show Question box
      axios({
        method: "POST",
        url: `${config.API_BASE_URL}/url`,
        data: { "url": url }
      })
      .then(response => {
          const data = response.data;
          setReviews(data);
          console.log(data);
        })
        .catch(error => {
          console.error(error);
        });
    } else {
      alert('Please enter a valid URL.');
    }
  };

  const handleQuestionSubmit = (e) => {
    e.preventDefault(); // Prevent form from refreshing the page
    if (question.trim()) {
      alert(`Your question: "${question}" has been submitted!`);
      console.log(reviews);
      axios({
        method: "POST",
        url: `${config.API_BASE_URL}/response`,
        data: { 
                "reviews": reviews,
                "question": question 
              }
      })
      .then(response => {
          const answer = response.data;
          setAnswer(answer);
          console.log(answer);
        })
        .catch(error => {
          console.error(error);
        });
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
