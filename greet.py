import json
import redis
from flask import Flask, request
from typing import Text, Optional, Dict, Any

app = Flask(__name__)


def get_current_user() -> Optional[Dict[Text, Any]]:
    """Extract current user details from storage."""

    red = redis.StrictRedis(host="localhost", port=6379, db=1)
    encoded_user = red.get("user")
    if encoded_user:
        return json.loads(encoded_user)
    else:
        return None


def store_user(user: Dict[Text, Any]) -> None:
    """Save user details to our storage."""

    red = redis.StrictRedis(host="localhost", port=6379, db=1)
    red.set("user", json.dumps(user))


@app.route('/', methods=["GET"])
def greet():
    """greet the user."""

    user = get_current_user()
    if user is not None:
        return "Hello, {}!".format(user.get("name"))
    else:
        return "Hello, unknown stranger!"


@app.route('/', methods=["POST"])
def save_name():
    """Change a users details"""

    user = request.json
    store_user(user)
    return "I'll try to remember your name, {}!".format(user.get("name"))


app.run(port=8080)
