import React from 'react';
import { MessageCircle, User, AlertCircle } from 'lucide-react';
import { Message } from '../types/chat';
import { formatTime } from '../utils/dateUtils';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  const isError = message.isError;

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} chat-message`}>
      <div className={`flex items-start space-x-3 max-w-4xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center ${
          isUser 
            ? 'bg-gent-primary text-white' 
            : isError 
              ? 'bg-red-100 text-red-600'
              : 'bg-gent-light text-gent-primary'
        }`}>
          {isUser ? (
            <User className="w-5 h-5" />
          ) : isError ? (
            <AlertCircle className="w-5 h-5" />
          ) : (
            <MessageCircle className="w-5 h-5" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`px-4 py-3 rounded-lg shadow-sm border ${
            isUser 
              ? 'bg-gent-primary text-white border-gent-primary' 
              : isError
                ? 'bg-red-50 text-red-800 border-red-200'
                : 'bg-white text-gent-dark-gray border-gray-200'
          } ${isUser ? 'rounded-br-sm' : 'rounded-bl-sm'}`}>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {message.content}
            </p>
          </div>
          
          {/* Timestamp */}
          <span className={`text-xs text-gent-gray mt-1 px-1 ${isUser ? 'text-right' : 'text-left'}`}>
            {formatTime(message.timestamp)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;