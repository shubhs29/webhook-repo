from datetime import datetime

def get_ordinal_suffix(day):
    """Get ordinal suffix for day (1st, 2nd, 3rd, etc.)"""
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return str(day) + suffix


def format_timestamp(dt):
    """Format timestamp as: 1st April 2021 - 9:30 PM UTC"""
    day_with_suffix = get_ordinal_suffix(dt.day)
    formatted = dt.strftime(f"{day_with_suffix} %B %Y - %I:%M %p UTC")
    return formatted


def extract_push_data(payload):
    """Extract relevant data from GitHub push event"""
    return {
        "request_id": payload.get("after", "")[:7],
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