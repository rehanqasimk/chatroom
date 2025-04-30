/**
 * Application Logic
 * 
 * This module handles front-end functionality that's not directly managed by HTMX.
 */
class ChatApplication {
    constructor() {
        this.setupEventListeners();
        this.setupHtmxEventHandlers();
    }
    
    /**
     * Set up event listeners for user interactions
     */
    setupEventListeners() {
        // Handle username changes
        const usernameInput = document.getElementById('username');
        if (usernameInput) {
            usernameInput.addEventListener('change', this.handleUsernameChange.bind(this));
            
            // Set a random username if none is set
            if (!usernameInput.value) {
                usernameInput.value = 'User' + Math.floor(Math.random() * 1000);
            }
        }
    }
    
    /**
     * Set up HTMX event handlers for server interactions
     */
    setupHtmxEventHandlers() {
        // Add username to all API requests
        document.body.addEventListener('htmx:configRequest', (evt) => {
            // Get the current username
            const username = document.getElementById('username')?.value || 'User1';
            
            // Add username to the parameters or URL
            if (evt.detail.parameters) {
                evt.detail.parameters['username'] = username;
            } else {
                // If URL has query params already
                if (evt.detail.path.includes('?')) {
                    evt.detail.path += '&username=' + encodeURIComponent(username);
                } else {
                    evt.detail.path += '?username=' + encodeURIComponent(username);
                }
            }
        });

        // Show toast messages for join and leave actions
        document.body.addEventListener('htmx:afterOnLoad', (evt) => {
            const path = evt.detail.pathInfo.requestPath;
            
            // Check if it's a join or leave action
            if (path.includes('/join')) {
                // Extract the room name from the response (if available) or the target element
                const roomId = path.split('/')[3];
                const roomElement = document.getElementById(`room-${roomId}`);
                const roomName = roomElement ? roomElement.querySelector('.room-name').textContent : 'the room';
                
                this.showToast(`Joined room: ${roomName}`);
            } 
            else if (path.includes('/leave')) {
                // Extract the room name from the response (if available) or the target element
                const roomId = path.split('/')[3];
                const roomElement = document.getElementById(`room-${roomId}`);
                const roomName = roomElement ? roomElement.querySelector('.room-name').textContent : 'the room';
                
                this.showToast(`Left room: ${roomName}`, 'warning');
            }
        });
    }
    
    /**
     * Handle username changes
     */
    handleUsernameChange(event) {
        const newUsername = event.target.value.trim();
        
        // Ensure username is not empty
        if (!newUsername) {
            event.target.value = 'User' + Math.floor(Math.random() * 1000);
            return;
        }
        
        // Refresh the rooms list with the new username
        htmx.ajax('GET', '/api/rooms?username=' + encodeURIComponent(newUsername), '#rooms-list');
        this.showToast(`Username changed to "${newUsername}"`);
    }
    
    /**
     * Show a toast notification
     */
    showToast(message, type = 'success') {
        let toast = document.querySelector('.toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.className = 'toast';
            document.body.appendChild(toast);
        }
        
        // Set message and type
        toast.textContent = message;
        toast.className = `toast ${type}`;
        
        // Show the toast
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        // Hide after a delay
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Initialize the chat application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new ChatApplication();
});
