from flask import Flask, session, request, jsonify
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "asdfsdf"
app.permanent_session_lifetime = timedelta(minutes=1)

credentials = {
    "admin":"admin",
    "user1":"user1"
}

@app.route("/login",methods=["POST"])
def loginsession():
    req = request.get_json()
    username = req.get("username")
    password = req.get("password")

    if username in credentials:
        if credentials.get(username) == password:
            session.permanent = True
            session["user"] = username
            return jsonify({"success": True})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/auth", methods=["GET"])
def auth():
    if "user" in session:
        return ("OK", 200)
    return ("Unauthorized", 401)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user",None)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)