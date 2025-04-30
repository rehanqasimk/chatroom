import json
import os
import pytest
import tempfile
import sys
from datetime import datetime

# Add the parent directory to the path so we can import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

def test_load_rooms():
    """Test loading rooms from file."""
    # Create a temporary directory and file
    with tempfile.TemporaryDirectory() as temp_dir:
        rooms_file = os.path.join(temp_dir, 'test_rooms.json')
        
        # Create test data
        test_rooms = [
            {'id': 1, 'name': 'Test Room', 'owner': 'TestUser', 'createdAt': datetime.now().isoformat()}
        ]
        
        # Write test data to file
        with open(rooms_file, 'w') as f:
            json.dump(test_rooms, f)
        
        # Set the global variable to our test file
        main.ROOMS_FILE = rooms_file
        
        # Load rooms
        rooms = main.load_rooms()
        
        # Check that rooms were loaded correctly
        assert len(rooms) == 1
        assert rooms[0]['id'] == 1
        assert rooms[0]['name'] == 'Test Room'
        assert rooms[0]['owner'] == 'TestUser'

def test_load_rooms_no_file():
    """Test loading rooms when file doesn't exist."""
    # Create a non-existent file path
    with tempfile.TemporaryDirectory() as temp_dir:
        rooms_file = os.path.join(temp_dir, 'nonexistent_file.json')
        
        # Set the global variable to our test file
        main.ROOMS_FILE = rooms_file
        
        # Load rooms (should create default rooms)
        rooms = main.load_rooms()
        
        # Check that default rooms were created
        assert len(rooms) == 2  # Two default rooms
        assert rooms[0]['name'] == 'General Discussion'
        assert rooms[1]['name'] == 'Tech Talk'

def test_save_rooms():
    """Test saving rooms to file."""
    # Create a temporary directory and file
    with tempfile.TemporaryDirectory() as temp_dir:
        rooms_file = os.path.join(temp_dir, 'test_rooms.json')
        
        # Create test data
        test_rooms = [
            {'id': 1, 'name': 'Test Room', 'owner': 'TestUser', 'createdAt': datetime.now().isoformat()}
        ]
        
        # Set the global variable to our test file
        main.ROOMS_FILE = rooms_file
        
        # Save rooms
        main.save_rooms(test_rooms)
        
        # Check that file exists and contains the correct data
        assert os.path.exists(rooms_file)
        
        with open(rooms_file, 'r') as f:
            saved_rooms = json.load(f)
            
        assert len(saved_rooms) == 1
        assert saved_rooms[0]['id'] == 1
        assert saved_rooms[0]['name'] == 'Test Room'
        assert saved_rooms[0]['owner'] == 'TestUser'

def test_load_joined_rooms():
    """Test loading joined rooms from file."""
    # Create a temporary directory and file
    with tempfile.TemporaryDirectory() as temp_dir:
        joined_rooms_file = os.path.join(temp_dir, 'test_joined_rooms.json')
        
        # Create test data
        test_joined_rooms = {
            'TestUser': [1, 2]
        }
        
        # Write test data to file
        with open(joined_rooms_file, 'w') as f:
            json.dump(test_joined_rooms, f)
        
        # Set the global variable to our test file
        main.JOINED_ROOMS_FILE = joined_rooms_file
        
        # Load joined rooms
        joined_rooms = main.load_joined_rooms()
        
        # Check that joined rooms were loaded correctly
        assert 'TestUser' in joined_rooms
        assert joined_rooms['TestUser'] == [1, 2]

def test_load_joined_rooms_no_file():
    """Test loading joined rooms when file doesn't exist."""
    # Create a non-existent file path
    with tempfile.TemporaryDirectory() as temp_dir:
        joined_rooms_file = os.path.join(temp_dir, 'nonexistent_file.json')
        
        # Set the global variable to our test file
        main.JOINED_ROOMS_FILE = joined_rooms_file
        
        # Load joined rooms (should create empty dict)
        joined_rooms = main.load_joined_rooms()
        
        # Check that an empty dict was created
        assert joined_rooms == {}

def test_save_joined_rooms():
    """Test saving joined rooms to file."""
    # Create a temporary directory and file
    with tempfile.TemporaryDirectory() as temp_dir:
        joined_rooms_file = os.path.join(temp_dir, 'test_joined_rooms.json')
        
        # Create test data
        test_joined_rooms = {
            'TestUser': [1, 2]
        }
        
        # Set the global variable to our test file
        main.JOINED_ROOMS_FILE = joined_rooms_file
        
        # Save joined rooms
        main.save_joined_rooms(test_joined_rooms)
        
        # Check that file exists and contains the correct data
        assert os.path.exists(joined_rooms_file)
        
        with open(joined_rooms_file, 'r') as f:
            saved_joined_rooms = json.load(f)
            
        assert 'TestUser' in saved_joined_rooms
        assert saved_joined_rooms['TestUser'] == [1, 2]