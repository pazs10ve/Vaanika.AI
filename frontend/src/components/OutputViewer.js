import React from 'react';

const OutputViewer = ({ output }) => {
  if (!output) return <div className="p-6">No output yet...</div>;

  return (
    <div className="p-6 overflow-y-auto">
      <h3 className="text-lg font-semibold mb-4">Generated Output</h3>
      {output.type === 'video' && <video controls src={output.url} className="w-full rounded" />}
      {output.type === 'graphics' && <img src={output.url} alt="Generated Graphic" className="w-full rounded" />}
      {output.type === 'audio' && <audio controls src={output.url} className="w-full" />}      
    </div>
  );
};

export default OutputViewer;
