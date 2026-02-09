# Task Manager with MongoDB and WebSocket Integration

A FastAPI-based task management application with real-time WebSocket updates.

## Features

- User registration and authentication (JWT)
- CRUD operations for tasks
- Real-time WebSocket notifications for task changes
- MongoDB database integration

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure MongoDB is running on `mongodb://localhost:27017`

3. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login and get JWT token

### Tasks (Protected)
- `POST /tasks` - Create a new task
- `GET /tasks` - Get all user's tasks
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### WebSocket
- `WS /ws/tasks?token={jwt_token}` - Real-time task updates

## WebSocket Integration

The application now includes real-time WebSocket support:

1. **Connection**: Connect to `/ws/tasks?token={your_jwt_token}`
2. **Real-time Updates**: Receive notifications when tasks are created, updated, or deleted
3. **User-specific**: Each user only receives updates for their own tasks

### WebSocket Message Format

```json
{
  "type": "task_update",
  "action": "created|updated|deleted",
  "task": {
    "id": "task_id",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2024-01-01T00:00:00"
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

## Testing WebSocket

You can test the WebSocket connection using JavaScript:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/tasks?token=YOUR_JWT_TOKEN');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

ws.onopen = function() {
    console.log('WebSocket connected');
};
```

## Architecture

- `main.py`: FastAPI application with HTTP and WebSocket endpoints
- `auth.py`: Authentication utilities (JWT, password hashing)
- `database.py`: MongoDB connection setup
- `schemas.py`: Pydantic models for request/response validation
- `websocket.py`: WebSocket connection manager for real-time updates