/**
 * Mock API Service
 * 
 * This module simulates backend API endpoints for the chat room application.
 * In a real application, these would be server-side endpoints.
 */
class MockApiService {
    constructor() {
        // Initialize with some sample data
        this.chatRooms = [
            { id: 1, name: 'General Discussion', owner: 'Admin', createdAt: new Date().toISOString() },
            { id: 2, name: 'Tech Talk', owner: 'User1', createdAt: new Date().toISOString() }
        ];
        
        // Counter for generating unique IDs
        this.nextId = this.chatRooms.length + 1;
        
        // Initialize the application
        this.init();
    }
    
    /**
     * Initialize the application and set up HTMX events
     */
    init() {
        // Render the initial rooms list
        document.addEventListener('DOMContentLoaded', () => {
            this.renderRoomsList();
            this.setupHtmxHandlers();
        });
    }
    
    /**
     * Set up handlers for HTMX events
     */
    setupHtmxHandlers() {
        const self = this;
        
        // Handle HTMX before send event to intercept API requests
        document.body.addEventListener('htmx:beforeSend', function(evt) {
            const path = evt.detail.path;
            const method = evt.detail.verb.toLowerCase();
            let body = evt.detail.parameters;
            
            // If this is an API request, prevent it and handle it ourselves
            if (path.startsWith('/api/')) {
                evt.preventDefault();
                
                // Get the response from our mock handler
                let responseText = '';
                
                try {
                    responseText = self.handleRequest(path, method, body);
                    
                    // If the request was successful, manually trigger the HTMX afterOnLoad
                    // event with our mock response
                    const xhr = {
                        status: 200,
                        responseText: responseText
                    };
                    
                    // Need to set a timeout to simulate network request
                    setTimeout(() => {
                        // Call the same handler that htmx would call
                        evt.detail.xhr = xhr;
                        evt.detail.target.innerHTML = responseText;
                        
                        // Dispatch a successful afterSwap event
                        const afterSwapEvent = new CustomEvent('htmx:afterSwap', {
                            bubbles: true,
                            detail: {
                                xhr: xhr,
                                target: evt.detail.target
                            }
                        });
                        
                        evt.detail.target.dispatchEvent(afterSwapEvent);
                        
                        // Dispatch a successful afterOnLoad event
                        const afterOnLoadEvent = new CustomEvent('htmx:afterOnLoad', {
                            bubbles: true,
                            detail: {
                                xhr: xhr,
                                target: evt.detail.target
                            }
                        });
                        
                        evt.detail.target.dispatchEvent(afterOnLoadEvent);
                    }, 300);
                } catch (error) {
                    console.error('Mock API error:', error);
                }
            }
        });
        
        // Handle click on "Create Room" button
        document.addEventListener('click', function(evt) {
            const target = evt.target;
            
            // Check if it's the "Create Room" button
            if (target.matches('button[hx-get="/api/rooms/create-form"]')) {
                evt.preventDefault();
                const createForm = document.getElementById('create-room-form');
                if (createForm) {
                    createForm.innerHTML = self.getCreateRoomForm();
                }
            }
            
            // Check if it's the "Cancel" button for create form
            if (target.matches('button[hx-get="/api/rooms/cancel-create"]')) {
                evt.preventDefault();
                const createForm = document.getElementById('create-room-form');
                if (createForm) {
                    createForm.innerHTML = '';
                }
            }
            
            // Check if it's the "Edit" button for a room
            if (target.matches('button[hx-get*="/api/rooms/"][hx-get*="/edit-form"]')) {
                evt.preventDefault();
                const editTarget = target.getAttribute('hx-target');
                const roomIdMatch = target.getAttribute('hx-get').match(/\/api\/rooms\/(\d+)\/edit-form/);
                
                if (roomIdMatch && editTarget) {
                    const roomId = parseInt(roomIdMatch[1]);
                    const editContainer = document.querySelector(editTarget);
                    
                    if (editContainer) {
                        editContainer.innerHTML = self.getEditRoomForm(roomId);
                    }
                }
            }
            
            // Check if it's the "Cancel" button for edit form
            if (target.matches('button[hx-get="/api/rooms"]')) {
                evt.preventDefault();
                self.renderRoomsList();
            }
            
            // Check if it's the "Delete" button for a room
            if (target.matches('button[hx-delete*="/api/rooms/"][hx-delete*="/delete"]')) {
                evt.preventDefault();
                
                // Check if confirmation is required
                const needConfirm = target.hasAttribute('hx-confirm');
                const confirmMessage = target.getAttribute('hx-confirm');
                
                if (!needConfirm || confirm(confirmMessage)) {
                    const roomIdMatch = target.getAttribute('hx-delete').match(/\/api\/rooms\/(\d+)\/delete/);
                    
                    if (roomIdMatch) {
                        const roomId = parseInt(roomIdMatch[1]);
                        self.deleteRoom(roomId);
                        self.renderRoomsList();
                    }
                }
            }
            
            // Check if it's the "Join" button for a room
            if (target.matches('button[hx-get*="/api/rooms/"][hx-get*="/join"]')) {
                evt.preventDefault();
                const roomIdMatch = target.getAttribute('hx-get').match(/\/api\/rooms\/(\d+)\/join/);
                
                if (roomIdMatch) {
                    const roomId = parseInt(roomIdMatch[1]);
                    const room = self.chatRooms.find(r => r.id === roomId);
                    
                    if (room) {
                        self.showToast(`Joined room: "${room.name}"`);
                    }
                }
            }
        });
        
        // Handle form submissions
        document.addEventListener('submit', function(evt) {
            const form = evt.target;
            
            // Create room form
            if (form.matches('form[hx-post="/api/rooms/create"]')) {
                evt.preventDefault();
                
                const formData = new FormData(form);
                const roomName = formData.get('roomName');
                
                if (roomName) {
                    self.createRoom({roomName});
                    self.renderRoomsList();
                    
                    // Clear the create form
                    const createForm = document.getElementById('create-room-form');
                    if (createForm) {
                        createForm.innerHTML = '';
                    }
                }
            }
            
            // Edit room form
            if (form.matches('form[hx-put*="/api/rooms/"][hx-put*="/edit"]')) {
                evt.preventDefault();
                
                const formData = new FormData(form);
                const roomName = formData.get('roomName');
                const roomIdMatch = form.getAttribute('hx-put').match(/\/api\/rooms\/(\d+)\/edit/);
                
                if (roomName && roomIdMatch) {
                    const roomId = parseInt(roomIdMatch[1]);
                    self.updateRoom(roomId, {roomName});
                    self.renderRoomsList();
                }
            }
        });
    }
    
