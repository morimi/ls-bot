import React from 'react';

interface ChatButtonProps {
  onClick: () => void;
}

const ChatButton: React.FC<ChatButtonProps> = ({ onClick }) => (
  <button
    className="fixed bottom-6 right-6 w-16 h-16 rounded-full bg-[#1428FF] text-white shadow-lg flex items-center justify-center z-50 hover:opacity-90 transition"
    onClick={onClick}
    aria-label="チャットを開く"
  >
    <svg width="32" height="32" fill="none" viewBox="0 0 24 24">
      <path fill="currentColor" d="M12 3C6.477 3 2 6.805 2 11c0 1.61.67 3.13 1.88 4.41-.13.7-.46 1.97-1.7 3.13a1 1 0 0 0 1.09 1.66c2.13-.5 3.7-1.36 4.7-2.01A13.6 13.6 0 0 0 12 17c5.523 0 10-3.805 10-8s-4.477-8-10-8Z"/>
    </svg>
  </button>
);

export default ChatButton; 