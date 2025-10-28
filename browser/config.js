// Rammerhead configuration override for Replit environment

module.exports = {
    bindingAddress: '0.0.0.0',  // Allow connections from anywhere (Replit environment)
    port: 3000,  // Use port 3000 to match our existing setup
    crossDomainPort: 3001,  // Cross-domain port
    
    // Update server info for reverse proxy setup
    getServerInfo: () => ({ 
        hostname: 'localhost', 
        port: 3000, 
        crossDomainPort: 3001, 
        protocol: 'http:' 
    }),
    
    // Keep the default password
    password: 'sharkie4life',
    
    // Logging for development
    logLevel: 'info',
};
