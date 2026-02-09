from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_rpc():
    payload = request.json

    if payload["method"] == "context.getUser":
        return jsonify({
            "jsonrpc": "2.0",
            "id": payload["id"],
            "result": {
                "email": "suvansh.tembe@iauro.com"
            }
        })

    return jsonify({
        "jsonrpc": "2.0",
        "id": payload["id"],
        "error": {"message": "Method not found"}
    })


if __name__ == "__main__":
    print("Context MCP Server running on http://localhost:3333")
    app.run(port=3333)
