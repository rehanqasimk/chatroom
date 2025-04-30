import json
import pytest
from bs4 import BeautifulSoup

def test_get_rooms(client):
    """Test getting the list of chat rooms."""
    response = client.get('/api/rooms?username=TestUser')
    assert response.status_code == 200
    
    # Check that the response contains the test rooms
    assert b'Test Room 1' in response.data
    assert b'Test Room 2' in response.data
    assert b'TestUser' in response.data
    assert b'AnotherUser' in response.data

def test_create_room(client):
    """Test creating a new chat room."""
    response = client.post('/api/rooms/create', 
                          data={'roomName': 'New Test Room', 'username': 'TestUser'},
                          follow_redirects=True)
    assert response.status_code == 200
    
    # Check if the new room appears in the response
    assert b'New Test Room' in response.data
    assert b'TestUser' in response.data
    
    # Check if the room was actually added to the database
    response = client.get('/api/rooms?username=TestUser')
    assert b'New Test Room' in response.data

def test_create_room_empty_name(client):
    """Test creating a room with an empty name returns an error."""
    response = client.post('/api/rooms/create', 
                          data={'roomName': '', 'username': 'TestUser'},
                          follow_redirects=True)
    assert response.status_code == 400
    assert b'Room name is required' in response.data

def test_edit_room(client):
    """Test editing an existing room."""
    # First, create a room that we own
    client.post('/api/rooms/create', 
               data={'roomName': 'Room To Edit', 'username': 'TestUser'},
               follow_redirects=True)
    
    # Get the room ID - since we know we have rooms 1 and 2 already, this should be 3
    room_id = 3
    
    # Get the edit form
    response = client.get(f'/api/rooms/{room_id}/edit-form')
    assert response.status_code == 200
    assert b'Room To Edit' in response.data
    
    # Edit the room
    response = client.put(f'/api/rooms/{room_id}/edit?username=TestUser', 
                         data={'roomName': 'Edited Room Name'})
    assert response.status_code == 200
    assert b'Edited Room Name' in response.data
    assert b'TestUser' in response.data
    
    # Check if it was actually edited
    response = client.get('/api/rooms?username=TestUser')
    assert b'Edited Room Name' in response.data

def test_edit_room_not_found(client):
    """Test editing a non-existent room."""
    response = client.put('/api/rooms/999/edit?username=TestUser', 
                         data={'roomName': 'Edited Room Name'})
    assert response.status_code == 404
    assert b'Room not found' in response.data

def test_delete_room(client):
    """Test deleting a room."""
    # First, create a room that we own
    client.post('/api/rooms/create', 
               data={'roomName': 'Room To Delete', 'username': 'TestUser'},
               follow_redirects=True)
    
    # Get the room ID - since we know we have rooms 1, 2, and possibly 3 already, this should be 3 or 4
    room_id = 3  # This assumes test_edit_room hasn't run yet
    
    # Delete the room
    response = client.delete(f'/api/rooms/{room_id}/delete?username=TestUser')
    assert response.status_code == 200
    
    # Check if it was actually deleted
    response = client.get('/api/rooms?username=TestUser')
    assert b'Room To Delete' not in response.data

def test_delete_room_not_found(client):
    """Test deleting a non-existent room."""
    response = client.delete('/api/rooms/999/delete?username=TestUser')
    assert response.status_code == 404
    assert b'Room not found' in response.data

def test_get_create_room_form(client):
    """Test getting the create room form."""
    response = client.get('/api/rooms/create-form')
    assert response.status_code == 200
    assert b'<form' in response.data
    assert b'Room Name' in response.data
    assert b'Create Room' in response.data

def test_cancel_create_room(client):
    """Test canceling room creation."""
    response = client.get('/api/rooms/cancel-create')
    assert response.status_code == 200
    assert response.data == b''  # Should return empty string