    /**
     * Handle mock API requests
     */
    handleRequest(path, method, body) {
        // Route the API request
        if (path === '/api/rooms' && (method === 'get' || !method)) {
            return this.getRooms();
        } else if (path === '/api/rooms/create-form') {
            return this.getCreateRoomForm();
        } else if (path === '/api/rooms/create' && method === 'post') {
            return this.createRoom(body);
        } else if (path.match(/\/api\/rooms\/\d+\/edit-form/)) {
            const id = parseInt(path.match(/\/api\/rooms\/(\d+)\/edit-form/)[1]);
            return this.getEditRoomForm(id);
        } else if (path.match(/\/api\/rooms\/\d+\/edit/) && method === 'put') {
            const id = parseInt(path.match(/\/api\/rooms\/(\d+)\/edit/)[1]);
            return this.updateRoom(id, body);
        } else if (path.match(/\/api\/rooms\/\d+\/delete/) && method === 'delete') {
            const id = parseInt(path.match(/\/api\/rooms\/(\d+)\/delete/)[1]);
            return this.deleteRoom(id);
        }
        
        // Default response
        return JSON.stringify({ error: 'Not found' });
    }
    
    /**
     * Render the rooms list into the DOM
     */
    renderRoomsList() {
        const roomsList = document.getElementById('rooms-list');
        if (roomsList) {
            roomsList.innerHTML = this.getRooms();
            this.updateRoomOwnership();
        }
    }
    
    /**
     * Get all chat rooms HTML
     */
    getRooms() {
        const html = `
            <div class="rooms-container">
                ${this.chatRooms.length === 0 
                    ? '<p>No chat rooms available. Create a new one!</p>' 
                    : this.chatRooms.map(room => this.renderRoomItem(room)).join('')}
            </div>
        `;
        return html;
    }
    
