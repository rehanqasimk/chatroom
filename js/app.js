/**
 * Application Logic
 * 
 * This module handles front-end functionality that's not directly managed by HTMX.
 */
class ChatApplication {
    constructor() {
        this.setupEventListeners();
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
     * Handle username changes
     */
    handleUsernameChange(event) {
        const newUsername = event.target.value.trim();
        
        // Ensure username is not empty
        if (!newUsername) {
            event.target.value = 'User' + Math.floor(Math.random() * 1000);
            return;
        }
        
        // If we have the mock API service, refresh the rooms list
        if (window.mockApiService) {
            window.mockApiService.renderRoomsList();
            window.mockApiService.showToast(`Username changed to "${newUsername}"`);
        } else {
            // Fallback if mockApiService isn't available
            this.showToast(`Username changed to "${newUsername}"`);
        }
    }
    
    /**
     * Show a toast notification (fallback if mockApiService isn't available)
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
