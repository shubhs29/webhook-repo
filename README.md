# GitHub Webhook Monitor - Backend System

This repository contains the webhook receiver, MongoDB storage, and UI for monitoring GitHub events.

## Features
- Receives GitHub webhook events (push, pull request, merge)
- Stores event data in MongoDB
- Displays events in a clean UI with 15-second auto-refresh
- RESTful API for retrieving events

## Prerequisites
- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- ngrok (for local testing with GitHub webhooks)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-webhook-repo-url>
cd webhook-repo
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB
Edit `config.py` and set your MongoDB connection string:
```python
MONGODB_URI = "mongodb://localhost:27017/"  # or your MongoDB Atlas URI
```

### 4. Run the Application
```bash
python app.py
```

The server will start on `http://localhost:5000`

### 5. Expose Local Server (for testing)
```bash
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 6. Configure GitHub Webhook
1. Go to your `action-repo` on GitHub
2. Settings → Webhooks → Add webhook
3. Payload URL: `https://abc123.ngrok.io/webhook`
4. Content type: `application/json`
5. Events: Select "Just the push event" and "Pull requests"
6. Click "Add webhook"

## API Endpoints

### POST /webhook
Receives GitHub webhook events

### GET /events
Returns all stored events in reverse chronological order

### GET /
Serves the UI

## Project Structure
```
webhook-repo/
├── app.py              # Flask application
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
├── static/
│   ├── style.css      # UI styling
│   └── script.js      # UI logic
└── templates/
    └── index.html     # UI template
```

## Testing
1. Push code to `action-repo`
2. Create a pull request
3. Merge a pull request
4. Check the UI at `http://localhost:5000`

## Deployment
For production, deploy to:
- Heroku
- AWS EC2
- DigitalOcean
- Render
- Railway

Remember to update the webhook URL in GitHub settings after deployment.
