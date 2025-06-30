// Mock API service that simulates calling your Python agent
// Updated with Dutch responses to match the Gent website style

export const sendMessage = async (message: string): Promise<string> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

  // Mock responses in Dutch based on message content
  const lowerMessage = message.toLowerCase();

  if (lowerMessage.includes('bibliotheek') || lowerMessage.includes('openingsuren') || lowerMessage.includes('krook')) {
    return "De Krook, de hoofdbibliotheek van Gent, bevindt zich aan Miriam Makebaplein 1, 9000 Gent. Openingsuren: maandag tot vrijdag van 10.00 tot 19.00 uur, zaterdag van 10.00 tot 19.00 uur, zondag gesloten. De bibliotheek biedt boeken, tijdschriften, kranten, cd's, dvd's en gratis internettoegang. Er worden regelmatig speciale evenementen en tentoonstellingen georganiseerd. Voor meer informatie: dekrook.be of bel 09 323 68 00.";
  }

  if (lowerMessage.includes('vervoer') || lowerMessage.includes('verstoring') || lowerMessage.includes('bus') || lowerMessage.includes('tram') || lowerMessage.includes('lijn')) {
    if (lowerMessage.includes('verstoring') || lowerMessage.includes('probleem') || lowerMessage.includes('storing')) {
      return "Ik heb de huidige vervoerssituatie in Gent gecontroleerd. Er zijn momenteel geen grote verstoringen gemeld op het De Lijn-netwerk. Alle bus- en tramlijnen rijden normaal. Let wel: kleine vertragingen kunnen voorkomen door verkeerssituaties. Voor real-time updates kunt u de De Lijn-app of website raadplegen.";
    } else {
      return "Ik kan u helpen met vervoersdienstregelingen! Ik heb echter meer specifieke informatie nodig. Kunt u mij vertellen:\n\n• Welke bus- of tramlijn u interesseert?\n• Of welke halte u wilt controleren?\n\nBijvoorbeeld: 'Wat is de dienstregeling van lijn 1?' of 'Wanneer vertrekt de volgende bus aan station Gent-Zuid?'";
    }
  }

  if (lowerMessage.includes('afval') || lowerMessage.includes('inzameling') || lowerMessage.includes('vuilnis')) {
    return "In Gent volgt de afvalinzameling een specifiek schema: Restafval (grijze zakken) wordt wekelijks opgehaald op uw toegewezen ophaaldag. PMD (blauwe zakken) wordt om de twee weken opgehaald. Papier en karton worden om de vier weken opgehaald. Glas wordt om de vier weken aan huis opgehaald, maar er zijn ook glascontainers verspreid over de stad. Tuinafval (groene zakken) wordt seizoensgebonden opgehaald. Controleer uw persoonlijke ophaalkalender op ivago.be of download de Recycle!-app voor uw specifieke ophaaldagen.";
  }

  if (lowerMessage.includes('vergunning') || lowerMessage.includes('bouwen') || lowerMessage.includes('bouw')) {
    return "Voor het aanvragen van een bouwvergunning in Gent moet u uw aanvraag indienen via het Omgevingsloket (omgevingsloket.be). Vereiste documenten zijn meestal: architecturale plannen, stabiliteitstudie, EPB-rapport en een beschrijving van het project. De verwerkingstijd is ongeveer 105 dagen voor gewone vergunningen, maar kan korter zijn voor kleinere projecten. De kost varieert van €50 tot €200 afhankelijk van de omvang van het werk. Voor vragen: stedenbouw@stad.gent of bezoek Woodrow Wilsonplein 1, 9000 Gent, maandag tot vrijdag van 9.00 tot 12.30 uur.";
  }

  if (lowerMessage.includes('stadhuis') || lowerMessage.includes('stadshuis')) {
    return "Het Stadhuis van Gent is open van maandag tot vrijdag van 9.00 tot 12.30 uur en van 14.00 tot 17.00 uur. Specifieke diensten kunnen andere openingsuren hebben. Het Stadhuis bevindt zich aan Botermarkt 1, 9000 Gent. Voor de meeste diensten is een afspraak vereist die u kunt maken via stad.gent of door te bellen naar 09 210 10 10.";
  }

  if (lowerMessage.includes('park') || lowerMessage.includes('recreatie')) {
    return "Gent heeft verschillende prachtige parken: Citadelpark (grootste centrale park met museum), Zuidpark (met muziekkiosk en speeltuinen), Koning Albertpark (met sportfaciliteiten), Muinkpark (klein vredig park met vijver), en recreatiegebied Blaarmeersen (met meer, strand, sportfaciliteiten en wandelpaden). De meeste parken zijn open van zonsopgang tot zonsondergang. Barbecueën is meestal niet toegestaan behalve in aangewezen zones in Blaarmeersen. Honden moeten aangelijnd blijven in alle parken tenzij anders aangegeven.";
  }

  if (lowerMessage.includes('museum')) {
    return "Gent biedt verschillende musea: Design Museum Gent (design van middeleeuwen tot heden), Museum voor Schone Kunsten (MSK) met kunst van middeleeuwen tot 20e eeuw, SMAK (hedendaagse kunst), STAM (stadsmuseum over de geschiedenis van Gent), en Huis van Alijn (over het dagelijks leven). Musea zijn meestal open van dinsdag tot zondag, 10.00 tot 18.00 uur (maandag gesloten). De Gentse Museumpas (€35) geeft een jaar lang onbeperkte toegang tot alle stadsmusea. Veel musea bieden gratis toegang op de eerste woensdagnamiddag van elke maand.";
  }

  // Default response in Dutch
  return "Ik begrijp dat u een vraag heeft over de stadsdiensten van Gent. Ik kan u helpen met informatie over:\n\n• Stadhuis en administratieve diensten\n• Afvalinzameling en schema's\n• Openbaar vervoer (dienstregelingen en verstoringen)\n• Bouwvergunningen en procedures\n• Bibliotheek- en museuminformatie\n• Parken en recreatiegebieden\n• Inschrijving nieuwe inwoners\n\nKunt u specifieker zijn over wat u wilt weten?";
};