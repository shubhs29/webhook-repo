from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os
from config import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME

app = Flask(__name__)

# MongoDB setup
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Create index on timestamp for faster queries
collection.create_index([("timestamp", -1)])


def extract_push_data(payload):
    """Extract relevant data from GitHub push event"""
    return {
        "request_id": payload.get("after", "")[:7],  # Short commit hash
        "author": payload.get("pusher", {}).get("name", "Unknown"),
        "action": "PUSH",
        "from_branch": None,
        "to_branch": payload.get("ref", "").replace("refs/heads/", ""),
        "timestamp": datetime.utcnow()
    }


def extract_pull_request_data(payload):
    """Extract relevant data from GitHub pull request event"""
    pr = payload.get("pull_request", {})
    action_type = payload.get("action", "")
    
    # Determine if it's a merge or just a PR
    if action_type == "closed" and pr.get("merged", False):
        action = "MERGE"
    else:
        action = "PULL_REQUEST"
    
    return {
        "request_id": str(pr.get("number", "")),
        "author": pr.get("user", {}).get("login", "Unknown"),
        "action": action,
        "from_branch": pr.get("head", {}).get("ref", "Unknown"),
        "to_branch": pr.get("base", {}).get("ref", "Unknown"),
        "timestamp": datetime.utcnow()
    }


@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint to receive GitHub webhook events"""
    if request.method == 'POST':
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')
        
        try:
            event_data = None
            
            if event_type == 'push':
                event_data = extract_push_data(payload)
            
            elif event_type == 'pull_request':
                # Only process opened and closed (merged) PRs
                action = payload.get("action", "")
                if action in ["opened", "closed"]:
                    event_data = extract_pull_request_data(payload)
            
            # Store in MongoDB if we have valid data
            if event_data:
                result = collection.insert_one(event_data)
                print(f" Stored event: {event_data['action']} by {event_data['author']}")
                return jsonify({
                    "status": "success",
                    "message": "Event stored successfully",
                    "id": str(result.inserted_id)
                }), 200
            else:
                return jsonify({
                    "status": "ignored",
                    "message": "Event type not tracked"
                }), 200
                
        except Exception as e:
            print(f"❌ Error processing webhook: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@app.route('/events', methods=['GET'])
def get_events():
    """API endpoint to retrieve all events"""
    try:
        # Get all events sorted by timestamp (newest first)
        events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1))
        
        # Format timestamps as strings
        for event in events:
            if isinstance(event.get("timestamp"), datetime):
                event["timestamp"] = event["timestamp"].strftime("%d %b %Y - %I:%M %p UTC")
        
        return jsonify({
            "status": "success",
            "count": len(events),
            "events": events
        }), 200
    
    except Exception as e:
        print(f"Error retrieving events: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/')
def index():
    """Serve the UI"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test MongoDB connection
        client.server_info()
        return jsonify({
            "status": "healthy",
            "mongodb": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "mongodb": "disconnected",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Starting GitHub Webhook Monitor...")
    print(f"📊 MongoDB: {DATABASE_NAME}.{COLLECTION_NAME}")
    print(f"🌐 Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
