import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { chatService } from '../services/api';

const ChatContainer = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hallo! Ich bin Ihr digitaler Assistent für die Stadt Rüsselsheim. Wie kann ich Ihnen heute helfen?\n\nIch kann Ihnen Informationen geben zu:\n- Bürgerservice (Personalausweis, Meldewesen)\n- KFZ-Zulassung\n- Müllabfuhr und Abfallwirtschaft\n- Öffnungszeiten und Kontakte',
      timestamp: new Date(),
    },
  ]);
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message
    const userMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Send to API
      const response = await chatService.sendMessage(message, sessionId);

      // Update session ID if new
      if (!sessionId) {
        setSessionId(response.session_id);
      }

      // Add assistant response
      const assistantMessage = {
        role: 'assistant',
        content: response.message,
        intent: response.intent,
        contextUsed: response.context_used,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);

    } catch (err) {
      console.error('Error sending message:', err);
      setError('Entschuldigung, es gab einen Fehler bei der Verarbeitung Ihrer Anfrage.');

      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: 'Entschuldigung, es gab einen Fehler bei der Verarbeitung Ihrer Anfrage. Bitte versuchen Sie es erneut.',
        timestamp: new Date(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto bg-white shadow-xl">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
        {isLoading && (
          <div className="flex items-center space-x-2 text-gray-500">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
            <span className="text-sm">Assistent tippt...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t bg-gray-50 p-4">
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
        {sessionId && (
          <p className="text-xs text-gray-500 mt-2 text-center">
            Session ID: {sessionId.slice(0, 8)}...
          </p>
        )}
      </div>
    </div>
  );
};

export default ChatContainer;
