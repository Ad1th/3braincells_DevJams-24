import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

const Popup: React.FC = () => {
  const [task, setTask] = useState<string>('');
  const [siteData, setSiteData] = useState<Record<string, { totalTime: number }>>({});
  const [isEnabled, setIsEnabled] = useState<boolean>(true);
  const [links, setLinks] = useState<string[]>([]); // State to hold fetched links

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Get the current tab's URL using Chrome's tabs API
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentUrl = tabs[0].url; // Get the current tab's URL

      fetch('http://127.0.0.1:8000/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task, url: currentUrl }), // Send both task and URL
      })
      .then(response => response.json())
      .then(result => {
        console.log("Response from server:", result); // Log the response from the server
      })
      .catch(error => {
        console.error("Error:", error);
      });
    });
  };

  useEffect(() => {
    chrome.storage.local.get(['currentTask', 'siteTimers', 'isEnabled'], (result) => {
      console.log('Storage data:', result); // Debug log
      if (result.currentTask) {
        setTask(result.currentTask);
      }
      if (result.siteTimers) {
        setSiteData(result.siteTimers);
      }
      setIsEnabled(result.isEnabled !== undefined ? result.isEnabled : true);
    });
  }, []);

  const handleTaskSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    chrome.runtime.sendMessage({ action: 'setTask', task: task });
  };

  const handleToggle = () => {
    const newState = !isEnabled;
    setIsEnabled(newState);
    chrome.storage.local.set({ isEnabled: newState });
  };

  // const fetchLinks = async () => {
  //   // Call your server to fetch threads/links
  //   const response = await fetch('http://localhost:3001/prompts'); // Adjust endpoint as needed

  //   if (response.ok) {
  //     const data = await response.json();
  //     // Assuming data.savedPrompts contains the links or threads
  //     setLinks(data.savedPrompts || []); // Set the fetched links in state
  //   } else {
  //     console.error('Failed to fetch links:', response.statusText);
  //   }
  // };

  const chartData = {
    labels: Object.keys(siteData),
    datasets: [
      {
        data: Object.values(siteData).map(site => site.totalTime / 60000), // Convert to minutes
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40'
        ],
      },
    ],
  };

  return (
    <div className="popup">
      <h1>Productivity tracker</h1>
      <div className="toggle-container">
        <label className="switch">
          <input type="checkbox" checked={isEnabled} onChange={handleToggle} />
          <span className="slider round"></span>
        </label>
        <span>Enable Extension: {isEnabled ? 'On' : 'Off'}</span>
      </div>
      <form onSubmit={handleTaskSubmit}>
        <input
          type="text"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="What are you working on?"
        />
        <button type="submit">Set Task</button>
      </form>
      <div className="chart-container">
        <h2>Time Spent on Sites (minutes)</h2>
        {Object.keys(siteData).length > 0 ? (
          <Pie data={chartData} />
        ) : (
          <p>No data available yet. Start browsing to collect data.</p>
        )}
      </div>

      {/* Display fetched links */}
      {links.length > 0 && (
        <div className="links-container">
          <h2>Relevant Links:</h2>
          <ul>
            {links.map((link, index) => (
              <li key={index}><a href={link} target="_blank" rel="noopener noreferrer">{link}</a></li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Popup;

const root = createRoot(document.getElementById('root') as HTMLElement);
root.render(<Popup />);