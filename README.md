# Chat Room Application

A simple chat room application that allows users to create, edit, and delete chat rooms using HTMX without full page reloads.

## Overview

This application demonstrates the use of HTMX to create a seamless user experience with a single-page-like application without using a complex frontend framework. The application allows users to:

- Create new chat rooms with unique names
- Edit the names of their own chat rooms
- Delete their own chat rooms
- View a list of available chat rooms
- "Join" chat rooms (view-only functionality)

## Technologies Used

- **HTML5**: For the page structure
- **CSS3**: For styling the application
- **JavaScript**: For client-side logic
- **HTMX**: For handling AJAX requests without full page reloads
- **Hyperscript**: For additional interactive behaviors

## Project Structure

```
chat-room/
├── css/
│   └── styles.css         # Styling for the application
├── js/
│   ├── app.js             # Main application logic
│   └── mock-api.js        # Mock API service that simulates a backend
├── index.html             # Main HTML file
└── README.md              # This documentation file
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd chat-room
   ```

2. Since this is a pure frontend application with no build steps, you can open it directly in your browser:
   - Double-click on `index.html`, or
   - Use a local development server like Python's built-in HTTP server:
     ```
     python -m http.server
     ```
     Then navigate to `http://localhost:8000` in your browser.
   - Or use any other static file server of your choice.

## How to Use the Application

### User Identification

- When you first load the application, you'll be assigned a random username (e.g., "User123").
- You can change your username by editing the "Logged in as:" input field.
- Your username determines which chat rooms you own and can therefore edit or delete.

### Creating a Chat Room

1. Click the "Create Room" button at the top of the page.
2. Enter a name for your chat room in the form that appears.
3. Click "Create Room" to add it to the list.

### Editing a Chat Room

1. For rooms that you own (created by your current username), an "Edit" button will be visible.
2. Click "Edit" to open the edit form.
3. Change the room name in the form.
4. Click "Update Room" to save your changes, or "Cancel" to discard them.

### Deleting a Chat Room

1. For rooms that you own, a "Delete" button will be visible.
2. Click "Delete" to remove the room.
3. Confirm the deletion when prompted.

### Joining a Chat Room

- Click the "Join" button on any room to simulate joining the room.
- (Note: In this demo, the actual chat room view is not implemented as per requirements.)

## Design Decisions and Assumptions

### Backend Simulation

- The application uses a mock API service to simulate backend functionality.
- All data is stored in memory and will be reset when the page is refreshed.
- In a real application, these would be replaced with actual API endpoints.

### HTMX Integration

- HTMX is used to handle all AJAX operations, providing a seamless user experience without page reloads.
- The application leverages HTMX attributes such as:
  - `hx-get`, `hx-post`, `hx-put`, `hx-delete`: For handling different HTTP methods
  - `hx-target`: For specifying where the response should be inserted
  - `hx-swap`: For controlling how the response is inserted
  - `hx-trigger`: For defining what event triggers the request

### User Ownership

- Room ownership is determined by the username of the creator.
- Only the creator of a room (based on the current username) can edit or delete it.
- This is a simplification for the demo - in a real application, proper authentication would be used.

### User Interface

- The UI is designed to be simple and intuitive.
- Toast notifications provide feedback for user actions.
- Form validation ensures that room names cannot be empty.

## Future Enhancements

- Implement actual chat functionality within rooms
- Add user authentication
- Persist data using a real backend and database
- Add real-time updates using WebSockets
- Implement search functionality for rooms
- Add user profile customization

## License

[MIT License](LICENSE)
