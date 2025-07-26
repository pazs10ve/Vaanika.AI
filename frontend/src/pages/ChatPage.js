import React, { useState, useEffect, useRef } from 'react';
import Sidebar from '../components/Sidebar';
import PromptInput from '../components/PromptInput';

const ChatPage = () => {
  const [sessions, setSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [history, setHistory] = useState([]);
  const [userId, setUserId] = useState(null);
  const [userName, setUserName] = useState(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [isNewChat, setIsNewChat] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    // Load user info from localStorage
    const storedUserId = localStorage.getItem('userId');
    const storedUserName = localStorage.getItem('loggedInUser');
    if (storedUserId) setUserId(storedUserId);
    if (storedUserName) setUserName(storedUserName);
  }, []);

  useEffect(() => {
    // Fetch sessions only after userId is loaded
    const fetchSessions = async () => {
      if (!userId) return;
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(`http://localhost:4000/api/sessions`, {
          headers: { 'Authorization': token }
        });
        const data = await res.json();
        setSessions(data);
      } catch (err) {
        console.error('Error fetching sessions:', err);
      }
    };
    fetchSessions();
  }, [userId]);

  useEffect(() => {
    const fetchHistory = async () => {
      if (!activeSession) {
        setHistory([]);
        return;
      }
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:4000/api/sessions/${activeSession}/messages`, {
        headers: { 'Authorization': token }
      });
      if (res.ok) {
        const messages = await res.json();
        setHistory(messages);
      } else {
        setHistory([]);
      }
    };
    fetchHistory();
  }, [activeSession]);

  // Scroll to bottom on new message
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [history]);

  // Show welcome message when a new session is created or new chat is clicked
  useEffect(() => {
    if (isNewChat) {
      setShowWelcome(true);
    } else {
      setShowWelcome(false);
    }
  }, [isNewChat]);

  const handleNewChat = () => {
    setActiveSession(null);
    setHistory([]);
    setIsNewChat(true);
    setShowWelcome(true);
  };

  const handleSessionSelect = (sessionId) => {
    setActiveSession(sessionId);
    setIsNewChat(false);
    setShowWelcome(false);
  };

  const handlePromptSubmit = async (prompt, type) => {
    if (!userId) {
      alert('Please login first.');
      return;
    }

    // If this is a new chat, create a session first
    let sessionId = activeSession;
    if (isNewChat || !activeSession) {
      try {
        const token = localStorage.getItem('token');
        // Create session with first message as title
        const sessionTitle = prompt.length > 50 ? prompt.substring(0, 50) + '...' : prompt;
        const sessionRes = await fetch('http://localhost:4000/api/sessions', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': token
          },
          body: JSON.stringify({ title: sessionTitle, userName }),
        });
        
        if (sessionRes.ok) {
          const newSession = await sessionRes.json();
          sessionId = newSession._id;
          setActiveSession(sessionId);
          setSessions(prev => [newSession, ...prev]);
          setIsNewChat(false);
        } else {
          alert('Failed to create session');
          return;
        }
      } catch (err) {
        console.error('Failed to create session:', err);
        alert('Failed to create session');
        return;
      }
    }

    const endpoint = `http://localhost:4000/api/generate/${type}`;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token
        },
        body: JSON.stringify({ prompt, sessionId }),
      });
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', response.status, errorText);
        alert(`Error: ${response.status}`);
        return;
      }
      // After generation, refresh history
      const res = await fetch(`http://localhost:4000/api/sessions/${sessionId}/messages`, {
        headers: { 'Authorization': token }
      });
      if (res.ok) {
        const messages = await res.json();
        setHistory(messages);
      }
    } catch (err) {
      console.error('Fetch error:', err);
      alert('Network or server error');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('loggedInUser');
    localStorage.removeItem('userId');
    window.location.href = '/login';
  };

  // User avatar with first letter
  const userInitial = userName ? userName.charAt(0).toUpperCase() : 'U';

  return (
    <div className="min-h-screen flex bg-black text-white relative">
      {/* Sidebar */}
      <Sidebar
        userId={userId}
        userName={userName}
        sessions={sessions}
        setSessions={setSessions}
        setActiveSession={handleSessionSelect}
        setHistory={setHistory}
        activeSession={activeSession}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        onNewChat={handleNewChat}
      />
      
      {/* Main Chat Area */}
      <div className={`flex-1 flex flex-col h-screen transition-all duration-300 ${sidebarCollapsed ? 'ml-16' : 'ml-64'}`}>
        {/* Chat Stream */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4" style={{marginBottom: '100px'}}>
          {history.map((entry, idx) => (
            <div key={idx} className={`flex ${entry.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xl px-4 py-3 rounded-lg shadow ${entry.role === 'user' ? 'bg-green-600 text-white' : 'bg-zinc-800 text-zinc-100'} whitespace-pre-line`}>
                {entry.role === 'user' && (
                  <span className="block text-xs opacity-70 mb-1">You</span>
                )}
                {entry.role === 'assistant' && (
                  <span className="block text-xs opacity-70 mb-1">AI ({entry.type || 'text'})</span>
                )}
                {/* Render text or output */}
                {entry.type === 'video' && entry.role === 'assistant' ? (
                  <video controls src={entry.url || entry.content} className="w-full rounded" />
                ) : entry.type === 'graphics' && entry.role === 'assistant' ? (
                  <img src={entry.url || entry.content} alt="Generated Graphic" className="w-full rounded" />
                ) : entry.type === 'audio' && entry.role === 'assistant' ? (
                  <audio controls src={entry.url || entry.content} className="w-full" />
                ) : (
                  <span>{entry.content}</span>
                )}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        
        {/* Welcome Message - Big and Bold in Center */}
        {showWelcome && (
          <div className={`absolute inset-0 flex items-center justify-center z-10 pointer-events-none transition-all duration-300 ${sidebarCollapsed ? 'left-16' : 'left-64'} right-0`}>
            <div className="text-center">
              <h1 className="text-6xl font-bold text-white mb-4">
                Welcome, <span className="text-green-400">{userName}</span>!
              </h1>
              <p className="text-xl text-zinc-400 max-w-md mx-auto">
                Start a new conversation by typing your first message below.
              </p>
            </div>
          </div>
        )}
        
        {/* Prompt Input at Bottom */}
        <div className={`absolute bottom-0 z-10 transition-all duration-300 pb-6 ${sidebarCollapsed ? 'left-20' : 'left-72'} right-6`}> 
          <div className="bg-zinc-900 border-t border-zinc-800 rounded-2xl shadow-lg p-4 max-w-4xl mx-auto">
            <PromptInput onSubmit={handlePromptSubmit} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
