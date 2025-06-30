import React from 'react';
import { Clock, AlertTriangle, MapPin, Building, Trash2, Phone } from 'lucide-react';

interface QuickActionsProps {
  onActionClick: (message: string) => void;
}

const QuickActions: React.FC<QuickActionsProps> = ({ onActionClick }) => {
  const actions = [
    {
      icon: Clock,
      label: 'What time is it?',
      message: 'What time is it right now?',
      color: 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100',
    },
    {
      icon: AlertTriangle,
      label: 'Help with tasks',
      message: 'Can you help me with my daily tasks?',
      color: 'bg-orange-50 text-orange-700 border-orange-200 hover:bg-orange-100',
    },
    {
      icon: MapPin,
      label: 'Find locations',
      message: 'Help me find nearby locations',
      color: 'bg-green-50 text-green-700 border-green-200 hover:bg-green-100',
    },
    {
      icon: Building,
      label: 'Business hours',
      message: 'What are typical business hours?',
      color: 'bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100',
    },
    {
      icon: Trash2,
      label: 'Organize files',
      message: 'Help me organize my files and folders',
      color: 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100',
    },
    {
      icon: Phone,
      label: 'Contact support',
      message: 'How can I contact customer support?',
      color: 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100',
    },
  ];

  return (
    <div className="gent-card p-6">
      <h3 className="text-lg font-heading font-semibold text-gent-dark-gray mb-4">
        Popular Questions
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {actions.map((action, index) => {
          const IconComponent = action.icon;
          return (
            <button
              key={index}
              onClick={() => onActionClick(action.message)}
              className={`flex items-center space-x-3 p-3 rounded-lg border transition-all duration-200 hover:shadow-md text-left ${action.color}`}
            >
              <IconComponent className="w-5 h-5 flex-shrink-0" />
              <span className="text-sm font-medium">{action.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default QuickActions;