import React from 'react';
import ReactMarkdown from 'react-markdown';

const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user';
  const isError = message.isError;

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('de-DE', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-primary-600 text-white'
            : isError
            ? 'bg-red-100 text-red-900'
            : 'bg-gray-100 text-gray-900'
        }`}
      >
        {/* Message content */}
        <div className="prose prose-sm max-w-none">
          {isUser ? (
            <p className="text-white m-0">{message.content}</p>
          ) : (
            <ReactMarkdown
              className={isError ? 'text-red-900' : 'text-gray-900'}
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                ul: ({ children }) => <ul className="ml-4 mb-2">{children}</ul>,
                ol: ({ children }) => <ol className="ml-4 mb-2">{children}</ol>,
                li: ({ children }) => <li className="mb-1">{children}</li>,
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {/* Metadata */}
        <div className={`flex items-center justify-between mt-2 text-xs ${
          isUser ? 'text-primary-100' : 'text-gray-500'
        }`}>
          <span>{formatTime(message.timestamp)}</span>
          {message.intent && (
            <span className="ml-2 px-2 py-1 bg-white bg-opacity-20 rounded">
              {message.intent === 'appointment' && '📅 Termin'}
              {message.intent === 'form' && '📄 Formular'}
              {message.intent === 'information' && '💡 Info'}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
