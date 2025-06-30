import React from 'react';
import { ExternalLink, Phone, Mail, MapPin } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gent-secondary text-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Contact Info */}
          <div>
            <h3 className="font-heading font-semibold text-lg mb-4">Contact</h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-center space-x-2">
                <Phone className="w-4 h-4" />
                <span>09 210 10 10</span>
              </div>
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4" />
                <span>info@stad.gent</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4" />
                <span>Botermarkt 1, 9000 Gent</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-heading font-semibold text-lg mb-4">Snelle Links</h3>
            <div className="space-y-2 text-sm">
              <a href="https://stad.gent" className="flex items-center space-x-1 hover:text-gent-light transition-colors">
                <span>Officiële website</span>
                <ExternalLink className="w-3 h-3" />
              </a>
              <a href="https://mijn.gent.be" className="flex items-center space-x-1 hover:text-gent-light transition-colors">
                <span>Mijn Gent</span>
                <ExternalLink className="w-3 h-3" />
              </a>
              <a href="https://data.delijn.be" className="flex items-center space-x-1 hover:text-gent-light transition-colors">
                <span>De Lijn Open Data</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          {/* About */}
          <div>
            <h3 className="font-heading font-semibold text-lg mb-4">Over deze dienst</h3>
            <p className="text-sm text-gray-300 leading-relaxed">
              Deze digitale assistent helpt u bij vragen over stadsdiensten, 
              openbaar vervoer en actuele verstoringen in Gent. 
              Aangedreven door kunstmatige intelligentie.
            </p>
          </div>
        </div>

        <div className="border-t border-gent-primary mt-8 pt-6">
          <div className="flex flex-col md:flex-row items-center justify-between text-sm text-gray-300">
            <div>
              © 2024 Stad Gent. Alle rechten voorbehouden.
            </div>
            <div className="flex items-center space-x-4 mt-4 md:mt-0">
              <a href="#" className="hover:text-white transition-colors">Privacy</a>
              <a href="#" className="hover:text-white transition-colors">Toegankelijkheid</a>
              <a href="#" className="hover:text-white transition-colors">Cookies</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;