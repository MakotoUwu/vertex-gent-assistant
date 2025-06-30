import React from 'react';
import { ExternalLink, Phone, Mail, MapPin } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gent-secondary text-white">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {/* Contact Info */}
          <div>
            <h3 className="font-heading font-semibold text-xl mb-6 text-white">Contact</h3>
            <div className="space-y-4 text-base">
              <div className="flex items-start space-x-3">
                <Phone className="w-5 h-5 mt-0.5 text-gent-light flex-shrink-0" />
                <span className="text-gray-200">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-start space-x-3">
                <Mail className="w-5 h-5 mt-0.5 text-gent-light flex-shrink-0" />
                <span className="text-gray-200">support@assistant.app</span>
              </div>
              <div className="flex items-start space-x-3">
                <MapPin className="w-5 h-5 mt-0.5 text-gent-light flex-shrink-0" />
                <span className="text-gray-200">123 Main Street, City</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-heading font-semibold text-xl mb-6 text-white">Quick Links</h3>
            <div className="space-y-3 text-base">
              <a href="#" className="flex items-center space-x-2 text-gray-200 hover:text-white transition-colors duration-200 group">
                <span>Documentation</span>
                <ExternalLink className="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-200" />
              </a>
              <a href="#" className="flex items-center space-x-2 text-gray-200 hover:text-white transition-colors duration-200 group">
                <span>API Reference</span>
                <ExternalLink className="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-200" />
              </a>
              <a href="#" className="flex items-center space-x-2 text-gray-200 hover:text-white transition-colors duration-200 group">
                <span>Support</span>
                <ExternalLink className="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-200" />
              </a>
            </div>
          </div>

          {/* About */}
          <div>
            <h3 className="font-heading font-semibold text-xl mb-6 text-white">About</h3>
            <p className="text-base text-gray-200 leading-relaxed">
              This AI assistant helps you with various tasks and questions. 
              Powered by advanced artificial intelligence technology.
            </p>
          </div>
        </div>

        <div className="border-t border-gent-primary/30 mt-12 pt-8">
          <div className="flex flex-col md:flex-row items-center justify-between text-base">
            <div className="text-gray-300">
              © 2024 AI Assistant. All rights reserved.
            </div>
            <div className="flex items-center space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-300 hover:text-white transition-colors duration-200">Privacy</a>
              <a href="#" className="text-gray-300 hover:text-white transition-colors duration-200">Terms</a>
              <a href="#" className="text-gray-300 hover:text-white transition-colors duration-200">Cookies</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;