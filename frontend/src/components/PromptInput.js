import React, { useState } from 'react';

const PromptInput = ({ onSubmit }) => {
  const [prompt, setPrompt] = useState('');
  const [type, setType] = useState('video');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    onSubmit(prompt, type);
    setPrompt('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (prompt.trim()) {
        onSubmit(prompt, type);
        setPrompt('');
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-3">
      <textarea
        className="flex-1 h-14 resize-none p-3 bg-zinc-800 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 shadow"
        placeholder="Type your prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={1}
      />
      <select 
        value={type} 
        onChange={(e) => setType(e.target.value)} 
        className="h-14 bg-zinc-800 text-white px-3 rounded-xl shadow focus:outline-none focus:ring-2 focus:ring-green-500"
      >
        <option value="video">Video</option>
        <option value="graphics">Graphics</option>
        <option value="audio">Audio</option>
      </select>
      <button 
        type="submit" 
        className="h-14 bg-green-500 text-black px-6 rounded-xl hover:bg-green-600 font-semibold shadow focus:outline-none focus:ring-2 focus:ring-green-500"
      >
        Generate
      </button>
    </form>
  );
};

export default PromptInput;