    /**
     * Render a single room item HTML
     */
    renderRoomItem(room) {
        const currentUser = document.getElementById('username')?.value || 'User1';
        const isOwner = room.owner === currentUser;
        
        return `
            <div class="room-item ${isOwner ? 'owned-room' : ''}" id="room-${room.id}">
                <div class="room-info">
                    <div class="room-name">${room.name}</div>
                    <div class="room-owner">Created by: ${room.owner}</div>
                </div>
                <div class="room-actions">
                    <button 
                        class="btn"
                        hx-get="/api/rooms/${room.id}/join"
                        hx-swap="none"
                        hx-target="#rooms-list">
                        Join
                    </button>
                    ${isOwner ? `
                        <button 
                            class="btn"
                            hx-get="/api/rooms/${room.id}/edit-form"
                            hx-target="#edit-form-${room.id}"
                            hx-swap="innerHTML">
                            Edit
                        </button>
                        <button 
                            class="btn btn-danger"
                            hx-delete="/api/rooms/${room.id}/delete"
                            hx-target="#rooms-list"
                            hx-confirm="Are you sure you want to delete this room?">
                            Delete
                        </button>
                    ` : ''}
                </div>
                <div id="edit-form-${room.id}"></div>
            </div>
        `;
    }
    
    /**
     * Get create room form HTML
     */
    getCreateRoomForm() {
        return `
            <form hx-post="/api/rooms/create" hx-target="#rooms-list" hx-swap="innerHTML">
                <div class="form-group">
                    <label for="roomName">Room Name</label>
                    <input type="text" id="roomName" name="roomName" required>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn" 
                        hx-get="/api/rooms/cancel-create" 
                        hx-target="#create-room-form" 
                        hx-swap="innerHTML">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-success">Create Room</button>
                </div>
            </form>
        `;
    }
    
    /**
     * Create a new chat room
     */
    createRoom(data) {
        const username = document.getElementById('username')?.value || 'User1';
        const newRoom = {
            id: this.nextId++,
            name: data.roomName,
            owner: username,
            createdAt: new Date().toISOString()
        };
        
        this.chatRooms.push(newRoom);
        
        // Show success notification
        this.showToast(`Room "${newRoom.name}" created successfully!`);
        
        // Return the updated rooms list
        return this.getRooms();
    }
    
    /**
     * Get edit room form HTML
     */
    getEditRoomForm(roomId) {
        const room = this.chatRooms.find(r => r.id === roomId);
        if (!room) {
            return '<p>Room not found</p>';
        }
        
        return `
            <form hx-put="/api/rooms/${roomId}/edit" hx-target="#rooms-list" hx-swap="innerHTML">
                <div class="form-group">
                    <label for="editRoomName">Room Name</label>
                    <input type="text" id="editRoomName" name="roomName" value="${room.name}" required>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn" 
                        hx-get="/api/rooms"
                        hx-target="#rooms-list" 
                        hx-swap="innerHTML">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-success">Update Room</button>
                </div>
            </form>
        `;
    }
    
    /**
     * Update a chat room
     */
    updateRoom(roomId, data) {
        const roomIndex = this.chatRooms.findIndex(r => r.id === roomId);
        if (roomIndex === -1) {
            return '<p>Room not found</p>';
        }
        
        // Update the room name
        this.chatRooms[roomIndex].name = data.roomName;
        
        // Show success notification
        this.showToast(`Room updated successfully!`);
        
        // Return the updated rooms list
        return this.getRooms();
    }
    
    /**
     * Delete a chat room
     */
    deleteRoom(roomId) {
        const roomIndex = this.chatRooms.findIndex(r => r.id === roomId);
        if (roomIndex === -1) {
            return '<p>Room not found</p>';
        }
        
        // Store the room name before deleting
        const roomName = this.chatRooms[roomIndex].name;
        
        // Remove the room
        this.chatRooms.splice(roomIndex, 1);
        
        // Show success notification
        this.showToast(`Room "${roomName}" deleted successfully!`, 'error');
        
        // Return the updated rooms list
        return this.getRooms();
    }
    
    /**
     * Update room ownership visual indicators
     */
    updateRoomOwnership() {
        const username = document.getElementById('username')?.value || 'User1';
        const roomItems = document.querySelectorAll('.room-item');
        
        roomItems.forEach(roomItem => {
            const ownerElement = roomItem.querySelector('.room-owner');
            if (ownerElement) {
                const ownerText = ownerElement.textContent;
                const owner = ownerText.replace('Created by: ', '').trim();
                
                // Add visual indicator for owned rooms
                if (owner === username) {
                    roomItem.classList.add('owned-room');
                } else {
                    roomItem.classList.remove('owned-room');
                }
            }
        });
    }
    
    /**
     * Show a toast notification
     */
    showToast(message, type = 'success') {
        // Create toast element if it doesn't exist
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

// Initialize the mock API service
const mockApiService = new MockApiService();
window.mockApiService = mockApiService;
