import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleUrlSubmit = () => {
    if (url) {
      setIsChatOpen(true);
    }
  };

  const handleSendMessage = async () => {
    if (input.trim() === "") return;
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await axios.post(`${url}/app`, {
        message: input,
      });
      const serverMessage = response.data.response;
      setMessages([...newMessages, { sender: "server", text: serverMessage }]);
    } catch (error) {
      setMessages([...newMessages, { sender: "server", text: "Error: Could not connect to server." }]);
    }
  };

  return (
    <div className="App">
      {!isChatOpen ? (
        <div className="url-input">
          <h2>Enter Server URL</h2>
          <input
            type="text"
            placeholder="Enter the server URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button onClick={handleUrlSubmit}>Open Chat</button>
        </div>
      ) : (
        <div className="chat-container">
          <div className="chat-header">
            <h2>Chat Interface</h2>
            <button onClick={() => setIsChatOpen(false)}>New Chat</button>
          </div>
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.sender === "user" ? "user" : "server"}`}
              >
                {msg.text}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              placeholder="Type your message"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
