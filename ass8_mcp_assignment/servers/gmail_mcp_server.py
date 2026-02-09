from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_rpc():
    payload = request.json

    # Handle Gmail calendar upcoming events RPC
    if payload["method"] == "gmail.calendar.getUpcomingEvents":
        now = datetime.now()

        events = [
            {
                "id": "evt-001",
                "subject": "Team Sync",
                "start": now.isoformat(),
                "end": (now + timedelta(minutes=30)).isoformat(),
                "location": "Google Meet",
                "description": "Weekly team alignment meeting"
            },
            {
                "id": "evt-002",
                "subject": "Design Review",
                "start": (now + timedelta(hours=2)).isoformat(),
                "end": (now + timedelta(hours=3)).isoformat(),
                "location": "Conference Room A",
                "description": "Review UI/UX designs for the new feature"
            }
        ]


        return jsonify({
            "jsonrpc": "2.0",
            "id": payload["id"],
            "result": events
        })

    return jsonify({
        "jsonrpc": "2.0",
        "id": payload["id"],
        "error": {"message": "Method not found"}
    })


if __name__ == "__main__":
    print("Gmail MCP Server running on http://localhost:4444")
    app.run(port=4444)

