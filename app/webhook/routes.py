

from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    # Get the GitHub event type from the header
    event_type = request.headers.get('X-GitHub-Event', 'ping')

    data = request.get_json()
    payload = {}

    # Handle push events
    if event_type == "push":
        payload = {
            "author": data.get("pusher", {}).get("name", "Unknown"),
            "from_branch": None,
            "to_branch": data.get("ref", "Unknown").split("/")[-1],
            "action": "push",
            "timestamp": datetime.utcnow().isoformat()
        }

    # Handle pull request opened/closed (merge)
    elif event_type == "pull_request":
        pull_request = data.get("pull_request", {})
        is_merged = pull_request.get("merged", False)
        action = "merge" if is_merged else "pull_request"

        payload = {
            "author": pull_request.get("user", {}).get("login", "Unknown"),
            "from_branch": pull_request.get("head", {}).get("ref", "Unknown"),
            "to_branch": pull_request.get("base", {}).get("ref", "Unknown"),
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        }

    # Other events
    else:
        payload = {
            "author": "Unknown",
            "from_branch": None,
            "to_branch": None,
            "action": event_type,
            "timestamp": datetime.utcnow().isoformat()
        }

    # Save to MongoDB
    mongo.db.events.insert_one(payload)

    return jsonify({"status": "success", "data": payload}), 200


# API to fetch all events
@webhook.route('/events', methods=["GET"])
def get_events():
    events = list(mongo.db.events.find({}, {"_id": 0}))  # Exclude MongoDB's _id field
    return jsonify(events), 200
