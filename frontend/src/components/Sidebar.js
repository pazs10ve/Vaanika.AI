import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ 
  sessions, 
  setSessions, 
  setActiveSession, 
  setHistory, 
  userId, 
  userName, 
  activeSession, 
  collapsed, 
  onToggleCollapse,
  onNewChat
}) => {
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState('');
  const [showUserMenu, setShowUserMenu] = useState(false);
  const navigate = useNavigate();

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays === 1) return 'Today';
    if (diffDays === 2) return 'Yesterday';
    if (diffDays <= 7) return `${diffDays - 1} days ago`;
    return date.toLocaleDateString();
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('loggedInUser');
    localStorage.removeItem('userId');
    navigate('/login');
  };

  const handleNewChatClick = () => {
    if (onNewChat) {
      onNewChat();
    } else {
      setShowForm(true);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !userName) return;
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:4000/api/sessions', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': token
        },
        body: JSON.stringify({ title, userName }),
      });
      const session = await res.json();
      setActiveSession(session._id);
      setHistory([]);
      setTitle('');
      setShowForm(false);
      setSessions(prev => [...prev, session]);
    } catch (err) {
      console.error('Failed to create session:', err);
    }
  };

  useEffect(() => {
    const fetchSessions = async () => {
      if (!userId) return;
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(`http://localhost:4000/api/sessions`, {
          headers: {
            'Authorization': token
          }
        });
        const data = await res.json();
        setSessions(data);
      } catch (err) {
        console.error('Failed to fetch sessions:', err);
      }
    };
    fetchSessions();
  }, [userId, setSessions]);

  // User avatar with first letter
  const userInitial = userName ? userName.charAt(0).toUpperCase() : 'U';

  if (collapsed) {
    return (
      <div className="w-16 bg-zinc-900 border-r border-zinc-700 h-screen flex flex-col items-center py-4">
        {/* Toggle Button */}
        <button
          className="text-zinc-400 hover:text-white bg-zinc-800 rounded-full p-2 mb-4"
          onClick={onToggleCollapse}
          title="Expand sidebar"
        >
          <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>

        {/* New Chat Button (Icon only) */}
        <button
          className="text-zinc-400 hover:text-white bg-zinc-800 rounded-full p-2 mb-4"
          onClick={handleNewChatClick}
          title="New chat"
        >
          <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <path d="M12 5v14M5 12h14" />
          </svg>
        </button>

        {/* User Avatar (Collapsed) */}
        <div className="relative mt-auto">
          <button
            className="w-10 h-10 bg-green-600 text-white rounded-full flex items-center justify-center font-semibold text-sm hover:bg-green-700 transition-colors"
            onClick={() => setShowUserMenu(!showUserMenu)}
            title={userName}
          >
            {userInitial}
          </button>
          
          {/* User Menu Popover */}
          {showUserMenu && (
            <div className="absolute bottom-full left-0 mb-2 w-48 bg-zinc-900 border border-zinc-700 rounded shadow-lg z-50">
              <div className="p-3 border-b border-zinc-700">
                <div className="text-sm text-zinc-400">Signed in as</div>
                <div className="font-semibold text-white">{userName}</div>
              </div>
              <button
                className="w-full text-left px-3 py-2 text-red-400 hover:bg-zinc-800 rounded text-sm"
                onClick={handleLogout}
              >
                Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="w-64 bg-zinc-900 border-r border-zinc-700 h-screen flex flex-col relative">
      {/* Header with Toggle */}
      <div className="p-4 border-b border-zinc-700">
        <div className="flex items-center justify-between">
          <button
            className="text-zinc-400 hover:text-white bg-zinc-800 rounded-full p-1"
            onClick={onToggleCollapse}
            title="Collapse sidebar"
          >
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M15 18l-6-6 6-6" />
            </svg>
          </button>
        </div>
      </div>

      {/* New Chat Button */}
      <button
        onClick={handleNewChatClick}
        className="mx-4 mt-4 bg-green-500 text-black py-2 rounded hover:bg-green-600 transition-colors"
      >
        + New Chat
      </button>

      {/* Session List */}
      <div className="flex-1 overflow-y-auto mt-4">
        <ul className="space-y-1 px-4">
          {sessions.map((session) => (
            <li key={session._id}>
              <button
                onClick={() => setActiveSession(session._id)}
                className={`w-full text-left px-3 py-2 rounded transition-colors ${
                  activeSession === session._id 
                    ? 'bg-green-600 text-white border-l-4 border-green-400' 
                    : 'bg-zinc-800 hover:bg-zinc-700 text-zinc-300'
                }`}
              >
                <div className="font-medium truncate">{session.title || 'Untitled Session'}</div>
                <div className="text-xs opacity-70">{formatDate(session.createdAt)}</div>
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* User Info at Bottom (Expanded) */}
      <div className="p-4 border-t border-zinc-700">
        <div className="relative">
          <button
            className="flex items-center gap-3 px-2 py-2 rounded-full hover:bg-zinc-700 focus:outline-none transition-all duration-300 w-full"
            onClick={() => setShowUserMenu(!showUserMenu)}
          >
            <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-semibold text-sm flex-shrink-0">
              {userInitial}
            </div>
            <span className="font-semibold text-white truncate">{userName}</span>
          </button>
          
          {/* User Menu Popover */}
          {showUserMenu && (
            <div className="absolute bottom-full left-0 mb-2 w-48 bg-zinc-900 border border-zinc-700 rounded shadow-lg z-50">
              <div className="p-3 border-b border-zinc-700">
                <div className="text-sm text-zinc-400">Signed in as</div>
                <div className="font-semibold text-white">{userName}</div>
              </div>
              <button
                className="w-full text-left px-3 py-2 text-red-400 hover:bg-zinc-800 rounded text-sm"
                onClick={handleLogout}
              >
                Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
