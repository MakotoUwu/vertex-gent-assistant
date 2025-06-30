// Mock API service that simulates calling your Python agent

export const sendMessage = async (message: string): Promise<string> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

  // Mock responses based on message content
  const lowerMessage = message.toLowerCase();

  if (lowerMessage.includes('time') || lowerMessage.includes('clock')) {
    const now = new Date();
    return `The current time is ${now.toLocaleTimeString()}.`;
  }

  if (lowerMessage.includes('help') || lowerMessage.includes('task')) {
    return "I can help you with various tasks such as:\n\n• Answering questions\n• Providing information\n• Helping with calculations\n• Organizing thoughts\n• General assistance\n\nWhat specific task would you like help with?";
  }

  if (lowerMessage.includes('location') || lowerMessage.includes('find') || lowerMessage.includes('nearby')) {
    return "I can help you find information about locations, but I'll need more specific details about what you're looking for. For example:\n\n• What type of place are you looking for?\n• What's your current location or area of interest?\n• Any specific requirements or preferences?";
  }

  if (lowerMessage.includes('business') || lowerMessage.includes('hours') || lowerMessage.includes('open')) {
    return "Typical business hours vary by industry:\n\n• Retail stores: 9 AM - 6 PM or 10 AM - 8 PM\n• Restaurants: 11 AM - 10 PM (varies widely)\n• Banks: 9 AM - 5 PM (weekdays)\n• Government offices: 8 AM - 5 PM (weekdays)\n\nFor specific businesses, I'd recommend checking their website or calling directly for accurate hours.";
  }

  if (lowerMessage.includes('organize') || lowerMessage.includes('file')) {
    return "Here are some tips for organizing files and folders:\n\n• Create a clear folder structure\n• Use descriptive file names\n• Sort by date, project, or category\n• Delete unnecessary files regularly\n• Use cloud storage for backup\n• Consider using tags or labels\n\nWould you like specific advice for a particular type of organization?";
  }

  if (lowerMessage.includes('support') || lowerMessage.includes('contact')) {
    return "For customer support, you typically have these options:\n\n• Check the company's website for contact information\n• Look for a 'Contact Us' or 'Support' page\n• Try live chat if available\n• Call their customer service number\n• Send an email to their support address\n• Check their social media pages\n\nIs there a specific company or service you need to contact?";
  }

  // Default response
  return "I'm here to help! I can assist you with:\n\n• Answering questions\n• Providing information\n• Helping with tasks\n• General assistance\n\nCould you please be more specific about what you'd like to know or what you need help with?";
};