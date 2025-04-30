import pytest
import os
import sys
import json
import tempfile
import shutil
from datetime import datetime

# Add the parent directory to the path so we can import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

@pytest.fixture
def client():
    # Create a temporary directory for test data
    test_data_dir = tempfile.mkdtemp()
    
    # Set up the app with test configuration
    main.DATA_DIR = test_data_dir
    main.ROOMS_FILE = os.path.join(test_data_dir, 'rooms.json')
    main.JOINED_ROOMS_FILE = os.path.join(test_data_dir, 'joined_rooms.json')
    
    # Initialize with test data
    rooms = [
        {'id': 1, 'name': 'Test Room 1', 'owner': 'TestUser', 'createdAt': datetime.now().isoformat()},
        {'id': 2, 'name': 'Test Room 2', 'owner': 'AnotherUser', 'createdAt': datetime.now().isoformat()}
    ]
    
    # Create data directory and save initial test data
    os.makedirs(test_data_dir, exist_ok=True)
    with open(main.ROOMS_FILE, 'w') as f:
        json.dump(rooms, f)
    
    joined_rooms = {
        'TestUser': [1]
    }
    
    with open(main.JOINED_ROOMS_FILE, 'w') as f:
        json.dump(joined_rooms, f)
    
    # Reset global variables with test data
    main.chat_rooms = rooms.copy()
    main.next_id = max([room['id'] for room in rooms]) + 1
    main.joined_rooms = joined_rooms.copy()
    
    # Create a test client
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        yield client
    
    # Clean up after the test
    shutil.rmtree(test_data_dir)