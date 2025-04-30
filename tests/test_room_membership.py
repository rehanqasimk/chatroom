import json
import pytest
from bs4 import BeautifulSoup

def test_join_room(client):
    """Test joining a room."""
    # Use room_id 2 which is owned by 'AnotherUser'
    room_id = 2
    
    # Join the room as TestUser
    response = client.get(f'/api/rooms/{room_id}/join?username=TestUser')
    assert response.status_code == 200
    
    # Check that the response shows the room as joined
    assert b'Leave' in response.data
    
    # Check if room class has joined-room class
    soup = BeautifulSoup(response.data, 'html.parser')
    room_div = soup.find(id=f'room-{room_id}')
    assert room_div is not None
    assert 'joined-room' in room_div['class']

def test_join_room_not_found(client):
    """Test joining a non-existent room."""
    response = client.get('/api/rooms/999/join?username=TestUser')
    assert response.status_code == 404
    assert b'Room not found' in response.data

def test_leave_room(client):
    """Test leaving a room."""
    # TestUser has already joined room 1 (from conftest.py)
    room_id = 1
    
    # First verify that user is in the room
    response = client.get('/api/rooms?username=TestUser')
    soup = BeautifulSoup(response.data, 'html.parser')
    room_div = soup.find(id=f'room-{room_id}')
    assert room_div is not None
    assert 'joined-room' in room_div['class']
    
    # Leave the room
    response = client.get(f'/api/rooms/{room_id}/leave?username=TestUser')
    assert response.status_code == 200
    
    # Check that the response shows the room as not joined
    assert b'Join' in response.data  # Should show Join button now
    
    # Check that joined-room class is no longer present
    soup = BeautifulSoup(response.data, 'html.parser')
    room_div = soup.find(id=f'room-{room_id}')
    assert room_div is not None
    assert 'joined-room' not in room_div['class']

def test_leave_room_not_found(client):
    """Test leaving a non-existent room."""
    response = client.get('/api/rooms/999/leave?username=TestUser')
    assert response.status_code == 404
    assert b'Room not found' in response.data

def test_leave_room_not_joined(client):
    """Test leaving a room that the user hasn't joined."""
    # Create a new user who hasn't joined any rooms
    response = client.get(f'/api/rooms/1/leave?username=NewUser')
    assert response.status_code == 200
    
    # Should succeed but not affect anything
    assert b'Join' in response.data