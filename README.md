# Copilot Agency Study

This project is not just a task API; it's a study.

I built this during Microsoft Build 2026 to understand where 
GitHub Copilot Agent actually helps, and where human judgment 
is still irreplaceable. Five issues, five experiments, one 
question: when should you trust the agent?

What I found: Copilot is spec-compliant, but not wisdom-aware.
It implemented a DELETE endpoint correctly per the spec, then 
silently introduced an ID collision bug it never flagged. It 
refactored cleanly, but made four architectural decisions 
without disclosure. It pushed back on a flawed bug report, 
and was right to. It never once asked a clarifying question.

My conclusion: the agent stays true to its training 
distribution. It handles patterns it has seen before with 
confidence. It cannot intuit what the spec forgot to say. 
That gap, between spec compliance and real-world correctness, 
is where human judgment still lives.

## Running the App Locally

### Prerequisites
- Python 3.7+
- Flask

### Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python -m flask run
   ```
   
The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Get All Tasks
**GET** `/tasks`

Retrieve all tasks in the system.

**Request:**
```bash
curl -X GET http://localhost:5000/tasks
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "done": false
  },
  {
    "id": 2,
    "title": "Complete project",
    "done": true
  }
]
```

### 2. Create a Task
**POST** `/tasks`

Create a new task.

**Request:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask"}'
```

**Request Body:**
```json
{
  "title": "Learn Flask"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "title": "Learn Flask",
  "done": false
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "title required"
}
```

### 3. Update a Task
**PATCH** `/tasks/<id>`

Update the completion status of a task.

**Request:**
```bash
curl -X PATCH http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

**Request Body:**
```json
{
  "done": true
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "done": true
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "not found"
}
```

### 4. Delete a Task
**DELETE** `/tasks/<id>`

Delete a task by ID.

**Request:**
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

**Response (204 No Content):**
```
(empty response body)
```

**Error Response (404 Not Found):**
```json
{
  "error": "not found"
}
```

## Request/Response Formats

All requests and responses use JSON format with `Content-Type: application/json`.

### Task Object
```json
{
  "id": 1,
  "title": "Task title",
  "done": false
}
```

### Status Codes
- **200 OK** - Successful GET/PATCH request
- **201 Created** - Task successfully created
- **204 No Content** - Task successfully deleted
- **400 Bad Request** - Invalid request (missing required fields)
- **404 Not Found** - Task does not exist

## Project Structure

```
app/
  __init__.py          - Flask app initialization
  routes.py            - API route handlers
  services.py          - TaskService business logic
tests/                 - Test files
README.md              - This file
requirements.txt       - Python dependencies
```
