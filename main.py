import time
import traceback

from utils import dblib as db
from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route("/get", methods=["GET"])
def handle_get_resources(request):
    data = request.get_json()
    if 'resource_name' in data and data['resource_name'] == "location_name":
        if 'value' in data:
            return db.get_coords(data['value'])

    return {
        "msg": "Invalid request (Invalid JSON)",
        "status": 403
    }, 403


@app.route("/")
def index():
    # db.insert_new_location(47.15739, 27.58695, "Palatul Culturii",
    #                        "https://www.youtube.com/watch?v=eHT5ivcpeYI", "Palatul de langa Mall")
    # user = db.get_user_id("Daniel")
    # location = db.get_location_id("Palatul Culturii")
    # if user and location:
    #     db.user_add_new_challange(user, location)
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
