from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder='../static', static_url_path='/')
CORS(app)  # Enable CORS for all domains on all routes

# Initialize with some sample data
chat_rooms = [
    {'id': 1, 'name': 'General Discussion', 'owner': 'Admin', 'createdAt': datetime.now().isoformat()},
    {'id': 2, 'name': 'Tech Talk', 'owner': 'User1', 'createdAt': datetime.now().isoformat()}
]
next_id = len(chat_rooms) + 1

# Dictionary to track which users have joined which rooms
# Format: {username: [room_id1, room_id2, ...]}
joined_rooms = {}

# Template for rooms list HTML
ROOMS_LIST_TEMPLATE = '''
<div class="rooms-container">
    {% if rooms|length == 0 %}
        <p>No chat rooms available. Create a new one!</p>
    {% else %}
        {% for room in rooms %}
        <div class="room-item {% if room.owner == username %}owned-room{% endif %} {% if room.id in joined_rooms %}joined-room{% endif %}" id="room-{{ room.id }}">
            <div class="room-info">
                <div class="room-name">{{ room.name }}</div>
                <div class="room-owner">Created by: {{ room.owner }}</div>
            </div>
            <div class="room-actions">
                {% if room.id in joined_rooms %}
                <button 
                    class="btn btn-warning"
                    hx-get="/api/rooms/{{ room.id }}/leave"
                    hx-target="#rooms-list"
                    hx-swap="innerHTML">
                    Leave
                </button>
                {% else %}
                <button 
                    class="btn"
                    hx-get="/api/rooms/{{ room.id }}/join"
                    hx-target="#rooms-list"
                    hx-swap="innerHTML">
                    Join
                </button>
                {% endif %}
                {% if room.owner == username %}
                <button 
                    class="btn"
                    hx-get="/api/rooms/{{ room.id }}/edit-form"
                    hx-target="#edit-form-{{ room.id }}"
                    hx-swap="innerHTML">
                    Edit
                </button>
                <button 
                    class="btn btn-danger"
                    hx-delete="/api/rooms/{{ room.id }}/delete"
                    hx-target="#rooms-list"
                    hx-confirm="Are you sure you want to delete this room?">
                    Delete
                </button>
                {% endif %}
            </div>
            <div id="edit-form-{{ room.id }}"></div>
        </div>
        {% endfor %}
    {% endif %}
</div>
'''

# Template for create room form
CREATE_ROOM_FORM = '''
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
'''

# Template for edit room form
EDIT_ROOM_FORM = '''
<form hx-put="/api/rooms/{{ room.id }}/edit" hx-target="#rooms-list" hx-swap="innerHTML">
    <div class="form-group">
        <label for="editRoomName">Room Name</label>
        <input type="text" id="editRoomName" name="roomName" value="{{ room.name }}" required>
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
'''

@app.route('/')
def index():
    # Serve the main index.html file
    return app.send_static_file('index.html')

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    # Get the username from the request (in real app would be from authentication)
    username = request.args.get('username', 'User1')
    
    # Get list of rooms this user has joined
    user_joined_rooms = joined_rooms.get(username, [])
    
    # Render the rooms list HTML
    return render_template_string(ROOMS_LIST_TEMPLATE, rooms=chat_rooms, username=username, joined_rooms=user_joined_rooms)

@app.route('/api/rooms/create-form', methods=['GET'])
def get_create_room_form():
    # Return the create room form HTML
    return CREATE_ROOM_FORM

@app.route('/api/rooms/cancel-create', methods=['GET'])
def cancel_create_room():
    # Return empty string to clear the form
    return ''

@app.route('/api/rooms/create', methods=['POST'])
def create_room():
    global next_id
    
    # Get room name from form data
    room_name = request.form.get('roomName')
    # Get username (in a real app would be from authentication)
    username = request.form.get('username', 'User1')
    
    if not room_name:
        return "Room name is required", 400
    
    # Create new room
    new_room = {
        'id': next_id,
        'name': room_name,
        'owner': username,
        'createdAt': datetime.now().isoformat()
    }
    
    # Add to rooms list
    chat_rooms.append(new_room)
    next_id += 1
    
    # Get list of rooms this user has joined
    user_joined_rooms = joined_rooms.get(username, [])
    
    # Return updated rooms list
    return render_template_string(ROOMS_LIST_TEMPLATE, rooms=chat_rooms, username=username, joined_rooms=user_joined_rooms)

