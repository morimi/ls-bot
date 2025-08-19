import React, { useState } from 'react';
import type { ChatCategory, ChatRequest, ChatResponse } from '@ls-bot/shared-types';
import ChatButton from './components/ChatButton';
import ChatPopup, { type Message } from './components/ChatPopup';

const CATEGORIES: ChatCategory[] = [
  'キャラクター',
  'ライブイベント',
  'グッズ',
  '楽曲',
  '生放送',
  'その他',
];

const ChatWidgetContainer: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [category, setCategory] = useState<ChatCategory | null>(null);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || !category) return;
    const userMsg = { from: 'user', text: input } as const;
    setMessages((msgs) => [...msgs, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const requestData: ChatRequest = { category, message: input };
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData),
      });
      const data: ChatResponse = await res.json();
      // botの返事を適度に改行・段落で整形
      const formatBotReply = (text: string) => {
        // 句点・改行・記号で分割
        const sentences = text.split(/(?<=[。！？!?.])|\n/);
        const grouped: string[] = [];
        let buf = '';
        for (let i = 0; i < sentences.length; i++) {
          buf += sentences[i];
          // 2文ごと、または50文字以上で区切る
          if ((i + 1) % 2 === 0 || buf.length > 50) {
            grouped.push(buf.trim());
            buf = '';
          }
        }
        if (buf.trim()) grouped.push(buf.trim());
        return grouped.join('\n\n');
      };
      setMessages((msgs) => [
        ...msgs,
        { from: 'bot', text: formatBotReply(data.reply) } as const
      ]);
    } catch {
      setMessages((msgs) => [...msgs, { from: 'bot', text: 'エラーが発生しました' } as const]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <ChatButton onClick={() => setOpen((v) => !v)} />
      <ChatPopup
        open={open}
        onClose={() => setOpen(false)}
        category={category}
        categories={CATEGORIES}
        onSelectCategory={setCategory}
        messages={messages}
        input={input}
        onInputChange={setInput}
        onSend={handleSend}
        loading={loading}
      />
    </>
  );
};

export default ChatWidgetContainer; 