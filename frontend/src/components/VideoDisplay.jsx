import React from 'react';

function VideoDisplay({ imageData }) {
  return (
    <div className="aspect-w-16 aspect-h-9 bg-black rounded-lg overflow-hidden flex items-center justify-center">
      {imageData ? (
        <img
          src={imageData}
          alt="Generated Animation"
          className="max-h-full max-w-full object-contain"
        />
      ) : (
        <span className="text-white">No image generated.</span>
      )}
    </div>
  );
}

export default VideoDisplay; 