@app.route('/api/rooms/<int:room_id>/edit-form', methods=['GET'])
def get_edit_room_form(room_id):
    # Find room by ID
    room = next((r for r in chat_rooms if r['id'] == room_id), None)
    
    if not room:
        return "Room not found", 404
    
    # Return edit form HTML
    return render_template_string(EDIT_ROOM_FORM, room=room)

@app.route('/api/rooms/<int:room_id>/edit', methods=['PUT'])
def update_room(room_id):
    # Get room name from form data
    room_name = request.form.get('roomName')
    # Get username (in a real app would be from authentication)
    username = request.args.get('username', 'User1')
    
    if not room_name:
        return "Room name is required", 400
    
    # Find room by ID
    room = next((r for r in chat_rooms if r['id'] == room_id), None)
    
    if not room:
        return "Room not found", 404
    
    # Update room name
    room['name'] = room_name
    
    # Get list of rooms this user has joined
    user_joined_rooms = joined_rooms.get(username, [])
    
    # Return updated rooms list
    return render_template_string(ROOMS_LIST_TEMPLATE, rooms=chat_rooms, username=username, joined_rooms=user_joined_rooms)

@app.route('/api/rooms/<int:room_id>/delete', methods=['DELETE'])
def delete_room(room_id):
    global chat_rooms
    # Get username (in a real app would be from authentication)
    username = request.args.get('username', 'User1')
    
    # Find room by ID
    room = next((r for r in chat_rooms if r['id'] == room_id), None)
    
    if not room:
        return "Room not found", 404
    
    # Remove room from list
    chat_rooms = [r for r in chat_rooms if r['id'] != room_id]
    
    # If any users have joined this room, remove it from their joined_rooms list
    for user, rooms in joined_rooms.items():
        if room_id in rooms:
            joined_rooms[user] = [r for r in rooms if r != room_id]
    
    # Get list of rooms this user has joined
    user_joined_rooms = joined_rooms.get(username, [])
    
    # Return updated rooms list
    return render_template_string(ROOMS_LIST_TEMPLATE, rooms=chat_rooms, username=username, joined_rooms=user_joined_rooms)

@app.route('/api/rooms/<int:room_id>/join', methods=['GET'])
def join_room(room_id):
    # Get username from request
    username = request.args.get('username', 'User1')
    
    # Find room by ID
    room = next((r for r in chat_rooms if r['id'] == room_id), None)
    
    if not room:
        return "Room not found", 404
    
    # Add room to user's joined rooms
    if username not in joined_rooms:
        joined_rooms[username] = []
    
    if room_id not in joined_rooms[username]:
        joined_rooms[username].append(room_id)
    
    # Refresh the rooms list to show updated UI
    return render_template_string(ROOMS_LIST_TEMPLATE, rooms=chat_rooms, username=username, joined_rooms=joined_rooms.get(username, []))

@app.route('/api/rooms/<int:room_id>/leave', methods=['GET'])
def leave_room(room_id):
    # Get username from request
    username = request.args.get('username', 'User1')
    
    # Find room by ID
    room = next((r for r in chat_rooms if r['id'] == room_id), None)
    
    if not room:
        return "Room not found", 404
    
    # Remove room from user's joined rooms
    if username in joined_rooms and room_id in joined_rooms[username]:
        joined_rooms[username].remove(room_id)
    
    # Return a success message
    message = f"Left room: {room['name']}"
    
    # Refresh the rooms list to show updated UI
    return render_template_string(ROOMS_LIST_TEMPLATE, rooms=chat_rooms, username=username, joined_rooms=joined_rooms.get(username, []))

if __name__ == '__main__':
    app.run(debug=True, port=5000)