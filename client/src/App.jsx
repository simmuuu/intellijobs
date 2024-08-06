import React, { useState } from 'react';
import "./App.css";
import { assets } from "./assets/assets";

function App() {
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState([]);
    const [hasStarted, setHasStarted] = useState(false);

    function handleChange(event) {
        setQuery(event.target.value);
    }

    function handleClick(event) {
        event.preventDefault();
        if (query.trim()) {
            const data = { query };
            setMessages([...messages, { text: query, sender: 'user' }]);
            setHasStarted(true);
            fetch('http://127.0.0.1:5000/job-search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
                .then(response => response.json())
                .then(data => {
                    setMessages(prevMessages => [
                        ...prevMessages,
                        { text: data.response, sender: 'bot' }
                    ]);
                })
                .catch(error => {
                    console.error('Error:', error);
                    setMessages(prevMessages => [
                        ...prevMessages,
                        { text: 'Something went wrong. Please try again.', sender: 'bot' }
                    ]);
                });
            setQuery('');
        }
    }

    function handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            handleClick(event);
        }
    }

    return (
        <div className="main">
            <div className="nav">
                <p>IntelliJobs</p>
            </div>
            <div className="main-container">
                {hasStarted ? (
                    <div className="chat-history">
                        {messages.map((message, index) => (
                            <div key={index} className={`chat-message ${message.sender}`}>
                                {message.text}
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="greet">
                        <p><span>Hello, Dev.</span></p>
                        <p>How can I help you today?</p>
                        <div className="cards">
                            <div className="card">
                                <p>Are there freelance opportunities available for web developers?</p>
                                <img src={assets.compass_icon} alt="" />
                            </div>
                            <div className="card">
                                <p>Can you help me find job openings for software developers in San Francisco?</p>
                                <img src={assets.bulb_icon} alt="" />
                            </div>
                            <div className="card">
                                <p>What are the latest job listings for data analysts in New York?</p>
                                <img src={assets.message_icon} alt="" />
                            </div>
                            <div className="card">
                                <p>Are there any remote job opportunities for project managers?</p>
                                <img src={assets.code} alt="" />
                            </div>
                        </div>
                    </div>
                )}
                <div className="main-bottom">
                    <div className="search-box">
                        <textarea
                            onChange={handleChange}
                            placeholder="Enter your query"
                            value={query}
                            onKeyDown={handleKeyDown}
                        />
                        <div>
                            <img src={assets.send_icon} alt="" onClick={handleClick} />
                        </div>
                    </div>
                    <p className="bottom-info">Powered by IntelliJobs</p>
                </div>
            </div>
        </div>
    );
}

export default App;
