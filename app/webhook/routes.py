from flask import Blueprint, request, jsonify
from datetime import datetime
from app.webhook.models import extract_push_data, extract_pull_request_data, format_timestamp
from app.webhook.extensions import get_collection, get_client

webhook = Blueprint('webhook', __name__)

@webhook.route('/webhook', methods=['POST'])
def receiver():
    """Endpoint to receive GitHub webhook events"""
    collection = get_collection()
    
    if request.method == 'POST':
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')
        
        try:
            event_data = None
            
            if event_type == 'push':
                event_data = extract_push_data(payload)
            
            elif event_type == 'pull_request':
                action = payload.get("action", "")
                if action in ["opened", "closed"]:
                    event_data = extract_pull_request_data(payload)
            
            if event_data:
                result = collection.insert_one(event_data)
                print(f"✅ Stored event: {event_data['action']} by {event_data['author']}")
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


@webhook.route('/events', methods=['GET'])
def get_events():
    """API endpoint to retrieve all events"""
    collection = get_collection()
    
    try:
        events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1))
        
        for event in events:
            if isinstance(event.get("timestamp"), datetime):
                event["timestamp"] = format_timestamp(event["timestamp"])
        
        return jsonify({
            "status": "success",
            "count": len(events),
            "events": events
        }), 200
    
    except Exception as e:
        print(f"❌ Error retrieving events: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@webhook.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        client = get_client()
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