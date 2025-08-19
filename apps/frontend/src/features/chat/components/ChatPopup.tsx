import React, { useRef, useEffect } from 'react';

export interface Message {
  from: 'user' | 'bot';
  text: string;
}

interface ChatPopupProps {
  open: boolean;
  onClose: () => void;
  category: string | null;
  categories: string[];
  onSelectCategory: (cat: string) => void;
  messages: Message[];
  input: string;
  onInputChange: (v: string) => void;
  onSend: () => void;
  loading: boolean;
}

const ChatPopup: React.FC<ChatPopupProps> = ({
  open, onClose, category, categories, onSelectCategory, messages, input, onInputChange, onSend, loading
}) => {
  const logRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (open && logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [messages, open]);
  if (!open) return null;
  return (
    <div className="fixed bottom-28 right-8 w-96 max-w-full h-[32rem] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col z-50 animate-fadein">
      {/* ヘッダー */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-100 bg-[#1428FF] text-white rounded-t-2xl">
        <span className="font-bold text-lg">お問い合わせBot</span>
        <button onClick={onClose} aria-label="閉じる" className="text-white hover:opacity-70 text-2xl leading-none">×</button>
      </div>
      {/* チャットログエリア */}
      <div ref={logRef} className="flex-1 p-4 overflow-y-auto text-gray-800 custom-scrollbar bg-gray-50">
        {!category ? (
          <div>
            <div className="mb-2 font-semibold">カテゴリーを選択してください</div>
            <div className="grid grid-cols-2 gap-2">
              {categories.map((cat) => (
                <button
                  key={cat}
                  className="bg-[#1428FF] text-white rounded px-2 py-1 hover:opacity-80 transition"
                  onClick={() => onSelectCategory(cat)}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            <div className="mb-2 text-xs text-gray-500">カテゴリー: {category}</div>
            <div className="space-y-3">
              {messages.map((msg, i) => (
                <div key={i} className={msg.from === 'user' ? 'flex justify-end' : 'flex justify-start items-end gap-2'}>
                  {msg.from === 'bot' && (
                    <span className="w-7 h-7 rounded-full bg-[#1428FF] flex items-center justify-center text-white font-bold text-base shrink-0">B</span>
                  )}
                  <span className={
                    msg.from === 'user'
                      ? 'relative inline-block bg-[#1428FF] text-white rounded-2xl px-4 py-2 shadow max-w-[70%] text-right chat-bubble-user'
                      : 'relative inline-block bg-white border border-gray-200 rounded-2xl px-4 py-2 shadow max-w-[70%] text-left chat-bubble-bot'
                  }>
                    {msg.from === 'bot'
                      ? msg.text.split(/\n{2,}|\n/).map((p, j) => <p key={j} className="mb-2 last:mb-0 whitespace-pre-line">{p}</p>)
                      : msg.text}
                  </span>
                </div>
              ))}
              {loading && <div className="text-xs text-gray-400">Botが応答中...</div>}
            </div>
          </>
        )}
      </div>
      {/* 入力エリア */}
      {category && (
        <div className="p-3 border-t border-gray-100 flex gap-2 bg-white">
          <input
            type="text"
            className="w-full rounded-xl border border-gray-300 px-4 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[#1428FF] transition text-black"
            placeholder="メッセージを入力..."
            value={input}
            onChange={e => onInputChange(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') onSend(); }}
            disabled={loading}
            autoFocus
          />
          <button
            className="bg-[#1428FF] text-white rounded-xl w-14 h-14 flex items-center justify-center shadow hover:bg-blue-700 transition disabled:opacity-50 text-base"
            onClick={onSend}
            disabled={loading || !input.trim()}
            aria-label="送信"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width={32} height={32} fill="currentColor" className="w-8 h-8">
              <polygon points="6,4 20,12 6,20" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

export default ChatPopup; 